# Release verification — 3.1.0

[English README](README.md) | [日本語README](README.ja.md)

Date: 2026-10-17. This is a verification record for the source package, not a claim of a successful clean Ubuntu/WSL deployment or authenticated Claude production run.

## Scope of this release

This release adds publication documentation, licensing, metadata, Git exclusions, and publication tests. A byte-for-byte comparison with the supplied 3.0.0 archive confirmed that `setup.sh`, `new-project.sh`, the three existing files in `scripts/`, `tests/test_workspace.py`, `CLAUDE.md`, `MAKE_SLIDES.md`, `START_PROMPT.md`, `requirements.txt`, and the entire `project-template/` were preserved. The `package.json` dependency ranges are unchanged; its version and license metadata changed.

No Anthropic Skill files or other third-party implementation files were copied into the release. The Apache-2.0 license text is the complete, unmodified standard English text, including its application appendix. Its SHA-256 is `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`. It was copied from the environment's standard license text and reviewed against the Apache Software Foundation's published text, not downloaded by the setup script. The copyright attribution uses the project-level label “Slide Workspace contributors”; no personal name or email was added.

## Offline regression and publication tests

```bash
python3 -m unittest discover -s tests -v
```

**Result: 22 tests passed (14 existing workspace tests and 8 publication tests).** The runner was Linux and ran as root, so the test that deliberately checks setup's root refusal was exercised. No real installation, `sudo`, account login, model call, or repository push was performed by these tests. Temporary Git repositories are used only to inspect ignore behavior; there are no commits or remotes.

The existing tests cover shell syntax, rejection of root setup, absence of obsolete launchers, policy imports, project creation and non-overwrite behavior, invalid project names, paths containing spaces/Japanese text, and native Claude settings generation. They also cover idempotence, preserving prior settings, backups, invalid JSON, and the absence of additional bypass/environment/hook settings.

The new tests cover reciprocal README language links, matching Bash/JSON examples in both READMEs, existence of relative Markdown link destinations, required publication files, complete Apache-2.0 text, consistent version/license metadata, and actual Git exclusion behavior. External URLs and GitHub-rendered anchors are not validated by that offline link test. Test cases confirm that private/local files are ignored while shared `CLAUDE.md`, the template, and `projects/.gitkeep` remain trackable.

## Synthetic document smoke check

Using the preinstalled tools in the verification environment, the unchanged `scripts/smoke_test.cjs` and `scripts/check_smoke.py` were executed. The following passed: two-slide PPTX creation; ZIP integrity; notes on both slides; a native-chart XML part; LibreOffice conversion to a two-page PDF; two PNG renders through Poppler; and extractable Japanese text. Both PNGs were visually inspected, with no obvious missing Japanese glyphs, clipping, or unintended overlaps.

| Component | Version used for this check |
|---|---|
| OS | Debian GNU/Linux 13 |
| Node.js | 22.16.0 |
| Python | 3.13.5 |
| PptxGenJS | 4.0.0 |
| python-pptx | 1.0.2 |
| pypdf | 5.9.0 |
| LibreOffice | 25.2.3.2 |
| Poppler | 25.06.0 |

**This is not a fresh install of the declared dependencies.** The smoke check used preinstalled packages; in particular, the test PptxGenJS was 4.0.0 while `package.json` still requests `^4.0.1`. It does not validate that dependency range, the online installers, or the complete `setup.sh` path. The smoke artifacts and installed libraries are not included in the source ZIP.

## Archive and publication checks

The archive contains the source tree, documentation, complete license, tests, and empty project placeholders only. The release has no `.git` history, `.venv`, `node_modules`, `.setup`, working presentation projects, images, fonts, or credentials. The source text was checked for personal/project-specific identifiers from the supplied material and common credential patterns; none were found. This inspection does not cover files later added on a user's machine or Git commit metadata, and is not a guarantee against every possible secret format.

`CHECKSUMS.sha256` covers every distributed file other than the checksum file itself. It can be checked from the extracted `slide-workspace/` directory:

```bash
sha256sum -c CHECKSUMS.sha256
```

The final ZIP was checked for integrity and safe relative entry paths. Local Markdown destinations and the Bash syntax were checked again after packaging.

## Not verified

A clean Ubuntu/WSL installation of apt packages, nvm, the selected LTS runtime, all Python/npm dependencies, Claude Code, and the official plugin has not been tested end to end. Network restrictions in this verification environment prevented ordinary external downloads; existing tools were used instead. No inference is made about whether those upstream packages or services are unavailable on the user's machine.

Claude authentication, effective user settings, parent `CLAUDE.md` loading in a live session, availability of `auto` mode, and presentation generation through the official Skill were not tested. Windows PowerPoint rendering/editing, official Skill OOXML validation, research correctness, organizational proxy configuration, and OS-version-specific package behavior are outside this verification.

This release intentionally does not change those setup mechanisms or relax security settings. Author review, permitted source materials, ordinary permission checks, and organization policies remain necessary.

## 日本語での要約

3.0.0から実行スクリプト・制作方針・案件ひな型・依存範囲を変えず、英日README、Apache-2.0、第三者ライセンスの説明、公開用の除外設定とテストを追加しました。既存14件と追加８件の計22テストは通過しています。

既存Linux環境のライブラリで、合成データによるPPTX・ノート・グラフ・PDF化・画像化・日本語抽出を確認し、２枚の描画も確認しました。配布版の依存を新規導入した試験ではなく、PptxGenJSの実測版も依存定義の指定範囲とは異なります。

新規Ubuntu/WSLへの全導入、実Claudeの認証・設定読込み・制作、Windows PowerPointの実動作は未検証です。公開用ZIPには個人・研究案件の資料、フォント本体、認証情報、導入済みライブラリを含めていませんが、利用者が後から追加するファイルやGitのコミット情報は別途確認が必要です。
