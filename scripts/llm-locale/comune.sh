#!/usr/bin/env bash
# comune.sh — impostazioni comuni di setup/scarica-modello/start/stop/prova.
# Stessa architettura di scripts/comfyui-local/: un Distrobox con la GPU
# dell'host, niente sull'OS immutabile di Bazzite, i dati dove dice LLM_DIR.
#   LLM_DIR    dove stanno i modelli (default: scripts/llm-locale/dati, gitignorato)
#   LLM_BOX    nome del box (default: llm-locale)
#   LLM_PORTA  porta del server (default: 11434, quella di Ollama)
#   LLM_CTX    contesto in token (default: 24576: le skill ne chiedono ~19.000)
BOX="${LLM_BOX:-llm-locale}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RADICE="$(cd "$HERE/../.." && pwd)"
DEST="${LLM_DIR:-$HERE/dati}"
PORTA="${LLM_PORTA:-11434}"
CTX="${LLM_CTX:-24576}"
URL="http://127.0.0.1:$PORTA/v1"

spazio_libero() {
  local dir="$1" serve="$2" su
  su="$dir"; while [ ! -d "$su" ]; do su="$(dirname "$su")"; done
  local liberi; liberi=$(df -Pk "$su" | awk 'NR==2{print int($4/1048576)}')
  if [ "$liberi" -lt "$serve" ]; then
    echo "AVVISO: $liberi GB liberi in $su, ne servono ~$serve." >&2
    echo "        Scegli un altro disco:  export LLM_DIR=/srv/llm" >&2
    return 1
  fi
  echo "    spazio: $liberi GB liberi in $su (servono ~$serve)"
}

# consiglia: il modello che sta su questa macchina, da VRAM e RAM totale.
# Le misure sono quelle dei tag di ollama.com/library/gemma4 (2026-10-10):
# e4b-it-qat 6,1 GB · 12b-it-qat 7,2 GB · 26b (MoE, 3,8 miliardi attivi)
# 16-19 GB. Tutti Apache 2.0. Ollama mette in GPU quello che ci sta e il resto
# in RAM. ADR-0089.
consiglia() {
  local vram ram
  vram=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1)
  vram=$(( ${vram:-0} / 1024 ))
  ram=$(awk '/MemTotal/{print int($2/1048576)}' /proc/meminfo)
  if [ "$ram" -ge 30 ]; then echo "gemma4:26b"        # Dell: esperti in RAM
  elif [ "$vram" -ge 10 ]; then echo "gemma4:12b-it-qat"
  else echo "gemma4:e4b-it-qat"                        # 4-8 GB di GPU
  fi
}
