"""strumenti.py (ADR-0113): i dati decidono, il kernel scarica-verifica-estrae e basta.

Tutto offline: gli archivi finti si servono da `file://`, quindi i test non
dipendono dalla rete e girano uguali in CI e in locale.
"""
from __future__ import annotations

import hashlib
import io
import json
import re
import sys
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import strumenti as S  # noqa: E402

PIATT = S.piattaforma()


def _tar_xz(nome: str, contenuto: bytes) -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:xz") as t:
        info = tarfile.TarInfo(f"{nome}-x86_64/{nome}")
        info.size = len(contenuto)
        t.addfile(info, io.BytesIO(contenuto))
        lic = b"Apache-2.0"
        info = tarfile.TarInfo(f"{nome}-x86_64/LICENSE")
        info.size = len(lic)
        t.addfile(info, io.BytesIO(lic))
    return buf.getvalue()


class DatiFinti(unittest.TestCase):
    """Un mise.toml e un mise.lock in una cartella temporanea, con un archivio vero."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.binario = b"#!/bin/sh\necho 'finto 1.2.3'\n"
        self.archivio = self.tmp / "finto-1.2.3.tar.xz"
        self.archivio.write_bytes(_tar_xz("finto", self.binario))
        self.sha = hashlib.sha256(self.archivio.read_bytes()).hexdigest()
        self.scrivi(self.sha)

    def scrivi(self, sha: str):
        (self.tmp / "mise.toml").write_text('[tools]\n"aqua:esempio/finto" = "1.2.3"\n')
        (self.tmp / "mise.lock").write_text(
            'lockfile_version = 3\n\n[[tools."aqua:esempio/finto"]]\nversion = "1.2.3"\n'
            'backend = "aqua:esempio/finto"\n\n'
            f'[tools."aqua:esempio/finto"."platforms.{PIATT}"]\n'
            f'checksum = "sha256:{sha}"\nurl = "{self.archivio.as_uri()}"\n')

    def voci(self):
        return S.voci(PIATT, self.tmp / "mise.toml", self.tmp / "mise.lock")


class TestDati(DatiFinti):
    def test_il_nome_dell_eseguibile_viene_dalla_chiave(self):
        self.assertEqual(S.nome_eseguibile("aqua:typst/typst"), "typst")
        self.assertEqual(S.nome_eseguibile("pdfcpu"), "pdfcpu")

    def test_la_piattaforma_usa_i_nomi_di_mise(self):
        self.assertEqual(S.piattaforma("Linux", "x86_64"), "linux-x64")
        self.assertEqual(S.piattaforma("Darwin", "arm64"), "macos-arm64")
        self.assertEqual(S.piattaforma("Windows", "AMD64"), "windows-x64")

    def test_voce_letta_dal_lockfile(self):
        (v,) = self.voci()
        self.assertEqual((v.nome, v.versione, v.sha256), ("finto", "1.2.3", self.sha))

    def test_una_piattaforma_assente_non_ha_url(self):
        (v,) = S.voci("plan9-mips", self.tmp / "mise.toml", self.tmp / "mise.lock")
        self.assertIsNone(v.url)
        ok, msg = S.installa_voce(v, self.tmp / "dest")
        self.assertFalse(ok)
        self.assertIn("mise lock", msg)

    def test_una_versione_che_il_lockfile_non_ha_non_si_installa(self):
        (self.tmp / "mise.toml").write_text('[tools]\n"aqua:esempio/finto" = "9.9.9"\n')
        (v,) = self.voci()
        self.assertIsNone(v.sha256)


class TestInstalla(DatiFinti):
    def test_installa_estrae_solo_l_eseguibile(self):
        (v,) = self.voci()
        dest = self.tmp / "dest"
        ok, _ = S.installa_voce(v, dest)
        self.assertTrue(ok)
        self.assertEqual((dest / "bin" / "finto").read_bytes(), self.binario)
        self.assertFalse((dest / "bin" / "LICENSE").exists())

    def test_la_seconda_volta_non_scarica(self):
        (v,) = self.voci()
        dest = self.tmp / "dest"
        S.installa_voce(v, dest)

        def vietato(url):
            raise AssertionError("ha scaricato di nuovo")
        ok, msg = S.installa_voce(v, dest, vietato)
        self.assertTrue(ok)
        self.assertIn("già installato", msg)

    def test_uno_sha256_sbagliato_non_installa_niente(self):
        self.scrivi("0" * 64)
        (v,) = self.voci()
        dest = self.tmp / "dest"
        ok, msg = S.installa_voce(v, dest)
        self.assertFalse(ok)
        self.assertIn("diverso dal lockfile", msg)
        self.assertFalse((dest / "bin" / "finto").exists())

    def test_un_binario_cambiato_a_mano_si_reinstalla(self):
        (v,) = self.voci()
        dest = self.tmp / "dest"
        S.installa_voce(v, dest)
        (dest / "bin" / "finto").write_bytes(b"altro")
        ok, msg = S.installa_voce(v, dest)
        self.assertTrue(ok)
        self.assertIn("installato in", msg)
        self.assertEqual((dest / "bin" / "finto").read_bytes(), self.binario)


class TestRiprova(unittest.TestCase):
    """Un 5xx si riprova con attese crescenti; un 404 no."""

    def _finto(self, errori):
        import urllib.error
        from unittest import mock
        chiamate = []

        class Risposta(io.BytesIO):
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

        def apri(req, timeout):
            chiamate.append(1)
            if errori:
                raise urllib.error.HTTPError(req.full_url, errori.pop(0), "x", {}, None)
            return Risposta(b"ok")
        return mock.patch.object(S.urllib.request, "urlopen", apri), chiamate

    def test_un_504_si_riprova(self):
        attese = []
        patch, chiamate = self._finto([504, 502])
        with patch:
            self.assertEqual(S.scarica("https://x/y", dormi=attese.append), b"ok")
        self.assertEqual((len(chiamate), attese), (3, [2, 4]))

    def test_un_404_non_si_riprova(self):
        import urllib.error
        patch, chiamate = self._finto([404])
        with patch, self.assertRaises(urllib.error.HTTPError):
            S.scarica("https://x/y", dormi=lambda s: None)
        self.assertEqual(len(chiamate), 1)

    def test_dopo_l_ultimo_tentativo_l_errore_passa(self):
        import urllib.error
        patch, chiamate = self._finto([503] * (len(S.ATTESE) + 1))
        with patch, self.assertRaises(urllib.error.HTTPError):
            S.scarica("https://x/y", dormi=lambda s: None)
        self.assertEqual(len(chiamate), len(S.ATTESE) + 1)


class TestCache(DatiFinti):
    """STRUMENTI_CACHE: un archivio già scaricato non si riscarica, uno rotto sì."""

    def setUp(self):
        super().setUp()
        from unittest import mock
        self.cache = self.tmp / "cache"
        p = mock.patch.dict(S.os.environ, {"STRUMENTI_CACHE": str(self.cache)})
        p.start()
        self.addCleanup(p.stop)

    @staticmethod
    def vietato(url):
        raise OSError("rete giù (504)")

    def test_con_la_cache_si_installa_senza_rete(self):
        (v,) = self.voci()
        self.assertTrue(S.installa_voce(v, self.tmp / "a")[0])
        self.assertTrue((self.cache / "finto-1.2.3.tar.xz").exists())
        ok, _ = S.installa_voce(v, self.tmp / "b", self.vietato)
        self.assertTrue(ok)
        self.assertEqual((self.tmp / "b" / "bin" / "finto").read_bytes(), self.binario)

    def test_una_cache_rotta_si_riscarica(self):
        (v,) = self.voci()
        self.cache.mkdir()
        (self.cache / "finto-1.2.3.tar.xz").write_bytes(b"rotto")
        self.assertTrue(S.installa_voce(v, self.tmp / "a")[0])
        self.assertEqual(S._sha(self.cache / "finto-1.2.3.tar.xz"), self.sha)

    def test_un_archivio_con_lo_sha_sbagliato_non_entra_in_cache(self):
        self.scrivi("0" * 64)
        (v,) = self.voci()
        self.assertFalse(S.installa_voce(v, self.tmp / "a")[0])
        self.assertFalse((self.cache / "finto-1.2.3.tar.xz").exists())


class TestBundle(DatiFinti):
    def bundle(self, uscita: Path) -> Path:
        orig = (S.TOML, S.LOCK)
        S.TOML, S.LOCK = self.tmp / "mise.toml", self.tmp / "mise.lock"
        try:
            return S.costruisci_bundle(PIATT, uscita)
        finally:
            S.TOML, S.LOCK = orig

    def test_il_bundle_e_riproducibile(self):
        a = self.bundle(self.tmp / "a").read_bytes()
        b = self.bundle(self.tmp / "b").read_bytes()
        self.assertEqual(hashlib.sha256(a).hexdigest(), hashlib.sha256(b).hexdigest())

    def test_il_bundle_porta_archivi_dati_e_manifest(self):
        zp = self.bundle(self.tmp / "a")
        with zipfile.ZipFile(zp) as z:
            nomi = {n.split("/", 1)[1] for n in z.namelist()}
            man = json.loads(z.read(f"rumblingstone-strumenti-{PIATT}/BUNDLE.json"))
        self.assertTrue({"mise.toml", "mise.lock", "strumenti.py", "BUNDLE.json",
                         "archivi/finto-1.2.3.tar.xz"} <= nomi)
        self.assertEqual(man["strumenti"][0]["sha256"], self.sha)

    def test_si_installa_dal_bundle_senza_rete(self):
        zp = self.bundle(self.tmp / "a")
        self.archivio.unlink()  # la «rete» non c'è più
        (v,) = self.voci()
        ok, _ = S.installa_voce(v, self.tmp / "dest", S.da_bundle(zp))
        self.assertTrue(ok)
        self.assertEqual((self.tmp / "dest" / "bin" / "finto").read_bytes(), self.binario)


class TestDatiVeriDelRepo(unittest.TestCase):
    """Il mise.toml e il mise.lock del repo: completi, coerenti, mai «latest»."""

    def test_ogni_strumento_ha_url_e_sha256_su_ogni_piattaforma_dichiarata(self):
        import tomllib
        piatt = tomllib.loads(S.TOML.read_text())["settings"]["lockfile_platforms"]
        for p in piatt:
            for v in S.voci(p):
                self.assertTrue(v.url and v.sha256, f"{v.nome} su {p}")
                self.assertRegex(v.sha256, r"^[0-9a-f]{64}$")
                self.assertIn(v.versione, v.url, f"{v.nome} su {p}: URL di un'altra versione")

    def test_versioni_esatte(self):
        for chiave, v in S.leggi_toml().items():
            self.assertRegex(v, r"^\d+\.\d+\.\d+$", chiave)

    def test_la_ci_non_scrive_versioni_di_typst_a_mano(self):
        ci = (REPO / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        self.assertNotIn("TYPST_VERSION", ci)
        self.assertIsNone(re.search(r"releases/download/v[\d.]+/typst", ci))


if __name__ == "__main__":
    unittest.main()
