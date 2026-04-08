# =============================================================
# Seminar 5.1 — Environment Setup (Windows / PowerShell)
# Run once before starting the lab:
#   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
#   .\setup.ps1
# =============================================================

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host " Seminar 5.1 — Application Layer Lab Setup"        -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

# ── Step 1: Python virtual environment ────────────────────────
Write-Host ""
Write-Host "[1/4] Creating Python virtual environment..."
python -m venv venv
.\venv\Scripts\Activate.ps1
Write-Host "      Virtual environment created at: $ScriptDir\venv"

# ── Step 2: Install dependencies ──────────────────────────────
Write-Host ""
Write-Host "[2/4] Installing Python dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
Write-Host "      All packages installed."

# ── Step 3: Generate TLS certificate (for TP2 and TP3) ────────
Write-Host ""
Write-Host "[3/4] Generating TLS certificate..."
New-Item -ItemType Directory -Force -Path certs | Out-Null

if (Test-Path "certs\server.crt") {
    Write-Host "      Certificate already exists — skipping."
    Write-Host "      (delete certs\server.crt and re-run to regenerate)"
} else {
    # Check for openssl in PATH (Git for Windows or standalone)
    if (Get-Command openssl -ErrorAction SilentlyContinue) {
        Write-Host "      Generating self-signed certificate with openssl..."
        openssl req -x509 -newkey rsa:2048 `
            -keyout certs\server.key `
            -out   certs\server.crt `
            -days 365 -nodes `
            -subj "/CN=localhost/O=Network101Lab/C=FR" `
            -addext "subjectAltName=IP:127.0.0.1,DNS:localhost" 2>$null
        Write-Host "      Certificate : certs\server.crt"
        Write-Host "      Private key : certs\server.key"
    } else {
        Write-Host "      openssl not found." -ForegroundColor Yellow
        Write-Host "      Install Git for Windows (includes openssl):" -ForegroundColor Yellow
        Write-Host "        https://git-scm.com/download/win" -ForegroundColor Yellow
        Write-Host "      Then re-run this script." -ForegroundColor Yellow
        exit 1
    }
}

# ── Step 4: Generate data file ────────────────────────────────
Write-Host ""
Write-Host "[4/4] Generating data file (~5 MB)..."
New-Item -ItemType Directory -Force -Path assets | Out-Null

if (Test-Path "assets\data.txt") {
    Write-Host "      data.txt already exists — skipping."
    Write-Host "      (delete assets\data.txt and re-run to regenerate)"
} else {
    python -c @"
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
"@
}

# ── Step 5: Generate gRPC stubs for TP4 ──────────────────────
Write-Host ""
Write-Host "[5/5] Generating gRPC stubs for TP4..."

python -m grpc_tools.protoc `
    -I tp4-grpc `
    --python_out=tp4-grpc `
    --grpc_python_out=tp4-grpc `
    tp4-grpc/metrics.proto

Write-Host "      Generated: tp4-grpc\metrics_pb2.py"
Write-Host "      Generated: tp4-grpc\metrics_pb2_grpc.py"

# ── Done ──────────────────────────────────────────────────────
Write-Host ""
Write-Host "===================================================" -ForegroundColor Green
Write-Host " Setup complete!" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Activate the virtualenv before starting any TP:"
Write-Host "    .\venv\Scripts\Activate.ps1"
Write-Host ""
Write-Host "  Each TP uses 2 terminals:"
Write-Host "    Terminal 1 (server):  cd tp1-http1; python server.py"
Write-Host "    Terminal 2 (client):  python client.py"
Write-Host ""
Write-Host "  TP1 (HTTP/1.1) :  cd tp1-http1; python server.py"
Write-Host "  TP2 (HTTP/2)   :  cd tp2-http2; python server.py"
Write-Host "  TP3 (HTTP/3)   :  cd tp3-http3; python server.py"
Write-Host "  TP4 (gRPC)     :  cd tp4-grpc;  python server.py"
Write-Host ""
