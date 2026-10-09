#!/usr/bin/env bash
# setup-distrobox.sh — one-time setup of a GPU-enabled Distrobox for ComfyUI.
# Bazzite: distrobox and podman are preinstalled. Debian/Ubuntu: install them
# first (sudo apt install distrobox podman). Keeps the toolchain OUT of the host.
# Standard Distrobox + ComfyUI commands (see README.md for official sources).
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/comune.sh"

for c in distrobox podman; do
  command -v "$c" >/dev/null 2>&1 || {
    echo "ERRORE: $c non trovato. Su Debian/Ubuntu: sudo apt install distrobox podman" >&2
    echo "        (su Bazzite sono preinstallati)." >&2; exit 1; }
done

if ! nvidia-smi >/dev/null 2>&1; then
  echo "AVVISO: nvidia-smi non risponde sull'host: il box non vedrà la GPU." >&2
  echo "        Su Debian serve il driver NVIDIA proprietario (pacchetto nvidia-driver)." >&2
fi

echo "==> 0/4 installo in $DEST"
spazio_libero "$DEST" 15 || [ "${COMFYUI_FORZA:-}" = 1 ] || {
  echo "        (oppure COMFYUI_FORZA=1 per procedere lo stesso)" >&2; exit 1; }

echo "==> 1/4 creo il box '$BOX' (Ubuntu 24.04 + driver NVIDIA dell'host)"
distrobox create --name "$BOX" --image ubuntu:24.04 --nvidia --yes || true

echo "==> 2/4 installo git/python nel box"
distrobox enter "$BOX" -- bash -lc '
  set -e
  sudo apt-get update -qq
  sudo apt-get install -y -qq git python3-venv python3-pip
'

if [ ! -d "$DEST/.git" ]; then
  echo "==> 3/4 clono ComfyUI (ufficiale) in $DEST"
  mkdir -p "$(dirname "$DEST")"
  git clone https://github.com/comfyanonymous/ComfyUI.git "$DEST"
else
  echo "==> 3/4 ComfyUI già presente, aggiorno"
  git -C "$DEST" pull --ff-only || true
fi

echo "==> 4/4 virtualenv + PyTorch CUDA + requirements (nel box)"
distrobox enter "$BOX" -- bash -lc "
  set -e
  cd '$DEST'
  [ -d venv ] || python3 -m venv venv
  . venv/bin/activate
  pip install --upgrade pip
  pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
  pip install -r requirements.txt
  python -c 'import torch; print(\"    GPU vista da torch:\", torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"\")'
"

echo
echo "OK. Ora i pesi:  scripts/comfyui-local/scarica-pesi.sh"
echo "poi avvia con:   scripts/comfyui-local/start.sh"
