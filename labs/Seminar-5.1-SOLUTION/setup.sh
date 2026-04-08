#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────
# Seminar 5.1 — Environment Setup  (macOS / Linux)
# Run once before starting the lab:
#   chmod +x setup.sh && ./setup.sh
#
# Windows users: run setup.ps1 instead (PowerShell)
# ──────────────────────────────────────────────────────────────────

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "==================================================="
echo " Seminar 5.1 — Application Layer Lab Setup"
echo "==================================================="

# ── Step 1: Python virtual environment ─────────────────────────
echo ""
echo "[1/4] Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
echo "      Virtual environment created at: $SCRIPT_DIR/venv"

# ── Step 2: Install dependencies ────────────────────────────────
echo ""
echo "[2/4] Installing Python dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "      All packages installed."

# ── Step 3: Generate TLS certificate (for TP2 and TP3) ─────────
#
#   openssl generates a self-signed certificate for localhost.
#   The Python clients use verify=False / CERT_NONE so no CA trust is needed.
#
echo ""
echo "[3/4] Generating TLS certificate..."
mkdir -p certs

if [ -f "certs/server.crt" ]; then
    echo "      Certificate already exists — skipping."
    echo "      (delete certs/server.crt and re-run to regenerate)"
else
    echo "      Generating self-signed certificate with openssl..."
    openssl req -x509 -newkey rsa:2048 \
        -keyout certs/server.key \
        -out   certs/server.crt \
        -days 365 -nodes \
        -subj "/CN=localhost/O=Network101Lab/C=FR" \
        -addext "subjectAltName=IP:127.0.0.1,DNS:localhost" \
        2>/dev/null
    echo "      Certificate : certs/server.crt"
    echo "      Private key : certs/server.key"
fi

# ── Step 4: Generate data file ──────────────────────────────────
echo ""
echo "[4/4] Generating data file (~5 MB)..."
mkdir -p assets

if [ -f "assets/data.txt" ]; then
    echo "      data.txt already exists — skipping."
    echo "      (delete assets/data.txt and re-run to regenerate)"
else
    python3 -c "
import os
target = 5 * 1024 * 1024
line   = 'NETWORK-101-LAB-DATA: ' + 'A' * 78 + '\n'
with open('assets/data.txt', 'w') as f:
    written = 0
    while written < target:
        f.write(line)
        written += len(line)
size = os.path.getsize('assets/data.txt')
print(f'      Generated assets/data.txt ({size:,} bytes)')
"
fi

# ── Step 5: Generate gRPC stubs for TP4 ────────────────────────
echo ""
echo "[5/5] Generating gRPC stubs for TP4..."

python -m grpc_tools.protoc \
    -I tp4-grpc \
    --python_out=tp4-grpc \
    --grpc_python_out=tp4-grpc \
    tp4-grpc/metrics.proto

echo "      Generated: tp4-grpc/metrics_pb2.py"
echo "      Generated: tp4-grpc/metrics_pb2_grpc.py"

# ── Done ─────────────────────────────────────────────────────────
echo ""
echo "==================================================="
echo " Setup complete!"
echo "==================================================="
echo ""
echo "  Activate the virtualenv before starting any TP:"
echo "    source venv/bin/activate"
echo ""
echo "  Each TP uses 2 terminals:"
echo "    Terminal 1 (server):  cd tp1-http1 && python server.py"
echo "    Terminal 2 (client):  python client.py"
echo ""
echo "  TP1 (HTTP/1.1) :  cd tp1-http1 && python server.py"
echo "  TP2 (HTTP/2)   :  cd tp2-http2 && python server.py"
echo "  TP3 (HTTP/3)   :  cd tp3-http3 && python server.py"
echo "  TP4 (gRPC)     :  cd tp4-grpc  && python server.py"
echo ""
