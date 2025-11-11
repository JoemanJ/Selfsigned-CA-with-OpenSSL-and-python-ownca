#!/bin/bash
# This script generates a new private key and certificate sign request for the 
# server
# 
# The generated CSR is not selfsigned and must be signed by the CA afterwards
# by using the sign_server_CSR.sh script
#
# The server request is created at "../reqs/server.req"
# The server private key is created at "../keys/server.key"

cd "$(dirname "$0")"

mkdir -p ../keys
mkdir -p ../reqs

# Generate RSA key
openssl genrsa -out ../keys/server.key 4096

# Generate CSR
openssl req -new \
            -key ../keys/server.key \
            -out ../reqs/server.csr \
            -subj "/C=BR/ST=Espirito Santo/L=Vitoria/O=UFES - Universidade Federal do Espirito Santo/OU=CT/CN=localhost"