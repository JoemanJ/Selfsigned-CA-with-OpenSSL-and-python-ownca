#!/bin/bash
# This script generates a new private key and certificate sign request for the CA
# The CSR is signed by the CA's own private key, that is, the CA is selfsigned
# 
# This script will prompt you for a password for the newly generated CA
# The password must be between 4 and 1024 characters long
# It will also prompt you for identifying information for the CA, such as country,
# estate, etc. 
# 
# The CA is created at "../certs/CA.crt"
# The CA private key is created at "../keys/CA.key"

cd "$(dirname "$0")"

mkdir ../keys
mkdir ../certs

openssl req -newkey rsa:4096 \
            -x509 \
            -sha256 \
            -days 3650 \
            -out ../certs/CA.crt \
            -keyout ../keys/CA.key \