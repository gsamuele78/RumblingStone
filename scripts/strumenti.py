#!/usr/bin/env python3
"""strumenti.py — installa i binari del repo (typst, pdfcpu) da `mise.lock`, con lo sha256.

ADR-0113. È un **microkernel**: il codice non sa niente di typst né di pdfcpu.
Sa leggere due file standard, `mise.toml` (cosa serve, a che versione) e
`mise.lock` (per ogni piattaforma: l'URL dell'archivio e il suo sha256, scritti
da `mise lock`), e sa fare quattro cose sempre uguali: scaricare, verificare,
estrarre l'eseguibile, metterlo in una cartella sola. Uno strumento nuovo è una
riga in `mise.toml` e un `mise lock`, non una riga di codice qui.

    python3 scripts/strumenti.py elenco [--json]
    python3 scripts/strumenti.py installa [NOME ...] [--bin DIR] [--bundle ZIP]
                                          [--github-path] [--env-file F]
    python3 scripts/strumenti.py bundle [--piattaforma P ...] [--uscita DIR] [--con-ruote]
    python3 scripts/strumenti.py verifica [--bin DIR]
    python3 scripts/strumenti.py versione NOME

Perché non solo `mise`. `mise install --locked` fa la stessa cosa ed è lo
standard di fatto (ADR-0113 §Decisione): in CI gira in canale testing e il suo
risultato si confronta byte per byte con questo. Ma dove mise non c'è (il
container delle sessioni cloud, un portatile senza mise) questo script basta
Python 3.13 e la rete: niente binario in più di cui fidarsi. I due leggono gli
stessi dati, quindi non possono divergere sulle versioni; se divergono sui byte,
il job `strumenti` della CI diventa rosso.

Determinismo. Se l'eseguibile installato ha già lo sha256 registrato, non si
scarica niente. Un archivio con sha256 diverso dal lockfile non si estrae mai.
Dall'archivio si legge **un** file, quello che si chiama come lo strumento: niente
estrazione di percorsi arbitrari.

Dove. Di default in `<repo>/.strumenti/` (ignorata da git), così ogni clone ha
le sue versioni e non serve sudo; `binari.trova()` la guarda prima del PATH.

Exit: 0 fatto · 1 uno strumento fallito (checksum, rete, archivio) · 2 dati
mancanti (niente mise.lock, piattaforma non nel lockfile).

Solo stdlib.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import tomllib
import urllib.request
import zipfile
from pathlib import Path
from typing import Callable, NamedTuple

REPO = Path(__file__).resolve().parents[1]
TOML = REPO / "mise.toml"
LOCK = REPO / "mise.lock"
DEST = REPO / ".strumenti"
REGISTRO = "installati.json"

MANCA = 2


class Voce(NamedTuple):
    """Uno strumento su una piattaforma, come lo dice il lockfile."""

    chiave: str        # la chiave in mise.toml, es. "aqua:typst/typst"
    nome: str          # il nome dell'eseguibile, es. "typst"
    versione: str
    backend: str
    url: str | None
    sha256: str | None


# ── la piattaforma, coi nomi di mise ─────────────────────────────────────────

def piattaforma(sistema: str | None = None, macchina: str | None = None) -> str:
    """`linux-x64`, `macos-arm64`, `windows-x64`…: i nomi che usa `mise lock --platform`."""
    s = (sistema or platform.system()).lower()
    m = (macchina or platform.machine()).lower()
    os_ = {"linux": "linux", "darwin": "macos", "windows": "windows"}.get(s, s)
    arch = {"x86_64": "x64", "amd64": "x64", "aarch64": "arm64", "arm64": "arm64"}.get(m, m)
    return f"{os_}-{arch}"


def nome_eseguibile(chiave: str) -> str:
    """`aqua:typst/typst` → `typst`; `typst` → `typst`. L'ultimo pezzo dopo `:` e `/`."""
    return chiave.split(":", 1)[-1].rstrip("/").rsplit("/", 1)[-1]


# ── i dati ───────────────────────────────────────────────────────────────────

def leggi_toml(p: Path | None = None) -> dict[str, str]:
    """`{chiave: versione}` da `[tools]` di mise.toml. Solo versioni esatte."""
    p = p or TOML
    dati = tomllib.loads(p.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for k, v in dati.get("tools", {}).items():
        if isinstance(v, dict):
            v = v.get("version")
        if not isinstance(v, str):
            raise ValueError(f"mise.toml: {k} senza versione")
        out[k] = v
    return out


def _piattaforme(voce: dict) -> dict[str, dict]:
    """Le due grafie del lockfile: `"platforms.linux-x64" = {...}` (v3) e `platforms.linux-x64`."""
    out = {k.split(".", 1)[1]: v for k, v in voce.items()
           if k.startswith("platforms.") and isinstance(v, dict)}
    out.update(voce.get("platforms", {}) or {})
    return out


def leggi_lock(p: Path | None = None) -> dict[str, list[dict]]:
    dati = tomllib.loads((p or LOCK).read_text(encoding="utf-8"))
    tools = dati.get("tools", {})
    return {k: (v if isinstance(v, list) else [v]) for k, v in tools.items()}


def voci(piatt: str | None = None, toml_p: Path | None = None,
         lock_p: Path | None = None) -> list[Voce]:
    """Ogni strumento di mise.toml con URL e sha256 del lockfile per `piatt`."""
    piatt = piatt or piattaforma()
    toml_p, lock_p = toml_p or TOML, lock_p or LOCK
    chiesti = leggi_toml(toml_p)
    lock = leggi_lock(lock_p)
    out = []
    for chiave, versione in chiesti.items():
        corrispondenti = lock.get(chiave) or lock.get(nome_eseguibile(chiave)) or []
        voce = next((v for v in corrispondenti if v.get("version") == versione), None)
        if voce is None:
            out.append(Voce(chiave, nome_eseguibile(chiave), versione, "?", None, None))
            continue
        pv = _piattaforme(voce).get(piatt, {})
        sha = pv.get("checksum")
        if sha and sha.startswith("sha256:"):
            sha = sha.split(":", 1)[1]
        elif sha:
            sha = None  # un algoritmo che qui non verifichiamo non conta come verificato
        out.append(Voce(chiave, nome_eseguibile(chiave), versione,
                        voce.get("backend", "?"), pv.get("url"), sha))
    return out


def versione(nome: str, toml_p: Path | None = None) -> str:
    """La versione fissata di uno strumento, per nome dell'eseguibile."""
    for chiave, v in leggi_toml(toml_p).items():
        if nome_eseguibile(chiave) == nome:
            return v
    raise KeyError(f"{nome} non è in mise.toml")


# ── gli estrattori (i plugin del kernel: uno per formato d'archivio) ─────────

def _da_tar(dati: bytes, nome: str) -> bytes:
    with tarfile.open(fileobj=io.BytesIO(dati), mode="r:*") as tar:
        for m in tar.getmembers():
            if m.isfile() and Path(m.name).name in (nome, nome + ".exe"):
                return tar.extractfile(m).read()
    raise ValueError(f"nell'archivio non c'è un file chiamato {nome}")


def _da_zip(dati: bytes, nome: str) -> bytes:
    with zipfile.ZipFile(io.BytesIO(dati)) as z:
        for n in z.namelist():
            if not n.endswith("/") and Path(n).name in (nome, nome + ".exe"):
                return z.read(n)
    raise ValueError(f"nello zip non c'è un file chiamato {nome}")


def _nudo(dati: bytes, nome: str) -> bytes:
    return dati


ESTRATTORI: dict[str, Callable[[bytes, str], bytes]] = {
    ".tar.xz": _da_tar, ".tar.gz": _da_tar, ".tgz": _da_tar, ".tar.bz2": _da_tar,
    ".tar.zst": _da_tar, ".zip": _da_zip,
}


def estrattore(url: str) -> Callable[[bytes, str], bytes]:
    for suffisso, f in ESTRATTORI.items():
        if url.endswith(suffisso):
            return f
    return _nudo


# ── scarica, verifica, installa ──────────────────────────────────────────────

def scarica(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "RumblingStone strumenti.py"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read()


def _registro(dest: Path) -> dict:
    p = dest / REGISTRO
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _sha(p: Path) -> str | None:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except FileNotFoundError:
        return None


def installa_voce(v: Voce, dest: Path = DEST, scarica_f=scarica) -> tuple[bool, str]:
    """Installa una voce. `(ok, messaggio)`. Non scarica se è già lì con lo sha giusto."""
    if not v.url or not v.sha256:
        return False, (f"{v.nome} {v.versione}: mise.lock non ha URL e sha256 per "
                       f"{piattaforma()} — rigeneralo con `mise lock --platform {piattaforma()}`")
    suffisso = ".exe" if piattaforma().startswith("windows") else ""
    finale = dest / "bin" / (v.nome + suffisso)
    reg = _registro(dest)
    gia = reg.get(v.nome, {})
    if gia.get("archivio_sha256") == v.sha256 and _sha(finale) == gia.get("sha256"):
        return True, f"{v.nome} {v.versione}: già installato ({finale})"
    try:
        dati = scarica_f(v.url)
    except OSError as e:
        return False, f"{v.nome} {v.versione}: scaricamento fallito ({e})"
    sha = hashlib.sha256(dati).hexdigest()
    if sha != v.sha256:
        return False, (f"{v.nome} {v.versione}: sha256 {sha} diverso dal lockfile "
                       f"{v.sha256} — non installato")
    try:
        binario = estrattore(v.url)(dati, v.nome)
    except (ValueError, tarfile.TarError, zipfile.BadZipFile) as e:
        return False, f"{v.nome} {v.versione}: archivio illeggibile ({e})"
    finale.parent.mkdir(parents=True, exist_ok=True)
    tmp = finale.with_name(finale.name + ".tmp")
    tmp.write_bytes(binario)
    tmp.chmod(0o755)
    tmp.replace(finale)
    reg[v.nome] = {"versione": v.versione, "backend": v.backend, "url": v.url,
                   "archivio_sha256": v.sha256,
                   "sha256": hashlib.sha256(binario).hexdigest()}
    (dest / REGISTRO).write_text(json.dumps(reg, indent=1, sort_keys=True) + "\n",
                                 encoding="utf-8")
    return True, f"{v.nome} {v.versione}: installato in {finale} (archivio sha256 {sha[:16]}…)"


def verifica_voce(v: Voce, dest: Path = DEST) -> tuple[bool, str]:
    """L'eseguibile c'è, ha lo sha registrato e `--version` dice la versione fissata."""
    finale = dest / "bin" / v.nome
    if not finale.exists() and (finale.with_suffix(".exe")).exists():
        finale = finale.with_suffix(".exe")
    reg = _registro(dest).get(v.nome, {})
    if not finale.exists():
        return False, f"{v.nome}: non installato in {finale.parent}"
    if reg.get("archivio_sha256") != v.sha256 or _sha(finale) != reg.get("sha256"):
        return False, f"{v.nome}: installato, ma non quello di mise.lock (rilancia `installa`)"
    out = ""
    # La convenzione GNU, poi quella dei comandi Go: `version -c disable` è come
    # pdfcpu non scrive ~/.config/pdfcpu (ADR-0027).
    for args in (["--version"], ["version", "-c", "disable"]):
        try:
            r = subprocess.run([str(finale), *args], capture_output=True, text=True, timeout=60)
        except OSError as e:
            return False, f"{v.nome}: non si esegue ({e})"
        out = r.stdout + r.stderr
        if r.returncode == 0 and v.versione in out:
            break
    if v.versione not in out:
        return False, f"{v.nome}: dice «{out.strip()[:80]}», fissato {v.versione}"
    riga = next((r for r in out.splitlines() if v.versione in r), out.strip())
    return True, f"{v.nome} {v.versione}: ✓ {riga.strip()[:80]}"


# ── il bundle: tutto ciò che serve, in un file, verificabile ─────────────────
#
# Sul modello dei bundle di gsamuele78/iemod-fetch: per ogni piattaforma un zip
# che porta con sé ogni requisito, così si installa anche senza rete. Dentro ci
# sono gli **archivi originali** di upstream (con le loro licenze), con lo
# stesso sha256 del lockfile, più mise.toml, mise.lock, questo script e
# `BUNDLE.json`, che elenca ogni file col suo sha256. Il zip è riproducibile:
# nomi in ordine, data fissa (SOURCE_DATE_EPOCH), permessi fissi. Il workflow
# Release lo mette in SHA256SUMS e lo attesta con Sigstore.

BUNDLE_MANIFEST = "BUNDLE.json"

#: Le etichette di piattaforma delle wheel (PEP 425) per ogni piattaforma di
#: mise: servono a `pip download --platform` per mettere nel bundle le
#: dipendenze Python di requirements.txt (ADR-0037) già compilate.
PIATTAFORME_PIP = {
    "linux-x64": ["manylinux_2_28_x86_64", "manylinux_2_17_x86_64", "manylinux2014_x86_64"],
    "linux-arm64": ["manylinux_2_28_aarch64", "manylinux_2_17_aarch64", "manylinux2014_aarch64"],
    "macos-arm64": ["macosx_11_0_arm64", "macosx_12_0_arm64", "macosx_14_0_arm64"],
    "windows-x64": ["win_amd64"],
}


def scarica_ruote(piatt: str, cartella: Path, requisiti: Path = REPO / "requirements.txt",
                  python: str = "3.13") -> None:
    """`pip download` delle wheel di `requisiti` per `piatt`, solo binarie."""
    cmd = [sys.executable, "-m", "pip", "download", "--quiet", "--only-binary=:all:",
           "--python-version", python, "--implementation", "cp", "-d", str(cartella),
           "-r", str(requisiti)]
    for etichetta in PIATTAFORME_PIP[piatt]:
        cmd += ["--platform", etichetta]
    subprocess.run(cmd, check=True)


def _data_zip() -> tuple[int, int, int, int, int, int]:
    import time
    epoch = int(os.environ.get("SOURCE_DATE_EPOCH", "315532800"))  # 1980-01-01
    return time.gmtime(max(epoch, 315532800))[:6]


def costruisci_bundle(piatt: str, uscita: Path, scarica_f=scarica,
                      ruote: Path | None = None) -> Path:
    """Scrive `rumblingstone-strumenti-<piatt>.zip` in `uscita`. Fallisce se uno sha non torna."""
    vv = voci(piatt)
    file: dict[str, bytes] = {}
    for v in vv:
        if not v.url or not v.sha256:
            raise ValueError(f"{v.nome}: mise.lock non ha {piatt}")
        dati = scarica_f(v.url)
        if hashlib.sha256(dati).hexdigest() != v.sha256:
            raise ValueError(f"{v.nome}: sha256 diverso dal lockfile")
        file[f"archivi/{v.url.rsplit('/', 1)[1]}"] = dati
    for p in (TOML, LOCK, Path(__file__).resolve()):  # letti ora: i test li cambiano
        file[p.name] = p.read_bytes()
    if ruote:
        for w in sorted(ruote.glob("*.whl")):
            file[f"ruote/{w.name}"] = w.read_bytes()
    manifest = {
        "piattaforma": piatt,
        "strumenti": [{"nome": v.nome, "versione": v.versione, "backend": v.backend,
                       "archivio": f"archivi/{v.url.rsplit('/', 1)[1]}", "sha256": v.sha256}
                      for v in vv],
        "file": {n: hashlib.sha256(d).hexdigest() for n, d in sorted(file.items())},
    }
    file[BUNDLE_MANIFEST] = (json.dumps(manifest, indent=1, sort_keys=True,
                                        ensure_ascii=False) + "\n").encode()
    uscita.mkdir(parents=True, exist_ok=True)
    zp = uscita / f"rumblingstone-strumenti-{piatt}.zip"
    data = _data_zip()
    with zipfile.ZipFile(zp, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for nome in sorted(file):
            info = zipfile.ZipInfo(f"rumblingstone-strumenti-{piatt}/{nome}", date_time=data)
            info.external_attr = (0o755 if nome.endswith(".py") else 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, file[nome], compresslevel=9)
    return zp


def da_bundle(zp: Path) -> Callable[[str], bytes]:
    """Una `scarica_f` che legge gli archivi dal bundle invece che dalla rete.

    Ogni file si verifica contro BUNDLE.json, e `installa_voce` lo verifica di
    nuovo contro il mise.lock del repo: un bundle di un'altra versione non passa.
    """
    z = zipfile.ZipFile(zp)
    nomi = {Path(n).name: n for n in z.namelist() if "/archivi/" in n}
    manifest_n = next(n for n in z.namelist() if n.endswith("/" + BUNDLE_MANIFEST))
    attesi = json.loads(z.read(manifest_n))["file"]

    def leggi(url: str) -> bytes:
        base = url.rsplit("/", 1)[1]
        if base not in nomi:
            raise OSError(f"{base} non è nel bundle {zp.name}")
        dati = z.read(nomi[base])
        if hashlib.sha256(dati).hexdigest() != attesi.get(f"archivi/{base}"):
            raise OSError(f"{base}: sha256 diverso da BUNDLE.json")
        return dati
    return leggi


def installa_ruote(zp: Path) -> tuple[bool, str]:
    """`pip install --no-index` delle wheel del bundle, verificate contro BUNDLE.json."""
    import tempfile
    with zipfile.ZipFile(zp) as z, tempfile.TemporaryDirectory() as tmp:
        manifest_n = next(n for n in z.namelist() if n.endswith("/" + BUNDLE_MANIFEST))
        attesi = json.loads(z.read(manifest_n))["file"]
        n_ruote = 0
        for n in z.namelist():
            if "/ruote/" in n and n.endswith(".whl"):
                dati = z.read(n)
                rel = "ruote/" + Path(n).name
                if hashlib.sha256(dati).hexdigest() != attesi.get(rel):
                    return False, f"{rel}: sha256 diverso da BUNDLE.json"
                (Path(tmp) / Path(n).name).write_bytes(dati)
                n_ruote += 1
        if not n_ruote:
            return False, "il bundle non ha wheel (costruito senza --con-ruote)"
        r = subprocess.run([sys.executable, "-m", "pip", "install", "--no-index",
                            "--find-links", tmp, "-r", str(REPO / "requirements.txt")])
    return r.returncode == 0, f"{n_ruote} wheel dal bundle, pip uscito con {r.returncode}"


# ── CLI ──────────────────────────────────────────────────────────────────────

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("elenco", help="cosa chiede mise.toml e cosa dice mise.lock")
    e.add_argument("--json", action="store_true")
    e.add_argument("--piattaforma")
    i = sub.add_parser("installa", help="scarica, verifica lo sha256, installa")
    i.add_argument("nomi", nargs="*")
    i.add_argument("--bin", type=Path, help="cartella di destinazione (default .strumenti/)")
    i.add_argument("--github-path", action="store_true",
                   help="aggiunge la cartella bin a $GITHUB_PATH (CI)")
    i.add_argument("--env-file", type=Path,
                   help="scrive `export PATH=...` in questo file (hook di sessione)")
    i.add_argument("--silenzioso", action="store_true")
    i.add_argument("--bundle", type=Path,
                   help="installa senza rete da un rumblingstone-strumenti-<piattaforma>.zip")
    i.add_argument("--con-ruote", action="store_true",
                   help="con --bundle: anche `pip install --no-index` delle wheel del bundle")
    b = sub.add_parser("bundle", help="costruisce i bundle per piattaforma (workflow Release)")
    b.add_argument("--piattaforma", action="append",
                   help="ripetibile; default: lockfile_platforms di mise.toml")
    b.add_argument("--uscita", type=Path, default=Path("dist"))
    b.add_argument("--con-ruote", action="store_true",
                   help="mette nel bundle anche le wheel di requirements.txt (pip download)")
    vf = sub.add_parser("verifica", help="ogni strumento c'è, è quello del lockfile e risponde")
    vf.add_argument("--bin", type=Path)
    vs = sub.add_parser("versione", help="la versione fissata di uno strumento")
    vs.add_argument("nome")
    a = ap.parse_args(argv)

    if a.cmd == "versione":
        try:
            print(versione(a.nome))
        except KeyError as ex:
            print(ex, file=sys.stderr)
            return MANCA
        return 0

    if not TOML.exists() or not LOCK.exists():
        print("mise.toml o mise.lock mancano nella radice del repo", file=sys.stderr)
        return MANCA

    if a.cmd == "elenco":
        vv = voci(a.piattaforma)
        if a.json:
            print(json.dumps([v._asdict() for v in vv], indent=1, ensure_ascii=False))
        else:
            for v in vv:
                stato = "✓" if v.url and v.sha256 else "✗ niente URL/sha256"
                print(f"{v.nome:8} {v.versione:10} {v.backend:22} {stato}")
        return 0 if all(v.url and v.sha256 for v in vv) else MANCA

    if a.cmd == "bundle":
        piatt = a.piattaforma or tomllib.loads(TOML.read_text(encoding="utf-8")).get(
            "settings", {}).get("lockfile_platforms", [piattaforma()])
        import tempfile
        try:
            for p in piatt:
                with tempfile.TemporaryDirectory() as tmp:
                    ruote = None
                    if a.con_ruote:
                        ruote = Path(tmp)
                        scarica_ruote(p, ruote)
                    print(f"✓ {costruisci_bundle(p, a.uscita, ruote=ruote)}")
        except (ValueError, OSError, subprocess.CalledProcessError) as ex:
            print(f"✗ {ex}", file=sys.stderr)
            return 1
        return 0

    dest = (a.bin or DEST).resolve()
    vv = [v for v in voci() if not getattr(a, "nomi", None) or v.nome in a.nomi]
    if a.cmd == "verifica":
        esiti = [verifica_voce(v, dest) for v in vv]
        for _, m in esiti:
            print(m)
        return 0 if all(ok for ok, _ in esiti) else 1

    sorgente = da_bundle(a.bundle) if a.bundle else scarica
    esiti = [installa_voce(v, dest, sorgente) for v in vv]
    for ok, m in esiti:
        if not a.silenzioso or not ok:
            print(("✓ " if ok else "✗ ") + m, file=sys.stdout if ok else sys.stderr)
    bindir = dest / "bin"
    if a.github_path and os.environ.get("GITHUB_PATH"):
        with open(os.environ["GITHUB_PATH"], "a", encoding="utf-8") as f:
            f.write(f"{bindir}\n")
    if a.env_file:
        with open(a.env_file, "a", encoding="utf-8") as f:
            f.write(f'export PATH="{bindir}:$PATH"\n')
    if a.bundle and a.con_ruote and all(ok for ok, _ in esiti):
        esiti.append(installa_ruote(a.bundle))
        print(("✓ " if esiti[-1][0] else "✗ ") + esiti[-1][1])
    if any(not ok for ok, _ in esiti):
        return 1
    if shutil.which(vv[0].nome) not in (None, str(bindir / vv[0].nome)) and not a.silenzioso:
        print(f"  nota: nel PATH c'è anche {shutil.which(vv[0].nome)}; "
              f"gli script del repo usano prima {bindir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
