#!/bin/bash
# This script generates a new private key and certificate sign request for the CA
# The CSR is signed by the CA's own private key, that is, the CA is selfsigned
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
            -nodes \
            -out ../certs/CA.crt \
            -keyout ../keys/CA.key \
            -subj "/C=BR/ST=Espirito Santo/L=Vitoria/O=UFES - Universidade Federal do Espirito Santo/OU=CT/CN=SegurancaEmComputacao.com"