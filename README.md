# Slide Workspace

**English** | [日本語](README.ja.md)

**Create editable PowerPoint drafts with Claude Code and Anthropic's official `pptx` skill.** Set up the tools once, keep each presentation's sources and outputs in its own project, and use the standard Claude Code CLI for creation and revision.

The workspace automates environment setup—not the decisions about what makes a good presentation. A shared brief guides Claude to connect the purpose, evidence, and conclusions, choose layouts that suit the content, and preserve useful material for the author's final edits. The intended outputs are an editable `.pptx`, a PDF preview, speaker notes, and a short run record.

**Platform:** Ubuntu 22.04 or later, including Ubuntu on WSL2; Ubuntu 24.04 LTS is the installation baseline. **Status:** experimental; a complete clean-machine installation and authenticated Claude run have not been verified. See [Validation status](#validation-status).

**Language:** this README is in English; a complete [Japanese README](README.ja.md) is available. The production prompts, project template, and some terminal messages remain in Japanese. Slide and speaker-note languages are selected in each project's `talk-brief.md`.

This is an independent project, not affiliated with or endorsed by Anthropic. The original workspace code and documentation use [Apache-2.0](LICENSE); separately installed tools and skills retain their own terms. See [Third-party components](THIRD_PARTY.md).

## Before you install

Review [setup.sh](setup.sh) before running it. It installs OS packages using `sudo`, prepares a shared Python environment and Node.js dependencies, installs or reuses Claude Code, and installs/enables the official document-skills plugin for your user. It also updates shell initialization files and adds **missing** model, effort, and permission defaults to your **user-wide** Claude settings. Those settings can affect Claude projects outside this workspace; existing values are preserved.

Start with Ubuntu and a regular user account with `sudo` access. You need internet access to the configured package sources and upstream installers, and access to Claude Code through an authorized account or provider configuration. Claude access is separate from this repository and may incur charges. WSL/Ubuntu installation, account sign-in, trust prompts, and organizational approvals are not automated. This is not a Windows-native or macOS installer.

Only use materials that you are permitted to send to the selected model. Local files and Git exclusion do **not** mean that presentation content stays on the machine.

## Quick start

### 1. Set up the shared tools

Clone this repository, or extract the source archive, into a user-owned Linux directory such as `~/Workspace/slide-workspace`. Run the following in the directory containing `setup.sh`:

```bash
bash setup.sh
```

Do **not** run the whole script with `sudo`. Only its OS-package steps use elevated privileges. After setup, open a new terminal so the shell initialization changes take effect. Sign in when you first start Claude Code; do not put credentials in this repository.

### 2. Create a presentation project

From the workspace root:

```bash
bash new-project.sh my-talk
```

Edit `projects/my-talk/talk-brief.md`: fill in the topic, purpose, audience, language, timing, session or meeting context, acknowledgments, and any template requirements. Put source documents in `projects/my-talk/inputs/` and figures or photos in `inputs/assets/`. File names are not fixed; explain the role and priority of multiple sources in the brief.

The project template initially selects Japanese slides and requested acknowledgments. Change those fields to match your presentation. `new-project.sh` creates files only; it neither launches Claude nor overwrites an existing project. Project names may contain letters, digits, hyphens, and underscores and must start with a letter or digit.

### 3. Start Claude and request a draft

```bash
cd projects/my-talk
claude
```

Then send, for example:

```text
Use talk-brief.md and inputs/ to create the editable first draft,
including the prescribed checks and all requested deliverables.
```

The root `CLAUDE.md` imports the shared production policy and recorded interpreter paths; the project's `CLAUDE.md` imports its brief. There is no custom launcher and no need to activate the Python environment by hand each time. These are instructions for Claude, not a technical enforcement boundary. Check the loaded context and effective settings on first use.

Alternatively, pass the supplied starting prompt through the standard CLI from the same project directory:

```bash
claude "$(cat ../../START_PROMPT.md)"
```

Use either that command or the interactive request, not both. Running `claude` alone does not automatically begin slide generation.

### 4. Review and revise

By default, the first draft is `outputs/talk-r01.pptx`, with a corresponding PDF, `speaker-notes-r01.md`, and `run-info-r01.md`. The filename prefix is configurable in the brief. Generated code and processed assets belong in `work/`.

Ask for focused revisions in the same conversation, or resume from the project directory:

```bash
claude --resume
```

To continue the most recent conversation for that directory:

```bash
claude --continue
```

Preserve revision files. After manual PowerPoint edits, tell Claude which PPTX is the current editing source so regenerating from older code does not discard your work. Copying project files to another machine does not automatically transfer Claude's conversation history.

## Workspace structure

```text
slide-workspace/
├── README.md / README.ja.md
├── LICENSE / NOTICE / THIRD_PARTY.md
├── setup.sh                 # Shared installation, updates, smoke checks
├── new-project.sh           # Optional project scaffolding only
├── CLAUDE.md                # Shared policy and environment imports
├── MAKE_SLIDES.md           # Reusable production policy
├── START_PROMPT.md          # Optional initial request
├── requirements.txt
├── package.json
├── package-lock.json        # Generated by npm during setup
├── .venv/                   # Shared Python dependencies; not committed
├── node_modules/            # Shared Node.js dependencies; not committed
├── .setup/                  # Local paths, logs, smoke outputs; not committed
├── scripts/ / tests/
├── project-template/
└── projects/                # Presentation materials; not committed
    └── my-talk/
        ├── CLAUDE.md
        ├── talk-brief.md
        ├── inputs/
        ├── work/
        └── outputs/
```

The source distribution contains no presentation materials, credentials, installed dependencies, font binaries, or Anthropic skill files. All projects share one `.venv` and one `node_modules`. Keep project code under `projects/` so Node's parent-directory module lookup can find the shared dependencies.

## Configuration and customization

### Presentation policy

Edit [MAKE_SLIDES.md](MAKE_SLIDES.md) for shared preferences and each project's `talk-brief.md` for its audience, sources, and constraints. The default policy asks for a draft that is easier to trim than to rebuild, preserves supporting figures and transitions, and leaves layout choices to Claude. It permits 14–16 pt text when appropriate while prioritizing the readability of important information; it does not require one layout or one title form on every slide.

The prompts and template intentionally remain one Japanese-language source of truth in this release. Editing the README does not change the production instructions. Ask an active conversation to reread any policy or brief you change.

### Claude settings

Setup adds the following only where the fields are not already set in `~/.claude/settings.json`, or in the configuration directory selected by `CLAUDE_CONFIG_DIR`. Changed existing files are backed up.

```json
{
  "model": "opus",
  "effortLevel": "high",
  "permissions": {
    "defaultMode": "auto"
  }
}
```

These are **user-wide** preferences. Claude's CLI, environment, project settings, or organizational policy can take precedence. The `opus` alias can change as upstream models change; use an explicit supported model ID when a specific version matters. Inspect settings with `/status`, models with `/model`, and loaded instructions with `/context`.

`auto` is not a blanket permissions bypass, and availability depends on the Claude environment and policy. When it is unavailable, select `acceptEdits` in the standard settings, or for one session:

```bash
claude --permission-mode acceptEdits
```

### Interpreter paths

Setup records absolute paths in `.setup/ENVIRONMENT.md`. Claude is instructed to call `.venv/bin/python` directly and to use the recorded Linux Node.js interpreter. A command that starts child processes by the names `python` or `node` may need a command-local `PATH` adjustment. No custom shell alias, always-active venv, or session hook is added by this workspace.

## Maintenance

Close active production sessions, then update from the workspace root:

```bash
bash setup.sh --update
```

This updates the shared dependencies within the declared ranges, the selected Node.js LTS, Claude Code, and the official plugin, then repeats the smoke checks and environment recording. It does not perform a distribution upgrade, edit `sudoers`, or disable TLS verification. Shared updates can affect every presentation; this is not a fully pinned build. Standard upstream auto-update behavior is not disabled. The nvm installer tag is declared in `setup.sh`.

To run checks and refresh local environment records without installing software or editing Claude settings:

```bash
bash setup.sh --check
```

`--check` still writes logs and test outputs under `.setup/`. Setup never starts a Claude conversation, and normal Claude startup never runs setup automatically. See [CHANGELOG.md](CHANGELOG.md) for release changes and migration notes.

## Validation status

See [TEST_REPORT.md](TEST_REPORT.md) for checks performed for this release and their limits. The offline suite can be run without Claude authentication, downloads, or `sudo`:

```bash
python3 -m unittest discover -s tests -v
```

The smoke test uses synthetic data to check a two-slide PPTX, speaker notes, a native chart, PDF conversion, PNG rendering, and extractable Japanese text. It is **not** a design template, an official Skill validation, a scientific review, or a guarantee of PowerPoint rendering quality.

A complete online installation on a clean Ubuntu/WSL machine, authenticated Claude operation, and Windows PowerPoint editing remain unverified. For errors, inspect `.setup/logs/`. Proxy, certificate, package-source, permission, and organizational restrictions must be resolved in the deployment environment; do not bypass them.

## Publishing and contributing

Commit the reusable workspace, not presentation projects. `.gitignore` excludes `projects/` contents (except the empty placeholder), `.setup/`, installed dependencies, environment files, and common local credential/configuration files. It does not remove files already tracked by Git or erase history. Before a public push, inspect staged files and commit author/email metadata. The workspace is not a backup service for project files.

Issues and pull requests are welcome once the repository is hosted. Include the workspace version, OS version, affected command, and a minimal redacted log; do not upload credentials or unpublished presentation materials. Keep the English and Japanese READMEs aligned when commands, configuration effects, or limitations change. No translation service or custom publishing platform is required.

## License

Copyright 2026 Slide Workspace contributors.

The original code and documentation in this repository are licensed under the **Apache License, Version 2.0**. See [LICENSE](LICENSE) and [NOTICE](NOTICE).

Third-party tools, libraries, fonts, and Anthropic skills are governed by their respective licenses and terms. Anthropic's official `pptx` skill is installed separately and is **not redistributed** here; it is not covered by this repository's Apache-2.0 license. See [THIRD_PARTY.md](THIRD_PARTY.md). The workspace license does not by itself license your input materials or generated presentations.

## Upstream documentation

[Claude CLI](https://code.claude.com/docs/en/cli-reference) · [Settings](https://code.claude.com/docs/en/settings) · [CLAUDE.md](https://code.claude.com/docs/en/memory) · [Plugin reference](https://code.claude.com/docs/en/plugins-reference) · [Official skills](https://github.com/anthropics/skills) · [Python venv](https://docs.python.org/3/library/venv.html) · [Node.js module lookup](https://nodejs.org/api/modules.html) · [nvm](https://github.com/nvm-sh/nvm)
