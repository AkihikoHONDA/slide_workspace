#!/usr/bin/env python3
"""One-time defaults in Claude's native user settings; not a launcher/config layer."""
from __future__ import annotations

import argparse
import copy
import json
import os
from pathlib import Path
import shutil
import tempfile
from datetime import datetime, timezone


def configure(settings_path: Path) -> dict:
    settings_path = settings_path.expanduser()
    if settings_path.is_symlink():
        settings_path = settings_path.resolve()
    before = settings_path.read_text(encoding="utf-8") if settings_path.exists() else None
    data = json.loads(before) if before is not None else {}
    if not isinstance(data, dict):
        raise ValueError("Claude settings must be a JSON object; no changes made")
    original = copy.deepcopy(data)
    data.setdefault("model", "opus")
    data.setdefault("effortLevel", "high")
    permissions = data.setdefault("permissions", {})
    if not isinstance(permissions, dict):
        raise ValueError("permissions must be a JSON object; no changes made")
    permissions.setdefault("defaultMode", "auto")
    # Preserve all existing preferences and permission rules. No PATH injection,
    # bypass mode, global read/write allowlist, or automatic-memory customization.
    if data != original or before is None:
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        if before is not None:
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
            backup = settings_path.with_name(f"{settings_path.name}.bak-slide-workspace-{stamp}")
            shutil.copy2(settings_path, backup)
            print(f"Backup: {backup}")
        fd, tmp = tempfile.mkstemp(prefix=".slide-settings-", dir=settings_path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.write("\n")
            os.chmod(tmp, 0o600)
            os.replace(tmp, settings_path)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
    print(f"Claude standard user settings: {settings_path}")
    print("model={}, effortLevel={}, permissions.defaultMode={}".format(
        data["model"], data["effortLevel"], permissions["defaultMode"]))
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    config_dir = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")
    parser.add_argument("--settings", type=Path, default=config_dir / "settings.json",
                        help="Standard settings path; override mainly for isolated testing")
    args = parser.parse_args()
    try:
        configure(args.settings)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"ERROR: {exc}\n")


if __name__ == "__main__":
    main()
