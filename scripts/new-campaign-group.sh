#!/usr/bin/env bash
# new-campaign-group.sh
#
# Helper to start a new campaign with a new player group, preserving
# all preparation material (archs, PNGs, skills, maps) and only
# resetting the "live state" (state.md + sessions/).
#
# Usage:
#   ./scripts/new-campaign-group.sh <new-group-name> [--backup-current <current-group-name>]
#
# Examples:
#   # Backup current group "alpha" and start "beta"
#   ./scripts/new-campaign-group.sh beta --backup-current alpha
#
#   # Just start "beta" (assumes main has the template/previous state)
#   ./scripts/new-campaign-group.sh beta
#
# See: campaign/DM-CAMPAIGN-PLAYBOOK.md §7

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

err() { echo "ERROR: $*" >&2; exit 1; }

# --- parse args ---
NEW_GROUP="${1:-}"
BACKUP_CURRENT=""
if [[ "${2:-}" == "--backup-current" ]]; then
    BACKUP_CURRENT="${3:-}"
    [[ -z "$BACKUP_CURRENT" ]] && err "--backup-current requires a group name"
fi

[[ -z "$NEW_GROUP" ]] && err "Usage: $0 <new-group-name> [--backup-current <current-group-name>]"

# --- sanity checks ---
command -v git >/dev/null || err "git not found"
[[ -d ".git" ]] || err "not a git repo"
# Ogni file di stato PER-GRUPPO deve avere il suo template: se ne manca uno,
# il gruppo nuovo eredita i dati del precedente. È esattamente ciò che è
# successo il 2026-08-05, quando state.yaml e state-changelog.md sono stati
# introdotti senza aggiornare questo script (lotto G2-quater).
for tpl in state-blank.md state-blank.yaml state-changelog-blank.md chronicle-blank.md; do
    [[ -f "campaign/templates/$tpl" ]] || \
        err "campaign/templates/$tpl not found — cannot reset cleanly"
done

# --- check clean working tree ---
if ! git diff-index --quiet HEAD --; then
    err "working tree is not clean — commit or stash first"
fi

echo "==> Current branch: $(git branch --show-current)"
echo "==> New group name: $NEW_GROUP"
[[ -n "$BACKUP_CURRENT" ]] && echo "==> Backup current as: campaign-group-$BACKUP_CURRENT"

read -p "Proceed? [y/N] " CONFIRM
[[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]] && { echo "Aborted."; exit 0; }

# --- backup current group ---
if [[ -n "$BACKUP_CURRENT" ]]; then
    BACKUP_BRANCH="campaign-group-$BACKUP_CURRENT"
    echo "==> Creating backup branch: $BACKUP_BRANCH"
    git checkout -b "$BACKUP_BRANCH"
    echo "==> Pushing backup branch to origin..."
    git push -u origin "$BACKUP_BRANCH" || echo "WARN: push failed — do it manually later"
    git checkout main
fi

# --- create new group branch ---
NEW_BRANCH="campaign-group-$NEW_GROUP"
echo "==> Creating new branch: $NEW_BRANCH"
git checkout -b "$NEW_BRANCH"

# --- reset live state ---
# Regola: tutto ciò che è PARTITA si azzera, tutto ciò che è PRODOTTO resta.
# Prodotto = archi, Bestiario, mappe, skill, premessa di campagna, house rules.
# Partita  = stato, storico, cronaca, sessioni, recap.
echo "==> Resetting campaign/state.md from template..."
cp campaign/templates/state-blank.md campaign/state.md

echo "==> Resetting campaign/state.yaml from template..."
cp campaign/templates/state-blank.yaml campaign/state.yaml

echo "==> Resetting campaign/state-changelog.md from template..."
cp campaign/templates/state-changelog-blank.md campaign/state-changelog.md

echo "==> Resetting campaign/lore/campaign-chronicle.md from template..."
cp campaign/templates/chronicle-blank.md campaign/lore/campaign-chronicle.md
echo "    (campaign-premise.md NON si azzera: è prodotto condiviso)"

echo "==> Clearing campaign/sessions/*.md..."
rm -f campaign/sessions/*.md
touch campaign/sessions/.gitkeep

echo "==> Clearing campaign/recaps/ (recap del gruppo precedente)..."
rm -f campaign/recaps/*.md campaign/recaps/homebrew/*.md 2>/dev/null || true
touch campaign/recaps/.gitkeep

echo "==> Rigenerazione della vista di stato dai dati vuoti..."
python3 scripts/render_state.py || err "render_state fallito — stato non coerente"

echo "==> Verifica: nessun residuo del gruppo precedente..."
python3 scripts/validate_state.py || err "validate_state fallito sul template"

# --- commit ---
git add -A
git commit -m "Campaign group $NEW_GROUP: session 0 (reset from template)"

echo ""
echo "=========================================="
echo "✅ Done. New campaign group '$NEW_GROUP' initialized."
echo ""
echo "Next steps:"
echo "  1. Compila campaign/state.yaml: party, primo villain, confine"
echo "     (NON scrivere le tabelle di state.md: sono generate)"
echo "  2. python3 scripts/render_state.py     # genera le tabelle"
echo "  3. python3 scripts/validate_state.py   # schema + coerenza"
echo "  4. python3 scripts/dm.py session branch --group $NEW_GROUP   # group.yaml"
echo "  5. python3 scripts/state_apply.py --migrate                  # marcatori auto:"
echo "  6. git push -u origin $NEW_BRANCH"
echo "  7. Gioca la sessione 1, poi: python3 scripts/dm.py session end"
echo "=========================================="
