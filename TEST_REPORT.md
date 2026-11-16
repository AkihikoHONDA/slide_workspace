# Release verification — 3.2.0

[English README](README.md) | [日本語README](README.ja.md)

Date: 2026-11-16. This is a verification record for the source package, not a claim of a successful clean Ubuntu/WSL deployment or authenticated Claude production run.

## Scope of this release

This release changes the production policy and its documentation only. Compared with the 3.1.0 commit, the changed files are `MAKE_SLIDES.md`, `README.md`, `README.ja.md`, `CHANGELOG.md`, `VERSION`, the version field of `package.json`, this report, and `CHECKSUMS.sha256`. `setup.sh`, `new-project.sh`, `scripts/`, `tests/`, `CLAUDE.md`, `START_PROMPT.md`, `requirements.txt`, the `package.json` dependency ranges, and the entire `project-template/` are unchanged, as confirmed with `git diff` against the 3.1.0 commit.

`MAKE_SLIDES.md` now separates short core drafting rules from a draft–render–review loop and a viewpoint-based review checklist. It also contains the maintainer's own presenter settings (measured speaking rate, hard-to-say words, and how to make Even G2 teleprompter files on request). Users of this workspace should replace or remove that section for their own use.

## Offline regression and publication tests

```bash
python3 -m unittest discover -s tests -v
```

**Result: 22 tests ran; 21 passed and 1 was skipped.** The runner was Linux (WSL2) as a non-root user, so the test that checks setup's refusal to run as root was skipped. No real installation, `sudo`, account login, model call, or repository push was performed by these tests.

## Synthetic document smoke check

Not re-run for this release. The smoke scripts, setup, and dependency ranges are unchanged from 3.1.0; see the 3.1.0 record in the Git history for that check and its limits.

## Not verified

The new review loop has not been measured for its effect on quality or token use. A clean Ubuntu/WSL installation, Claude authentication, live loading of the parent `CLAUDE.md`, presentation generation through the official Skill, and Windows PowerPoint behavior were not tested for this release.

## 日本語での要約

3.1.0から変えたのは制作方針（`MAKE_SLIDES.md`）と、その説明（README、CHANGELOG）、版情報、この記録、チェックサムだけです。セットアップ、案件作成、スクリプト、テスト、案件ひな型、依存範囲は変えていません。

`MAKE_SLIDES.md` は、作るときの核ルール、作って見直す進め方、観点別の見直しチェックリストに分かれました。また、管理者自身の発表者向けの設定（話す速さ、言いにくい語、Even G2用ファイルの作り方）を含みます。ほかの人が使う場合は、この節を自分用に書き換えるか削除してください。

テストは22件のうち21件が通過し、1件はroot以外で実行したため省略されました。基本動作確認（スモークテスト）は、関係するスクリプトに変更がないため再実行していません。新しい見直しの進め方が品質やトークン使用量に与える影響は、まだ測っていません。
