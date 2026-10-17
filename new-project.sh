#!/usr/bin/env bash
# Create files only. Conversation lifecycle belongs to the standard Claude CLI.
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
usage() {
  printf '%s\n' 'Usage: bash new-project.sh PROJECT' \
    '  projects/PROJECT/ に条件ひな型と空の入出力フォルダを作成します。' \
    '  Claudeの起動・ログイン・会話再開・環境準備は行いません。'
}
if [[ $# = 0 || "${1:-}" = --help || "${1:-}" = -h ]]; then usage; exit 0; fi
[[ $# = 1 ]] || { usage >&2; exit 2; }
NAME="$1"
[[ "$NAME" =~ ^[a-zA-Z0-9][a-zA-Z0-9_-]*$ ]] || {
  printf 'ERROR: 案件名は英数字で始まる英数字・ハイフン・アンダースコアにしてください。\n' >&2
  exit 2
}
PROJECT="$ROOT/projects/$NAME"
mkdir -p "$ROOT/projects"
# Deliberately no -p: an existing project must never be overwritten.
mkdir "$PROJECT" || {
  printf 'ERROR: 作成できませんでした。既存案件の再開は、そのフォルダで claude --resume を使用してください。\n' >&2
  exit 1
}
cp -R "$ROOT/project-template/." "$PROJECT/"
mkdir -p "$PROJECT/inputs/assets" "$PROJECT/work" "$PROJECT/outputs"
printf '作成しました: %s\n' "$PROJECT"
printf 'talk-brief.mdを記入し、inputs/へ資料を置いてください。\n\n'
printf '制作開始:\n  cd %q\n  claude\n\n' "$PROJECT"
printf '最初の依頼例: talk-brief.mdとinputs/に基づいて、初稿の制作と検査を最後まで進めてください。\n'
