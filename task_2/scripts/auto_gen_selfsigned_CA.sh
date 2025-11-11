#!/bin/bash
# This script generates a new private key and certificate sign request for the CA
# The CSR is signed by the CA's own private key, that is, the CA is selfsigned
# 
# This script is similar to gen_selfsigned_CA.sh, except it will not ask you for
# a password or identifying information. It will use the default identifying 
# information provided by the -subj parameter and no password
#
# Keep in mind this is for demonstration purposes only! You should always use 
# strong passwords and correct identifying information for your CAs
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