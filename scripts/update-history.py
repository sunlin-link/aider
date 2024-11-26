#!/usr/bin/env python3

import os
import re
import subprocess
import tempfile

from aider import __version__


def get_base_version():
    # Parse current version like "0.64.2.dev" to get major.minor
    match = re.match(r"(\d+\.\d+)", __version__)
    if not match:
        raise ValueError(f"Could not parse version: {__version__}")
    return match.group(1) + ".0"


def run_git_log():
    base_ver = get_base_version()
    cmd = [
        "git",
        "log",
        "-p",
        f"v{base_ver}..HEAD",
        "--",
        "aider/",
        ":!aider/website/",
        ":!HISTORY.md",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout


def main():
    # Get the git log output
    diff_content = run_git_log()

    # Save to temporary file
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".diff") as tmp:
        tmp.write(diff_content)
        tmp_path = tmp.name

    # Construct and run the aider command
    message = (
        "Update the history with changes shown in the diffs. "
        "Follow the existing pattern. "
        "Don't edit or duplicate changes that have existing history entries, "
        "just add any new items not already listed."
    )

    cmd = ["aider", "HISTORY.md", "--read", tmp_path, "--msg", message]
    subprocess.run(cmd)

    # Cleanup
    os.unlink(tmp_path)


if __name__ == "__main__":
    main()
