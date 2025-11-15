#!/bin/bash
# This script will use the intermediate CA key and certificate generated using 
# [auto_]gen_intermediate_CA.sh to sign the server CSR generated using
# [auto_]gen_server_CSR.sh

# The generated certificate contains the server's sertificate, signed by the
# intermediate CA, bundled with the intermediate CA's certificate, signed by
# the main certificate

cd "$(dirname "$0")"

# Sign server CSR
openssl x509 -req -days 3650 -in ../reqs/server.csr -CA ../certs/int_CA.crt -CAkey ../keys/int_CA.key -CAcreateserial -out ../certs/server.crt -days 365 -sha256 -extfile v3.ext

# Concatenate intermediate CA's certificate
cat ../certs/server.crt ../certs/int_CA.crt > ../certs/server.chained.crt