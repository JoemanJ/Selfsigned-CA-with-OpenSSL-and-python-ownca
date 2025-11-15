#!/bin/bash
# This script generates a new private key and certificate sign request for the 
# intermediate CA
# 
# The CSR will be signed by the primary CA using another script
# 
# This script will prompt you for a password for the newly generated CA
# The password must be between 4 and 1024 characters long
# It will also prompt you for identifying information for the CA, such as country,
# estate, etc. 
# 
# The CA is created at "../certs/int_CA.crt"
# The CA private key is created at "../keys/int_CA.key"

cd "$(dirname "$0")"

mkdir -p ../keys
mkdir -p ../reqs

# Generate RSA key
openssl genrsa -out ../keys/int_CA.key 4096

# Generate CSR
openssl req -new \
            -key ../keys/int_CA.key \
            -out ../reqs/int_CA.csr \