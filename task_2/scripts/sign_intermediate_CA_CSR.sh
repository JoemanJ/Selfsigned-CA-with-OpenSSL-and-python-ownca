#!/bin/bash
# This script will use the primary CA key and certificate generated using 
# [auto_]gen_selfsigned_CA.sh to sign the intermediate CA CSR generated using
# [auto_]gen_intermediate_CA_CSR.sh

cd "$(dirname "$0")"

openssl x509 -req \
             -days 3650 \
             -in ../reqs/int_CA.csr \
             -CA ../certs/CA.crt \
             -CAkey ../keys/CA.key \
             -CAcreateserial \
             -out ../certs/int_CA.crt \
             -extfile intermediate.cnf \
             -extensions v3_intermediate_ca