#!/bin/bash
# This script will use the CA key and certificate generated using 
# [auto_]gen_selfsigned_CA.sh to sign the server CSR generated using
# [auto_]gen_server_CSR.sh

cd "$(dirname "$0")"

openssl x509 -req -days 3650 -in ../reqs/server.csr -CA ../certs/CA.crt -CAkey ../keys/CA.key -CAcreateserial -out ../certs/server.crt