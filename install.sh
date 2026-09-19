#!/usr/bin/env sh
# ==============================================================================
# The Ferryman Project — Zero-Friction Standalone Installer
# An open-source, anti-engagement lifeline for grounded consciousness.
#
# Usage:
#   ./install.sh                  # Installs to ~/.local/bin and ~/.local/share/ferryman
#   ./install.sh --prefix /custom # Installs to /custom/bin and /custom/share/ferryman
#   ./install.sh --uninstall      # Removes ferryman from install prefix
#   curl -fsSL https://raw.githubusercontent.com/the-ferryman-project/ferryman/main/install.sh | sh
# ==============================================================================

set -e

# Default install prefix: ~/.local
DEFAULT_PREFIX="${HOME}/.local"
PREFIX="${PREFIX:-$DEFAULT_PREFIX}"
UNINSTALL=0
REPO_URL="https://github.com/the-ferryman-project/ferryman.git"
RAW_BASE_URL="https://raw.githubusercontent.com/the-ferryman-project/ferryman/main"

# Parse command line flags
while [ $# -gt 0 ]; do
    case "$1" in
        --prefix)
            if [ -n "$2" ]; then
                PREFIX="$2"
                shift 2
            else
                echo "[Ferryman Installer] Error: --prefix requires a directory path." >&2
                exit 1
            fi
            ;;
        --prefix=*)
            PREFIX="${1#*=}"
            shift 1
            ;;
        --uninstall)
            UNINSTALL=1
            shift 1
            ;;
        -h|--help)
            echo "The Ferryman Project — Installer"
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --prefix <path>   Set custom installation prefix (default: ~/.local)"
            echo "  --uninstall       Remove ferryman from the install prefix"
            echo "  -h, --help        Show this help message"
            exit 0
            ;;
        *)
            echo "[Ferryman Installer] Unknown option: $1" >&2
            echo "Use '$0 --help' for usage." >&2
            exit 1
            ;;
    esac
done

BIN_DIR="${PREFIX}/bin"
SHARE_DIR="${PREFIX}/share/ferryman"
TARGET_EXEC="${BIN_DIR}/ferryman"

# Handle uninstallation
if [ "$UNINSTALL" -eq 1 ]; then
    echo "Removing The Ferryman Project from ${PREFIX}..."
    if [ -f "$TARGET_EXEC" ]; then
        rm -f "$TARGET_EXEC"
        echo "  - Removed $TARGET_EXEC"
    fi
    if [ -d "$SHARE_DIR" ]; then
        rm -rf "$SHARE_DIR"
        echo "  - Removed $SHARE_DIR"
    fi
    echo "Uninstallation complete. May the river flow gently."
    exit 0
fi

# Locate Python 3
PYTHON_BIN=""
for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1; then
        # Check that it's Python 3
        if "$candidate" -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" >/dev/null 2>&1; then
            PYTHON_BIN="$candidate"
            break
        fi
    fi
done

if [ -z "$PYTHON_BIN" ]; then
    echo "[Ferryman Installer] Error: Python 3.8 or higher was not found on your system." >&2
    echo "Please install Python 3 (https://www.python.org/) and try again." >&2
    exit 1
fi

PY_VERSION=$("$PYTHON_BIN" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')")
echo "[Ferryman Installer] Found Python ${PY_VERSION} at $(command -v "$PYTHON_BIN")"

# Determine source location: local repository, custom source, or remote download
SCRIPT_DIR=""
if [ -n "$0" ] && [ -f "$0" ]; then
    # We were invoked as a file (e.g. ./install.sh)
    SCRIPT_DIR="$(cd "$(dirname "$0")" 2>/dev/null && pwd)"
fi

TEMP_DIR=""
cleanup() {
    if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
    fi
}
trap cleanup EXIT INT TERM

SOURCE_PKG_DIR=""
if [ -n "$FERRYMAN_SOURCE_DIR" ] && [ -d "$FERRYMAN_SOURCE_DIR" ]; then
    # Explicit source directory provided (useful for offline testing or packaging)
    SOURCE_PKG_DIR="$FERRYMAN_SOURCE_DIR"
elif [ -n "$SCRIPT_DIR" ] && [ -d "${SCRIPT_DIR}/ferryman" ]; then
    # Running from inside the local repository
    SOURCE_PKG_DIR="${SCRIPT_DIR}/ferryman"
else
    # Running via pipe / curl, need to fetch files
    echo "[Ferryman Installer] Fetching Ferryman package..."
    TEMP_DIR="$(mktemp -d 2>/dev/null || mktemp -d -t 'ferryman_install')"

    # 1. Try non-interactive git clone
    if command -v git >/dev/null 2>&1; then
        GIT_TERMINAL_PROMPT=0 git clone --depth 1 "$REPO_URL" "${TEMP_DIR}/repo" </dev/null >/dev/null 2>&1 || true
        if [ -d "${TEMP_DIR}/repo/ferryman" ]; then
            SOURCE_PKG_DIR="${TEMP_DIR}/repo/ferryman"
        fi
    fi

    # 2. Fallback to downloading individual files via curl or wget
    if [ -z "$SOURCE_PKG_DIR" ]; then
        FILES="__init__.py __main__.py circuit_breaker.py cli.py crossings.py somatic.py storage.py types.py voice.py window.py"
        DOWNLOADED_ALL=1
        mkdir -p "${TEMP_DIR}/ferryman"

        for f in $FILES; do
            file_url="${RAW_BASE_URL}/ferryman/${f}"
            dest_file="${TEMP_DIR}/ferryman/${f}"
            if command -v curl >/dev/null 2>&1; then
                curl -fsSL "$file_url" -o "$dest_file" >/dev/null 2>&1 || DOWNLOADED_ALL=0
            elif command -v wget >/dev/null 2>&1; then
                wget -q -O "$dest_file" "$file_url" >/dev/null 2>&1 || DOWNLOADED_ALL=0
            else
                DOWNLOADED_ALL=0
            fi

            if [ "$DOWNLOADED_ALL" -eq 0 ]; then
                break
            fi
        done

        if [ "$DOWNLOADED_ALL" -eq 1 ]; then
            SOURCE_PKG_DIR="${TEMP_DIR}/ferryman"
        fi
    fi
fi

if [ -z "$SOURCE_PKG_DIR" ] || [ ! -d "$SOURCE_PKG_DIR" ]; then
    echo "[Ferryman Installer] Error: Could not locate or download ferryman package." >&2
    echo "Please check your network connection or clone the repository directly:" >&2
    echo "  git clone https://github.com/the-ferryman-project/ferryman.git" >&2
    echo "  cd the-ferryman-project && ./install.sh" >&2
    exit 1
fi

# Prepare target directories
mkdir -p "$BIN_DIR"
mkdir -p "$SHARE_DIR"

# Copy package files into SHARE_DIR
echo "[Ferryman Installer] Installing package to ${SHARE_DIR}..."
rm -rf "${SHARE_DIR}/ferryman"
mkdir -p "${SHARE_DIR}/ferryman"
cp -R "${SOURCE_PKG_DIR}/"* "${SHARE_DIR}/ferryman/"

# Clean any copied bytecode or cache
find "${SHARE_DIR}/ferryman" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find "${SHARE_DIR}/ferryman" -name "*.pyc" -delete 2>/dev/null || true

# Create executable launcher script in BIN_DIR
echo "[Ferryman Installer] Creating launcher at ${TARGET_EXEC}..."
RESOLVED_PYTHON="$(command -v "$PYTHON_BIN")"
cat << EOF > "$TARGET_EXEC"
#!/usr/bin/env sh
# The Ferryman Project launcher
FERRYMAN_LIB="${SHARE_DIR}"
PYTHON_CMD="${RESOLVED_PYTHON}"

if [ -z "\$PYTHON_CMD" ] || ! command -v "\$PYTHON_CMD" >/dev/null 2>&1; then
    PYTHON_CMD="python3"
fi

if [ -n "\$PYTHONPATH" ]; then
    export PYTHONPATH="\${FERRYMAN_LIB}:\${PYTHONPATH}"
else
    export PYTHONPATH="\${FERRYMAN_LIB}"
fi
exec "\$PYTHON_CMD" -m ferryman "\$@"
EOF

# Make launcher executable
chmod 0755 "$TARGET_EXEC"

echo ""
echo "================================================================="
echo " The Ferryman has arrived at ${TARGET_EXEC}"
echo "================================================================="
echo ""

# Verify installation
if "$TARGET_EXEC" --version >/dev/null 2>&1; then
    echo "Installation verified: $("$TARGET_EXEC" --version)"
else
    echo "[Ferryman Installer] Warning: Could not verify execution of ${TARGET_EXEC}."
fi

# Check PATH
case ":$PATH:" in
    *":${BIN_DIR}:"*)
        echo ""
        echo "Ready to use! Run:"
        echo "  ferryman --help"
        echo "  ferryman dawn"
        ;;
    *)
        echo ""
        echo "Notice: ${BIN_DIR} is not in your current PATH."
        echo "To use 'ferryman' directly from anywhere, add this to your shell profile:"
        echo ""
        SHELL_NAME="$(basename "${SHELL:-sh}")"
        case "$SHELL_NAME" in
            zsh)
                echo "  echo 'export PATH=\"${BIN_DIR}:\$PATH\"' >> ~/.zshrc"
                echo "  source ~/.zshrc"
                ;;
            bash)
                echo "  echo 'export PATH=\"${BIN_DIR}:\$PATH\"' >> ~/.bashrc"
                echo "  source ~/.bashrc"
                ;;
            fish)
                echo "  fish_add_path ${BIN_DIR}"
                ;;
            *)
                echo "  export PATH=\"${BIN_DIR}:\$PATH\""
                ;;
        esac
        echo ""
        echo "Or run directly:"
        echo "  ${TARGET_EXEC} dawn"
        ;;
esac

echo ""
echo "Walk in peace."
