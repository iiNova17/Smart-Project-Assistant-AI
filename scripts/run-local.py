"""Foreground cross-platform local launcher. Ctrl+C stops both child processes."""

import os
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    if not (root / "data/team.json").is_file():
        raise SystemExit("Run python -m app.setup first; see README.md.")
    node = shutil.which("node")
    if not node:
        raise SystemExit("Install Node.js 24 or newer first.")
    for port in (8000, 8787):
        with socket.socket() as probe:
            if probe.connect_ex(("127.0.0.1", port)) == 0:
                raise SystemExit(f"Port {port} is in use. Stop the other local instance first.")
    commands = [
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:create_app",
            "--factory",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
            "--workers",
            "1",
            "--no-access-log",
        ],
        [node, "whatsapp/src/main.mjs"],
    ]
    children = []
    try:
        for command in commands:
            children.append(
                subprocess.Popen(
                    command,
                    cwd=root,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                )
            )
        print("Chat: http://127.0.0.1:8000/ | WhatsApp pairing: http://127.0.0.1:8787/")
        print("Keep this terminal open. Ctrl+C stops both services; login state is preserved.")
        while all(child.poll() is None for child in children):
            time.sleep(1)
        raise SystemExit("A service stopped. Check the messages above before restarting.")
    except KeyboardInterrupt:
        pass
    finally:
        for child in children:
            if child.poll() is None:
                child.terminate()
        for child in children:
            try:
                child.wait(timeout=10)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait()


if __name__ == "__main__":
    main()
