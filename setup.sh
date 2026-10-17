#!/usr/bin/env bash
# Bootstrap shared tools only. Start/resume conversations with the standard claude CLI.
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
fail() { printf '\nERROR: %s\n' "$*" >&2; exit 1; }
info() { printf '\n== %s ==\n' "$*"; }
MODE="${1:-install}"
case "$MODE" in
  -h|--help)
    printf '%s\n' 'Usage: bash setup.sh [--update | --check]' \
      '  引数なし: 共通環境の導入・標準Claude設定の初期値・基本テスト' \
      '  --update: 共通依存とClaude・公式Skillを更新し、基本テスト' \
      '  --check : インストールや設定変更をせず基本テスト・環境記録のみ' \
      '  スクリプト全体にsudoは付けません。aptだけ内部でsudoを使います。'
    exit 0 ;;
  install|--update|--check) [[ $# -le 1 ]] || fail '引数が多すぎます。' ;;
  *) fail '不明な引数です。--helpを参照してください。' ;;
esac
[[ "${EUID:-$(id -u)}" -ne 0 ]] || fail \
  'sudoを付けず通常ユーザーで実行してください。OSパッケージ導入だけ内部でsudoを使用します。'
cd "$ROOT"
mkdir -p .setup/logs .setup/downloads projects
LOG="$ROOT/.setup/logs/setup-$(date +%Y%m%d-%H%M%S)-$$.log"
exec > >(tee -a "$LOG") 2>&1
trap 'rc=$?; printf "\nセットアップ未完了: line=%s exit=%s\nログ: %s\n" "$LINENO" "$rc" "$LOG" >&2; exit "$rc"' ERR
export PATH="$HOME/.local/bin:$PATH"

if [[ "$MODE" != --check ]]; then
  [[ -r /etc/os-release ]] || fail 'Ubuntu環境を使用してください。'
  # shellcheck disable=SC1091
  source /etc/os-release
  [[ "${ID:-}" = ubuntu ]] || fail '自動導入はUbuntu用です（Ubuntu 24.04 LTS推奨）。'
  dpkg --compare-versions "${VERSION_ID:-0}" ge 22.04 || fail 'Ubuntu 22.04以降を使用してください。'

  info '1/6 OSツールと日英フォント'
  sudo -v
  sudo apt-get -o DPkg::Lock::Timeout=120 update
  sudo env DEBIAN_FRONTEND=noninteractive apt-get -o DPkg::Lock::Timeout=120 \
    install -y --no-install-recommends \
    ca-certificates curl git xz-utils build-essential python3 python3-venv python3-pip \
    libreoffice-impress poppler-utils fontconfig fonts-liberation \
    fonts-crosextra-carlito fonts-crosextra-caladea fonts-noto-cjk zip unzip
  fc-cache -f

  info '2/6 Node.js: nvmとLTS版'
  export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
  if [[ ! -s "$NVM_DIR/nvm.sh" ]]; then
    NVM_TAG=v0.40.6  # Official nvm README checked 2026-10-17.
    curl --proto '=https' --tlsv1.2 -fSL --retry 3 --connect-timeout 20 \
      "https://raw.githubusercontent.com/nvm-sh/nvm/$NVM_TAG/install.sh" \
      -o .setup/downloads/install-nvm.sh
    touch "$HOME/.bashrc"
    PROFILE="$HOME/.bashrc" bash .setup/downloads/install-nvm.sh
  fi
  set +u
  # shellcheck disable=SC1091
  source "$NVM_DIR/nvm.sh" --no-use
  # Normal reruns retain the existing usable default. Explicit update selects current LTS.
  if [[ "$MODE" = --update ]] || ! nvm use --silent default || \
    ! node -e 'if (process.platform !== "linux" || +process.versions.node.split(".")[0] < 22) process.exit(1)'; then
    nvm install --lts --no-progress
    nvm alias default 'lts/*'
    nvm use --silent default
  fi
  set -u

  info '3/6 共通Python・JavaScriptライブラリ'
  [[ -d .venv ]] || python3 -m venv .venv
  PIP_ARGS=(install -r "$ROOT/requirements.txt")
  [[ "$MODE" != --update ]] || PIP_ARGS+=(--upgrade)
  "$ROOT/.venv/bin/python" -m pip "${PIP_ARGS[@]}"
  "$ROOT/.venv/bin/python" -m pip check
  if [[ "$MODE" = --update ]]; then
    npm update --no-audit --no-fund
  else
    npm install --no-audit --no-fund
  fi

  info '4/6 Claude Codeと公式document-skills（userスコープ）'
  if ! command -v claude >/dev/null 2>&1 || [[ "$(command -v claude)" = /mnt/[a-z]/* ]]; then
    curl --proto '=https' --tlsv1.2 -fSL --retry 3 --connect-timeout 20 \
      https://claude.ai/install.sh -o .setup/downloads/install-claude.sh
    bash .setup/downloads/install-claude.sh stable
    hash -r
  elif [[ "$MODE" = --update ]]; then
    claude update
  fi
  # Native CLI on a fresh interactive terminal; no venv activation or CLI alias.
  PATH_LINE='export PATH="$HOME/.local/bin:$PATH"'
  touch "$HOME/.bashrc"
  grep -Fqx "$PATH_LINE" "$HOME/.bashrc" || printf '\n%s\n' "$PATH_LINE" >> "$HOME/.bashrc"
  claude --version
  claude plugin marketplace list > .setup/marketplaces.txt
  if ! grep -Fq 'anthropic-agent-skills' .setup/marketplaces.txt; then
    claude plugin marketplace add anthropics/skills
  elif [[ "$MODE" = --update ]]; then
    claude plugin marketplace update anthropic-agent-skills
  fi
  claude plugin list > .setup/plugins.txt
  if ! grep -Fq 'document-skills@anthropic-agent-skills' .setup/plugins.txt; then
    claude plugin install document-skills@anthropic-agent-skills --scope user
  elif [[ "$MODE" = --update ]]; then
    claude plugin update document-skills@anthropic-agent-skills --scope user
  fi
  claude plugin enable document-skills@anthropic-agent-skills --scope user
  claude plugin list > .setup/plugins.txt

  info '5/6 Claude標準のユーザー設定を初期化'
  python3 "$ROOT/scripts/configure_claude.py"
  echo '設定済みの項目は保持します。以後の変更先は ~/.claude/settings.json です。'
  echo '新規環境の初期値: Opus / High / auto。組織の制限や初回認証は別途適用されます。'
fi

# This block prepares the bootstrap's own commands, not the user's future shell.
# Direct claude sessions get absolute interpreter paths from CLAUDE.md imports.
if [[ -s "${NVM_DIR:-$HOME/.nvm}/nvm.sh" ]]; then
  export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
  set +u
  # shellcheck disable=SC1091
  source "$NVM_DIR/nvm.sh" --no-use
  nvm use --silent default
  set -u
fi
node -e 'if (process.platform !== "linux" || +process.versions.node.split(".")[0] < 22) process.exit(1)'
[[ -x "$ROOT/.venv/bin/python" ]] || fail '共通.venvがありません。引数なしのsetup.shを実行してください。'
PY="$ROOT/.venv/bin/python"
NODE="$(command -v node)"
info '6/6 合成データで基本動作確認'
"$PY" -c 'import pptx, pypdf, PIL, lxml, defusedxml, markitdown'
node -e 'for (const m of ["pptxgenjs","sharp","react","react-dom","react-icons"]) require(m)'
"$PY" -m pip check
TESTDIR="$ROOT/.setup/smoke-$(date +%Y%m%d-%H%M%S)-$$"
mkdir -p "$TESTDIR"
node "$ROOT/scripts/smoke_test.cjs" "$TESTDIR"
"$PY" "$ROOT/scripts/check_smoke.py" pptx "$TESTDIR/smoke.pptx"
PROFILE_URI="$("$PY" -c 'from pathlib import Path; import sys; print(Path(sys.argv[1]).resolve().as_uri())' "$TESTDIR/lo-profile")"
timeout 120 soffice "-env:UserInstallation=$PROFILE_URI" --headless \
  --convert-to pdf --outdir "$TESTDIR" "$TESTDIR/smoke.pptx"
[[ -s "$TESTDIR/smoke.pdf" ]] || fail 'PDFが出力されませんでした。'
pdftoppm -r 100 -png "$TESTDIR/smoke.pdf" "$TESTDIR/slide"
pdftotext "$TESTDIR/smoke.pdf" "$TESTDIR/smoke.txt"
pdffonts "$TESTDIR/smoke.pdf" > "$TESTDIR/pdf-fonts.txt"
"$PY" "$ROOT/scripts/check_smoke.py" pdf "$TESTDIR/smoke.pdf"
"$PY" -m pip freeze > .setup/python-resolved.txt
npm ls --depth=0 --json > .setup/npm-resolved.json
{
  date -Iseconds
  printf 'workspace=%s\n' "$ROOT"
  node --version; npm --version; "$PY" --version; claude --version
  soffice --version
  fc-match Calibri; fc-match Cambria; fc-match 'Noto Sans CJK JP:lang=ja'
} > .setup/environment.txt
printf '%s\n' "$TESTDIR" > .setup/latest-smoke-dir.txt
"$PY" - "$ROOT" "$NODE" <<'PY'
from pathlib import Path
import shlex
import sys
root = Path(sys.argv[1]).absolute()
node = Path(sys.argv[2]).absolute()
python = root / '.venv/bin/python'
markitdown = root / '.venv/bin/markitdown'
# The known venv path must not be resolved through its interpreter symlink:
# doing so would turn it into the system Python and bypass venv packages.
path_prefix = str(root / '.venv/bin') + ':' + str(node.parent)
text = f'''# 共通の実行環境（setup.shで生成）

ワークスペース: `{root}`
Python: `{python}`
MarkItDown: `{markitdown}`
Node.js: `{node}`
JavaScriptライブラリ: `{root / 'node_modules'}`
版の記録: `{root / '.setup/environment.txt'}`
基本テストの場所: `{root / '.setup/latest-smoke-dir.txt'}`

Pythonのactivateは不要です。上記のvenv内Pythonをそのパスのまま実行してください。
シンボリックリンク先のシステムPythonへ置き換えないでください。

案件の `work/` にある生成コードを実行する例:
```bash
{shlex.quote(str(python))} work/check.py
{shlex.quote(str(node))} work/make_slides.cjs
```

複数ツールや子プロセスが `python` / `node` を名前で起動する場合は、
そのBash呼出し内で次を設定できます。利用者に毎回実行させる必要はありません。
```bash
export PATH={shlex.quote(path_prefix)}:"$PATH"
```

共通node_modulesは、案件内のJavaScriptファイルからNodeの通常の親ディレクトリ探索で参照できます。
ライブラリ追加は共通環境と依存定義へ反映し、OSのPythonへpip installしないでください。
setupの基本テストは、実スライドの視覚品質や公式Skill検査の合格を意味しません。
'''
(root / '.setup/ENVIRONMENT.md').write_text(text, encoding='utf-8')
PY
info '共通環境の準備完了'
printf 'テスト: %s\nログ: %s\n' "$TESTDIR" "$LOG"
echo '新しいターミナルを開くとClaude・nvmのPATH設定が反映されます。'
echo '次: bash new-project.sh my-talk → 条件と資料を用意 → cd projects/my-talk → claude'
echo '再開: 同じ案件フォルダで claude --resume または claude --continue'
