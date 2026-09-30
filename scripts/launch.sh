#!/usr/bin/env bash
# Run from the EDA host. --check checks paths only and never launches Virtuoso.
set -euo pipefail
repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ -f "$repo_root/config/local.env" ]]; then
  source "$repo_root/config/local.env"
fi

usage() { printf 'Usage: bash scripts/launch.sh {adc|pll} [--check]\n' >&2; }
if [[ $# -lt 1 || $# -gt 2 ]]; then usage; exit 2; fi
case "$1" in
  adc) package=adc_verification_v5.0_001; workarea=saradc ;;
  pll) package=pll_verification_ws_v1.0_001; workarea=pll_zambezi45 ;;
  *) usage; exit 2 ;;
esac
if [[ $# -eq 2 && "$2" != --check ]]; then usage; exit 2; fi
: "${CADENCE_VERIFICATION_ROOT:?Set CADENCE_VERIFICATION_ROOT in config/local.env}"
: "${CDSHOME:?Set CDSHOME in config/local.env}"
export PROJECT="$(cd -- "$CADENCE_VERIFICATION_ROOT/$package" && pwd)"
export CDSHOME="$(cd -- "$CDSHOME" && pwd)"
export CDS_DB_TYPE=oa
export CDS_SITE="$PROJECT/setup/site"
export CDS_LOAD_ENV=CWD
work_dir="$PROJECT/WORK/$workarea"
virtuoso_bin="$CDSHOME/tools/dfII/bin/virtuoso"
if [[ ! -f "$work_dir/cds.lib" || ! -x "$virtuoso_bin" ]]; then
  printf 'Missing cds.lib or executable: %s | %s\n' "$work_dir/cds.lib" "$virtuoso_bin" >&2
  exit 1
fi
printf 'PROJECT=%s\nWORK=%s\nVIRTUOSO=%s\n' "$PROJECT" "$work_dir" "$virtuoso_bin"
if [[ "${2:-}" == --check ]]; then
  printf 'Path check only; license, models, ADE and simulation are not verified.\n'
  exit 0
fi
cd -- "$work_dir"
exec "$virtuoso_bin" -log CDS.log
