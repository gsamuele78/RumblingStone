#!/usr/bin/env bash
# Banco della trascrizione (ADR-0135): audio NON personale, fuori dal repo.
# Uso: banco.sh WHISPER_DIR LAVORO_DIR
#   WHISPER_DIR: whisper.cpp compilato, con models/ggml-large-v3-turbo-q5_0.bin
#   LAVORO_DIR:  cartella fuori dal repo per audio e trascrizioni
# Serve un venv con `pip install piper-tts` attivo (voce it_IT-paola-medium, CC0).
set -euo pipefail
W="$1"; L="$2"; QUI="$(cd "$(dirname "$0")" && pwd)"; REPO="$QUI/../../.."
mkdir -p "$L" && cd "$L"
V=https://huggingface.co/rhasspy/piper-voices/resolve/main/it/it_IT/paola/medium
for f in it_IT-paola-medium.onnx it_IT-paola-medium.onnx.json; do [ -f "$f" ] || curl -sLO "$V/$f"; done
python -m piper -m it_IT-paola-medium.onnx -f finta.wav < "$QUI/copione.txt"
ffmpeg -v error -y -i finta.wav -ar 16000 -ac 1 -c:a pcm_s16le pulita16.wav
ffmpeg -v error -y -i finta.wav -filter_complex \
  "anoisesrc=color=pink:amplitude=0.06:d=81[n];[0:a]aecho=0.8:0.6:40|70:0.3|0.2[e];[e][n]amix=inputs=2:duration=first:normalize=0,aresample=16000" \
  -ac 1 -c:a pcm_s16le rumorosa16.wav
P=$(cd "$REPO" && python3 -c "import sys;sys.path.insert(0,'scripts');import transcribe_session as t;print(t.prompt_dei_nomi(t.nomi_della_campagna()))")
for f in pulita16 rumorosa16; do
  "$W/build/bin/whisper-cli" -m "$W/models/ggml-large-v3-turbo-q5_0.bin" -l it -f $f.wav -otxt -of $f-senza -np
  "$W/build/bin/whisper-cli" -m "$W/models/ggml-large-v3-turbo-q5_0.bin" -l it -f $f.wav -otxt -of $f-nomi -np --prompt "$P"
  for v in senza nomi; do
    echo "== $f $v"; python3 "$REPO/scripts/transcribe_session.py" misura $f-$v.txt "$QUI/copione-riferimento.txt"
  done
done
