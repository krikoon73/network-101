#!/bin/bash

# Certificate Generation Script for Layer-4 Lab
# This script generates SSL/TLS certificates for HTTPS communication
# between tcp-client and web-server via reverse-proxy

set -e  # Exit on error

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CERTS_DIR="${SCRIPT_DIR}/../services/certs"

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║              SSL/TLS Certificate Generation for Layer-4 Lab                 ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Create certs directory if it doesn't exist
mkdir -p "${CERTS_DIR}"

# Check if certificates already exist
if [ -f "${CERTS_DIR}/ca-cert.pem" ] && \
   [ -f "${CERTS_DIR}/reverse-proxy-cert.pem" ] && \
   [ -f "${CERTS_DIR}/web-server-cert.pem" ]; then
    echo -e "${YELLOW}⚠️  Certificates already exist in ${CERTS_DIR}${NC}"
    echo -e "${YELLOW}   Skipping certificate generation.${NC}"
    echo -e "${YELLOW}   To regenerate certificates, delete the existing ones first.${NC}"
    echo ""
    exit 0
fi

echo -e "${GREEN}📁 Certificate directory: ${CERTS_DIR}${NC}"
echo ""

# Change to certs directory
cd "${CERTS_DIR}"

# Clean up any partial certificate files
echo -e "${BLUE}🧹 Cleaning up old certificate files...${NC}"
rm -f ca-cert.pem ca-key.pem ca-cert.srl
rm -f reverse-proxy-cert.pem reverse-proxy-key.pem reverse-proxy-csr.pem
rm -f web-server-cert.pem web-server-key.pem web-server-csr.pem
echo ""

# Generate Certificate Authority (CA)
echo -e "${GREEN}🔐 Step 1/3: Generating Certificate Authority (CA)...${NC}"
openssl req -x509 -newkey rsa:4096 -keyout ca-key.pem -out ca-cert.pem \
    -days 365 -nodes \
    -subj "/C=FR/ST=IDF/L=Paris/O=Dauphine/OU=MIAGE/CN=Lab-CA" \
    2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}   ✅ CA certificate created successfully${NC}"
    echo -e "      Subject: C=FR, ST=IDF, L=Paris, O=Dauphine, OU=MIAGE, CN=Lab-CA"
else
    echo -e "${RED}   ❌ Failed to create CA certificate${NC}"
    exit 1
fi
echo ""

# Generate Reverse-Proxy Certificate
echo -e "${GREEN}🔐 Step 2/3: Generating Reverse-Proxy certificate...${NC}"
openssl req -newkey rsa:4096 -keyout reverse-proxy-key.pem -out reverse-proxy-csr.pem \
    -nodes \
    -subj "/C=FR/ST=IDF/L=Paris/O=Dauphine/OU=MIAGE/CN=10.100.100.10" \
    2>/dev/null

openssl x509 -req -in reverse-proxy-csr.pem \
    -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial \
    -out reverse-proxy-cert.pem -days 365 -sha256 \
    2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}   ✅ Reverse-Proxy certificate created successfully${NC}"
    echo -e "      Subject: C=FR, ST=IDF, L=Paris, O=Dauphine, OU=MIAGE, CN=10.100.100.10"
    echo -e "      Issuer: CN=Lab-CA"
else
    echo -e "${RED}   ❌ Failed to create Reverse-Proxy certificate${NC}"
    exit 1
fi
echo ""

# Generate Web-Server Certificate
echo -e "${GREEN}🔐 Step 3/3: Generating Web-Server certificate...${NC}"
openssl req -newkey rsa:4096 -keyout web-server-key.pem -out web-server-csr.pem \
    -nodes \
    -subj "/C=FR/ST=IDF/L=Paris/O=Dauphine/OU=MIAGE/CN=web-server" \
    2>/dev/null

openssl x509 -req -in web-server-csr.pem \
    -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial \
    -out web-server-cert.pem -days 365 -sha256 \
    2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}   ✅ Web-Server certificate created successfully${NC}"
    echo -e "      Subject: C=FR, ST=IDF, L=Paris, O=Dauphine, OU=MIAGE, CN=web-server"
    echo -e "      Issuer: CN=Lab-CA"
else
    echo -e "${RED}   ❌ Failed to create Web-Server certificate${NC}"
    exit 1
fi
echo ""

# Clean up CSR files (Certificate Signing Requests - no longer needed)
echo -e "${BLUE}🧹 Cleaning up temporary files...${NC}"
rm -f reverse-proxy-csr.pem web-server-csr.pem
echo ""

# Display generated files
echo -e "${GREEN}✅ Certificate generation complete!${NC}"
echo ""
echo -e "${BLUE}📋 Generated files:${NC}"
ls -lh ca-cert.pem ca-key.pem reverse-proxy-cert.pem reverse-proxy-key.pem web-server-cert.pem web-server-key.pem 2>/dev/null | awk '{print "   " $9 " (" $5 ")"}'
echo ""
echo -e "${GREEN}🎓 Certificates are ready for use in the lab!${NC}"
echo ""

