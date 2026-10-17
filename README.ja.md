# Slide Workspace

[English](README.md) | **日本語**

**Claude CodeとAnthropic公式`pptx` Skillを使い、編集可能なPowerPoint初稿を作るためのワークスペースです。** ツールを一度セットアップし、資料・条件・成果物を案件ごとに整理します。制作と修正には、通常のClaude Codeを使います。

自動化するのは環境構築であり、スライドの構成や配置を固定するものではありません。共通の制作方針で、目的・根拠・結論のつながり、内容に合う画面、後から手編集しやすい説明材料を求めます。編集可能なPPTX、確認用PDF、発表者ノート、短い実行記録を作成する運用です。

**対象環境：** Ubuntu 22.04以降（WSL2上のUbuntuを含む）。導入の基準はUbuntu 24.04 LTSです。**検証状況：** 実験的な配布物であり、新規PCへの全導入と実Claudeの認証から制作までの通し実行は未検証です。[検証状況](#検証状況)を参照してください。

**言語：** この日本語READMEと[英語README](README.md)を用意しています。制作プロンプト・案件ひな型・一部の端末メッセージは日本語のままです。スライドとノートの言語は、案件ごとの`talk-brief.md`で指定できます。

Anthropicとの提携・公式認定を示すものではない独立プロジェクトです。独自のコードと文書には[Apache-2.0](LICENSE)を適用し、別途導入するツールとSkillにはそれぞれの条件が適用されます。[第三者コンポーネント](THIRD_PARTY.md#日本語での要点)も確認してください。

## インストール前の確認

実行前に[setup.sh](setup.sh)を確認してください。OSパッケージを`sudo`で導入し、共通のPython環境とNode.jsライブラリを用意し、Claude Codeを導入または再利用し、公式document-skillsプラグインをユーザー共通で導入・有効化します。シェルの初期化ファイルを変更し、Claudeの**ユーザー共通設定**へモデル・推論・権限の**未設定項目だけ**を追加します。スライド以外のClaudeプロジェクトにも影響する設定で、既存値は保持します。

Ubuntuと、`sudo`を使える通常ユーザーを先に用意してください。設定されたパッケージ配布元・公式インストーラーへ接続できるネットワークと、適切なアカウントまたはプロバイダー設定によるClaude Codeの利用権限が必要です。Claudeの利用契約・費用は、このリポジトリとは別です。WSL・Ubuntuの導入、本人のログイン、信頼確認、組織の承認は自動化しません。Windowsネイティブ版やmacOS用のインストーラーではありません。

入力するのは、利用先モデルへ送信してよい資料だけにしてください。ローカルに置くことやGitの除外設定は、資料がPC外へ出ないことを意味しません。

## クイックスタート

### 1．共通ツールを準備する

リポジトリをcloneするか、ソースZIPを展開し、`~/Workspace/slide-workspace`など、通常ユーザーが所有するLinux側のフォルダへ置きます。`setup.sh`があるフォルダで実行してください。

```bash
bash setup.sh
```

**スクリプト全体に`sudo`は付けません。** OSパッケージの導入だけ内部で管理者権限を使います。完了したら、シェル初期化設定を反映するため新しいターミナルを開いてください。本人のログインは最初のClaude起動時に行い、認証情報をこのリポジトリへ保存しないでください。

### 2．案件を作る

ワークスペース直下で実行します。

```bash
bash new-project.sh my-talk
```

`projects/my-talk/talk-brief.md`へ、題名、用途、聴衆、言語、時間、セッション・会議の文脈、謝辞、テンプレートなどを記入します。資料は`projects/my-talk/inputs/`、図や写真はその中の`assets/`へ置きます。入力のファイル名は固定ではありません。複数資料の役割・優先順位も条件ファイルで指定してください。

ひな型の初期値は日本語スライド・謝辞掲載ありです。今回の資料に合わせて変更してください。`new-project.sh`はファイルを作るだけで、Claudeの起動や既存案件の上書きはしません。案件名は英数字で始め、英数字・ハイフン・アンダースコアを使えます。

### 3．Claudeを起動して初稿を依頼する

```bash
cd projects/my-talk
claude
```

会話欄へ、例えば次を送ってください。

```text
talk-brief.mdとinputs/に基づいて、初稿の制作と検査を最後まで進めてください。
```

親フォルダの`CLAUDE.md`が共通方針と実行ファイルのパスを、案件の`CLAUDE.md`が今回の条件を参照します。専用ランチャーや、利用者による毎回のPython環境のactivateは不要です。ただし、CLAUDE.mdはClaudeへの指示であり、技術的な強制境界ではありません。初回は読み込まれた文脈と有効設定を確認してください。

同じ案件フォルダから、同梱の開始指示を標準CLIで渡す方法も使えます。

```bash
claude "$(cat ../../START_PROMPT.md)"
```

このコマンドと会話欄への依頼は、どちらか一方で十分です。`claude`だけで起動しても、勝手にスライド制作は始まりません。

### 4．確認・修正する

初稿の標準出力は`outputs/talk-r01.pptx`と、対応するPDF、`speaker-notes-r01.md`、`run-info-r01.md`です。ファイル名のprefixは案件条件で変更できます。生成コードと加工素材は`work/`へ保存します。

同じ会話へ修正を依頼するか、案件フォルダから再開します。

```bash
claude --resume
```

会話を選ばず、そのフォルダの直近の会話を続ける場合はこちらです。

```bash
claude --continue
```

改版前のファイルは保存してください。PowerPointで手編集した後は、最新の編集元をClaudeへ明示し、古いコードから再生成して変更を失わないようにします。案件ファイルを別PCへコピーしても、Claudeの会話履歴が自動的に移るわけではありません。

## フォルダ構成

```text
slide-workspace/
├── README.md / README.ja.md
├── LICENSE / NOTICE / THIRD_PARTY.md
├── setup.sh                 # 共通環境の導入・更新・基本テスト
├── new-project.sh           # 任意の案件作成。Claudeは起動しない
├── CLAUDE.md                # 共通方針と環境の参照
├── MAKE_SLIDES.md           # 再利用する制作方針
├── START_PROMPT.md          # 任意の開始依頼文
├── requirements.txt
├── package.json
├── package-lock.json        # セットアップ時にnpmが生成
├── .venv/                   # 共通Python依存。Git管理しない
├── node_modules/            # 共通Node.js依存。Git管理しない
├── .setup/                  # ローカルパス・ログ・基本テスト。Git管理しない
├── scripts/ / tests/
├── project-template/
└── projects/                # 案件資料。Git管理しない
    └── my-talk/
        ├── CLAUDE.md
        ├── talk-brief.md
        ├── inputs/
        ├── work/
        └── outputs/
```

配布物には、発表資料・認証情報・導入済みライブラリ・フォント本体・AnthropicのSkillファイルを含めません。全案件で一つの`.venv`と`node_modules`を共用します。Nodeの親ディレクトリ探索で共通依存を参照できるよう、案件の生成コードは`projects/`の下で運用してください。

## 設定とカスタマイズ

### 制作方針

共通の好みは[MAKE_SLIDES.md](MAKE_SLIDES.md)、用途・聴衆・資料・制約は案件の`talk-brief.md`で変更します。標準の方針は、後から削って仕上げやすい初稿を求め、根拠となる図や説明のつながりを残し、配置は内容に合わせてClaudeへ任せるものです。14〜16 ptも適宜使い、重要な情報の読みやすさを優先します。全ページに同一の配置やタイトル形式を強制しません。

この版では、制作プロンプトとひな型は日本語の一系統を維持しています。READMEの変更は制作指示を変更しません。稼働中の会話へ方針や案件条件の変更を反映するときは、読み直しを依頼してください。

### Claudeの設定

setupは`~/.claude/settings.json`、または`CLAUDE_CONFIG_DIR`で指定された設定ディレクトリへ、次の未設定値だけを補います。既存ファイルを変更する場合はバックアップを残します。

```json
{
  "model": "opus",
  "effortLevel": "high",
  "permissions": {
    "defaultMode": "auto"
  }
}
```

これは**ユーザー共通設定**です。ClaudeのCLI指定、環境変数、プロジェクト設定、組織の管理設定が優先される場合があります。`opus`は更新され得る別名なので、特定の版が必要な場合は利用可能な実モデルIDを指定してください。`/status`で設定、`/model`でモデル、`/context`で読み込まれた指示を確認できます。

`auto`は権限検査の全面解除ではなく、利用可否はClaudeの環境や組織方針に依存します。使えない場合は標準設定で`acceptEdits`を選ぶか、そのセッションだけ次のように起動します。

```bash
claude --permission-mode acceptEdits
```

### 実行ファイルのパス

setupは絶対パスを`.setup/ENVIRONMENT.md`へ記録します。Claudeには`.venv/bin/python`の直接実行と、記録されたLinux側Node.jsの利用を指示します。子プロセスが`python`や`node`を名前で呼ぶ場合は、そのコマンド内でPATHを補う必要があります。このワークスペースは、独自のCLI alias、venvの常時activate、セッション起動フックを追加しません。

## 保守

制作中のセッションを閉じ、ワークスペース直下で更新します。

```bash
bash setup.sh --update
```

依存定義の範囲内の共通ライブラリ、選択するNode.js LTS、Claude Code、公式プラグインを更新し、基本テストと環境記録をやり直します。OSのディストリビューション更新、sudoersの変更、TLS検証の無効化はしません。共通環境の更新は全案件に影響し、完全な版固定ではありません。配布元の標準自動更新も独自に止めません。nvm本体の導入タグは`setup.sh`内にあります。

ソフトの導入やClaude設定の変更をせず、検査と環境記録だけを行う場合はこちらです。

```bash
bash setup.sh --check
```

`--check`でもログとテスト結果は`.setup/`へ書き込みます。setupはClaudeの会話を起動せず、通常のClaude起動時にもsetupは自動実行しません。変更履歴と旧版からの移行は[CHANGELOG.md](CHANGELOG.md)に記載しています。

## 検証状況

今回実施した確認と未検証範囲は[TEST_REPORT.md](TEST_REPORT.md)を参照してください。オフラインのテストは、Claude認証・ダウンロード・sudoなしで実行できます。

```bash
python3 -m unittest discover -s tests -v
```

基本テストは合成データの２枚資料で、PPTX・発表者ノート・ネイティブグラフ・PDF化・PNG化・日本語テキスト抽出を確認します。**本番資料のテンプレート、公式Skillの検査、研究内容の審査、PowerPointでの表示保証ではありません。**

新規Ubuntu/WSLへのオンライン全導入、実Claudeの認証を伴う動作、Windows PowerPointでの編集は未検証です。エラー時は`.setup/logs/`を確認してください。プロキシ・証明書・配布元・権限・組織の制限は導入先で解決する条件であり、回避しないでください。

## 公開と変更への参加

Gitで管理するのは共通の制作環境であり、案件資料ではありません。`.gitignore`は、空のプレースホルダーを除く`projects/`内、`.setup/`、導入済みライブラリ、環境変数ファイル、一般的なローカル認証・設定ファイルを除外します。既にGitへ登録したファイルや過去履歴は消しません。Publicへpushする前に、ステージ済みファイルとコミットの氏名・メールアドレスを確認してください。このワークスペースは案件資料のバックアップ機能を持ちません。

リポジトリ公開後はIssueやPull Requestで改善できます。報告には版、OS、対象コマンド、秘匿情報を取り除いた最小限のログを添え、認証情報や未公開資料は掲載しないでください。コマンド・設定変更の影響・制約を変えた場合は、英日READMEを同時に更新します。翻訳サービスや独自の公開基盤は不要です。

## ライセンス

Copyright 2026 Slide Workspace contributors.

このリポジトリの独自コードと文書には**Apache License, Version 2.0**を適用します。[LICENSE](LICENSE)の英語原文と[NOTICE](NOTICE)を参照してください。

第三者のツール・ライブラリ・フォント・AnthropicのSkillには、それぞれのライセンスと利用条件が適用されます。公式`pptx` Skillは別途導入するもので、**ここでは再配布せず**、本リポジトリのApache-2.0の対象にも含めません。[THIRD_PARTY.md](THIRD_PARTY.md#日本語での要点)を参照してください。本リポジトリのライセンスが、入力資料や生成スライドへ自動的に適用されるわけではありません。

## 配布元の文書

[Claude CLI](https://code.claude.com/docs/en/cli-reference) · [設定](https://code.claude.com/docs/en/settings) · [CLAUDE.md](https://code.claude.com/docs/en/memory) · [プラグイン](https://code.claude.com/docs/en/plugins-reference) · [公式Skill](https://github.com/anthropics/skills) · [Python venv](https://docs.python.org/3/library/venv.html) · [Node.jsのモジュール探索](https://nodejs.org/api/modules.html) · [nvm](https://github.com/nvm-sh/nvm)
