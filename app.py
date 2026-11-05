"""Inspect a Linux process and filesystem from the host or a container."""

import argparse
import json
import os
from pathlib import Path
import platform
import shutil
import sys


def collect_report(directory):
    directory = directory.expanduser().resolve(strict=True)
    if not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")
    disk = shutil.disk_usage(directory)
    return {
        "system": platform.system(),
        "kernel": platform.release(),
        "architecture": platform.machine(),
        "python": platform.python_version(),
        "uid": os.getuid(),
        "gid": os.getgid(),
        "cpu_count": os.cpu_count(),
        "directory": str(directory),
        "disk": {
            "total_bytes": disk.total,
            "used_bytes": disk.used,
            "free_bytes": disk.free,
        },
    }


def format_report(report):
    free_gib = report["disk"]["free_bytes"] / (1024**3)
    return "\n".join(
        [
            f"System: {report['system']} {report['kernel']}",
            f"Architecture: {report['architecture']}",
            f"Python: {report['python']}",
            f"Process identity: uid={report['uid']} gid={report['gid']}",
            f"Logical CPUs reported by the runtime: {report['cpu_count']}",
            f"Directory: {report['directory']}",
            f"Free space: {free_gib:.2f} GiB",
        ]
    )


def main(arguments=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print a JSON report.")
    parser.add_argument(
        "--directory",
        type=Path,
        default=Path.cwd(),
        help="Filesystem directory to inspect (default: current directory).",
    )
    args = parser.parse_args(arguments)
    try:
        report = collect_report(args.directory)
    except OSError as error:
        print(f"linux-lab: {error}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))
    else:
        print(format_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
