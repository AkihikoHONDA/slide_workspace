# Third-party components

[English README](README.md) | [日本語README](README.ja.md) | [日本語での要点](#日本語での要点)

## License boundary

The Apache License, Version 2.0 in [LICENSE](LICENSE) applies to the original code and documentation supplied in this repository. It does not relicense external software, services, skills, fonts, input documents, or presentation assets.

The source distribution contains workspace scripts, prompts, templates, tests, and documentation. Dependencies and Anthropic skills are installed separately. Do not add downloaded skill directories, `node_modules/`, `.venv/`, font files, credentials, or private project materials to a public source release without assessing their own terms.

## Anthropic tools and skills

Claude Code and the official `document-skills@anthropic-agent-skills` plugin are obtained from Anthropic's supported installation and plugin mechanisms. This repository does not contain or redistribute the official `pptx` Skill or its helper scripts, and does not modify them during setup.

Anthropic's [skills README](https://github.com/anthropics/skills) distinguishes its document creation/editing skills from the Apache-licensed examples: the document skills are described as **source-available, not open source**. The `pptx` folder has its own [LICENSE.txt](https://github.com/anthropics/skills/blob/main/skills/pptx/LICENSE.txt), which refers to the applicable service agreement and contains additional restrictions. Do not treat a public GitHub location as permission to redistribute or relicense those materials. Refer to the version you actually use and your applicable agreement.

Claude Code authentication, model access, service usage, and any associated charges remain outside this project's Apache-2.0 license. See [Claude Code documentation](https://code.claude.com/docs/en/setup) and Anthropic's [Consumer Terms](https://www.anthropic.com/legal/consumer-terms) or [Commercial Terms](https://www.anthropic.com/legal/commercial-terms), as applicable.

## Separately installed dependencies

| Component group | Use in this workspace | Upstream information |
|---|---|---|
| Node.js and nvm | JavaScript runtime and user-level runtime selection | [Node.js](https://nodejs.org/), [nvm](https://github.com/nvm-sh/nvm) |
| PptxGenJS | Programmatic PowerPoint generation and the synthetic smoke test | [PptxGenJS](https://github.com/gitbrent/PptxGenJS) |
| React, React DOM, React Icons, Sharp | Libraries available to generated presentation code for graphics and image handling | Declared in [package.json](package.json); consult each installed package's license and asset terms |
| Python and Python packages | Document reading, PPTX inspection, image handling, and smoke checks | [Python](https://www.python.org/), [requirements.txt](requirements.txt) |
| LibreOffice Impress | PPTX-to-PDF conversion | [LibreOffice licensing](https://www.libreoffice.org/about-us/licenses/) |
| Poppler | PDF rasterization, text extraction, and font inspection | [Poppler](https://poppler.freedesktop.org/) |
| Ubuntu packages and fonts | System tools, font matching, and Japanese/Latin text rendering | Package copyright/license files under `/usr/share/doc/<package>/` after installation |

This is an inventory of the principal integration points, **not** a complete software bill of materials or an audit of transitive dependencies. Package versions and their notices should be checked in the installation actually used. Icon sets and other bundled assets can have terms different from the surrounding library. Installing a font does not by itself settle redistribution or embedding permissions for that font.

The setup records resolved Python packages and top-level npm dependencies under `.setup/`. Those local records and the generated `package-lock.json` can help identify installed versions. The source ZIP does not include the installed packages themselves.

## Materials and outputs

The synthetic smoke test uses demonstration values only. It is not a template based on a private presentation. User-provided documents, figures, photos, templates, and generated presentations are not automatically licensed under Apache-2.0 because this workspace was used to process them. Their use and redistribution depend on their sources, applicable permissions, and service terms.

## Attribution and affiliation

This is an independent project. It is not affiliated with or endorsed by Anthropic or the Apache Software Foundation. Product and project names identify the tools used; this repository does not grant rights to their trademarks.

The Apache and Anthropic licensing references were reviewed on 2026-10-17. Upstream terms can change; consult the terms that apply to your installed version and use.

## 日本語での要点

このリポジトリのApache-2.0は、ここで配布する独自のコードと文書に適用します。外部ソフトウェア、サービス、Skill、フォント、入力資料を同じライセンスへ変更するものではありません。

公式`pptx` Skillはプラグイン経由で別途導入し、このソース配布物には含めません。Anthropicは文書作成Skillをsource-availableとして区別しており、個別の`LICENSE.txt`とサービス契約・追加制限が適用されます。GitHubで閲覧できることを、自由な再配布・改変の許可とは扱わないでください。

Node.js、Python、PptxGenJS、LibreOffice、Poppler、フォントなどにも、それぞれの条件が適用されます。上の表は主な利用先の案内であり、間接依存を含む完全なライセンス監査ではありません。アイコン集合やフォントの埋め込み・再配布の条件も、利用したものごとに確認が必要です。

案件の原稿、写真、図、テンプレート、生成スライドの権利も別です。本ワークスペースを使っただけで、それらへApache-2.0が自動適用されることはありません。認証・契約・費用は利用者が別途用意します。このプロジェクトはAnthropicやApache Software Foundationの公式・公認プロジェクトではありません。
