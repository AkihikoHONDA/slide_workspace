# Changelog

## 3.1.0 — 2026-10-17

Publication-focused release. The setup and project-creation implementations, production prompts, project template, dependency ranges, and existing workspace tests are unchanged from 3.0.0.

- Add the Apache License, Version 2.0, an attribution NOTICE, and Apache-2.0 package metadata for the original workspace code and documentation.
- Make `README.md` the English entry point and add `README.ja.md`, with reciprocal language links. Move historical design explanations out of the introductory workflow.
- Add `THIRD_PARTY.md` to distinguish this repository's license from separately installed software, fonts, and Anthropic's source-available document skills.
- Expand `.gitignore` for environment files, local Claude configuration, credential-bearing package-manager files, and operating-system metadata. Keep `CLAUDE.md` and the empty project template tracked.
- Add offline publication checks for README links and command parity, package metadata, license content, and Git exclusions.
- Refresh the release test report and checksums. No clean-machine installation or authenticated Claude end-to-end run is claimed.

### Using this release

For a fresh installation, extract or clone into a user-owned folder and follow either README. GitHub should contain the expanded source tree, not only a ZIP. Once checked into Git, remember that ignore patterns do not remove existing tracked files or history.

For an existing 3.0.0 workspace, this release does not require reinstalling the shared environment just to gain the documentation/license changes. Keep `projects/`, `.setup/`, `.venv/`, and `node_modules/`; review and apply the source/documentation changes rather than deleting the workspace. If you have local changes to policies or scripts, merge them instead of overwriting them. Use a new folder when starting from a pre-3.0 workspace so obsolete launcher files are not left behind.

## 3.0.0

Return conversation startup and resumption to the standard Claude Code CLI.

- Remove `start.sh`, `config.sh`, and the launcher-oriented `scripts/env.sh`.
- Keep `new-project.sh` only for creating project files; it never launches Claude or overwrites an existing project.
- Use the root `CLAUDE.md` to import `MAKE_SLIDES.md` and `.setup/ENVIRONMENT.md`; use each project's `CLAUDE.md` to import its brief.
- Initialize missing model, effort, and permission defaults in Claude's standard user settings instead of overriding them on every launch.
- Record direct interpreter paths; remove the need for manual venv activation, `SLIDES_WORKSPACE`, or a custom launcher.
- Keep shared dependencies, smoke checks, and user-scope installation of the official plugin.
- Select a new Node.js LTS on first installation or explicit update, while retaining a usable existing default on ordinary setup reruns.
- Preserve production preferences; change only the instructions for locating and using the shared runtime.
- Do not add CLI aliases, custom resume behavior, startup hooks, or a blanket permissions bypass.

## 2.0.0

Share Python and JavaScript environments across projects, install the official plugin at user scope, and separate shared production policy from project-specific conditions.
