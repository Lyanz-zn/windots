import subprocess
import time
from pathlib import Path

# Path executable Flow Launcher
FLOW_EXE = (
    Path.home() / "scoop" / "apps" / "flow-launcher" / "current" / "Flow.Launcher.exe"
)


def main():
    # Hentikan proses Flow Launcher
    subprocess.run(
        ["taskkill", "/IM", "Flow.Launcher.exe", "/T", "/F"],
        capture_output=True,
        check=False,
    )
    time.sleep(1)
    # Jalankan kembali tanpa membuka terminal baru
    if FLOW_EXE.exists():
        subprocess.Popen(
            [str(FLOW_EXE)],
            cwd=str(FLOW_EXE.parent),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
    else:
        raise FileNotFoundError(f"Flow Launcher tidak ditemukan: {FLOW_EXE}")


if __name__ == "__main__":
    main()
