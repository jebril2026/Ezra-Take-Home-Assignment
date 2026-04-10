import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / ".venv"
REQUIREMENTS_FILE = ROOT / "requirements.txt"
ENV_FILE = ROOT / ".env"

def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    print(f"\n> {' '.join(cmd)}")
    return subprocess.run(cmd, check=check, text=True)

def command_exists(name: str) -> bool:
    return shutil.which(name) is not None

def fail(message: str) -> None:
    print(f"\nERROR: {message}")
    sys.exit(1)

def get_python_executable() -> str:
    if command_exists("asdf"):
        try:
            result = subprocess.run(
                ["asdf", "which", "python"],
                capture_output=True,
                text=True,
                check=True,
            )
            python_path = result.stdout.strip()
            if python_path:
                print(f"Using asdf-managed Python: {python_path}")
                return python_path
        except subprocess.CalledProcessError:
            print("asdf found, but no active Python version is set.")
    if command_exists("python3"):
        python_path = shutil.which("python3")
        print(f"Using system python3: {python_path}")
        return python_path
    fail("Python was not found. Install Python first, preferably via asdf.")
    return ""

def ensure_asdf() -> None:
    if not command_exists("asdf"):
        fail(
            "asdf is not installed or not available in PATH. "
            "Please install asdf and ensure your shell loads it before running setup."
        )
    run(["asdf", "--version"], check=False)
    try:
        result = subprocess.run(
            ["asdf", "current", "python"],
            capture_output=True,
            text=True,
            check=False,
        )
        current = result.stdout.strip()
        if current:
            print(f"asdf current python: {current}")
        else:
            print(
                "No active asdf Python version detected. "
                "The script will fall back to python3 if available."
            )
    except Exception:
        print("Unable to verify current asdf Python version.")

def create_venv(python_executable: str) -> None:
    if VENV_DIR.exists():
        print(f"Virtual environment already exists at: {VENV_DIR}")
    else:
        print(f"Creating virtual environment at: {VENV_DIR}")
        run([python_executable, "-m", "venv", str(VENV_DIR)])

def venv_python() -> str:
    if sys.platform == "win32":
        return str(VENV_DIR / "Scripts" / "python.exe")
    return str(VENV_DIR / "bin" / "python")

def install_dependencies() -> None:
    vp = venv_python()
    run([vp, "-m", "pip", "install", "--upgrade", "pip"])
    if not REQUIREMENTS_FILE.exists():
        fail(f"Missing requirements.txt at {REQUIREMENTS_FILE}")
    run([vp, "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)])

def install_playwright_browsers() -> None:
    vp = venv_python()
    run([vp, "-m", "playwright", "install"])



def validate_env() -> None:
    required_keys = [
        "ENV",
        "INTERNAL_HUB_EMAIL",
        "INTERNAL_HUB_PASSWORD"
    ]
    env_values: dict[str, str] = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            env_values[key.strip()] = value.strip()
    missing = [key for key in required_keys if not os.getenv(key) and not env_values.get(key)]
    if missing:
        fail(
            "Missing required environment variables: "
            + ", ".join(missing)
            + ". Update your .env file before running tests."
        )
    print("Environment validation passed.")

def smoke_check() -> None:
    vp = venv_python()
    smoke_test_path = ROOT / "tests" / "automation" / "install_smoke.py"
    if smoke_test_path.exists():
        print(f"Running smoke test: {smoke_test_path}")
        run([vp, "-m", "pytest", str(smoke_test_path)])
    else:
        print(f"Smoke test file not found: {smoke_test_path}. Skipping.")

def print_next_steps() -> None:
    activate_cmd = "source venv/bin/activate" if sys.platform != "win32" else r"venv\Scripts\activate"
    print("\nSetup complete.")
    print(f"Next steps:")
    print(f"1. {activate_cmd}")
    print("2. Review .env and update any values if needed")
    print("3. Run tests with: pytest")


def main() -> None:
    print("Starting project setup...")
    ensure_asdf()
    python_executable = get_python_executable()
    create_venv(python_executable)
    install_dependencies()
    install_playwright_browsers()
    validate_env()
    smoke_check()
    print_next_steps()

if __name__ == "__main__":
    main()
