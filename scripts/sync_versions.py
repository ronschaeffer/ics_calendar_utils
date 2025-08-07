#!/usr/bin/env python3
"""
Version Synchronization Script for ICS Calendar Utils

This script ensures version consistency between pyproject.toml and __init__.py files.

Usage:
    python scripts/sync_versions.py
    python scripts/sync_versions.py --check  # Check only, don't update
"""

import argparse
import re
import sys
from pathlib import Path


class VersionSync:
    """Version synchronization for the ICS Calendar Utils project."""

    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.pyproject_path = self.project_root / "pyproject.toml"
        self.version = self._get_pyproject_version()

    def _get_pyproject_version(self) -> str:
        """Get version from pyproject.toml (source of truth)."""
        if not self.pyproject_path.exists():
            raise FileNotFoundError(f"pyproject.toml not found in {self.project_root}")

        content = self.pyproject_path.read_text()
        match = re.search(r'^version = "([^"]+)"', content, re.MULTILINE)
        if match:
            return match.group(1)

        raise ValueError("Version not found in pyproject.toml")

    def find_init_files(self) -> list[Path]:
        """Find all __init__.py files in the src directory."""
        init_files = []
        src_dir = self.project_root / "src"

        if src_dir.exists():
            for init_file in src_dir.rglob("__init__.py"):
                if "__pycache__" not in str(init_file):
                    init_files.append(init_file)

        return init_files

    def update_init_file(self, init_path: Path, check_only: bool = False) -> bool:
        """Update version in __init__.py file."""
        if not init_path.exists():
            return False

        content = init_path.read_text()

        # Look for __version__ = "x.y.z" pattern
        version_pattern = r'^(__version__ = ["\'])([^"\']+)(["\'])'
        match = re.search(version_pattern, content, re.MULTILINE)

        if not match:
            return False

        current_version = match.group(2)

        if current_version == self.version:
            return False  # Already correct

        if check_only:
            print(
                f"⚠️  Version mismatch in {init_path.relative_to(self.project_root)}: "
                f"found {current_version}, expected {self.version}"
            )
            return True

        # Update the version
        new_content = re.sub(
            version_pattern,
            f"{match.group(1)}{self.version}{match.group(3)}",
            content,
            flags=re.MULTILINE,
        )

        init_path.write_text(new_content)
        print(f"✅ Updated {init_path.relative_to(self.project_root)}: {self.version}")
        return True

    def sync_versions(self, check_only: bool = False) -> dict:
        """Sync versions across all relevant files."""
        print(f"📦 Source version from pyproject.toml: {self.version}")

        results = {"init_files": 0, "errors": 0}

        # Update __init__.py files
        for init_file in self.find_init_files():
            try:
                if self.update_init_file(init_file, check_only):
                    results["init_files"] += 1
            except Exception as e:
                print(f"❌ Error updating {init_file}: {e}")
                results["errors"] += 1

        return results


def main():
    parser = argparse.ArgumentParser(description="Sync versions across project files")
    parser.add_argument(
        "--check", action="store_true", help="Check for mismatches without updating"
    )
    args = parser.parse_args()

    try:
        # Find project root (look for pyproject.toml)
        project_root = Path.cwd()
        while project_root != project_root.parent:
            if (project_root / "pyproject.toml").exists():
                break
            project_root = project_root.parent
        else:
            print("❌ Could not find pyproject.toml")
            sys.exit(1)

        syncer = VersionSync(project_root)
        results = syncer.sync_versions(check_only=args.check)

        if args.check:
            if results["init_files"] + results["errors"] == 0:
                print("✅ All versions are in sync")
            else:
                print(f"⚠️  Found {results['init_files']} version mismatches")
                if results["errors"] > 0:
                    print(f"❌ {results['errors']} errors occurred")
                sys.exit(1)
        else:
            print(f"✅ Updated {results['init_files']} __init__.py files")
            if results["errors"] > 0:
                print(f"❌ {results['errors']} errors occurred")
                sys.exit(1)

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
