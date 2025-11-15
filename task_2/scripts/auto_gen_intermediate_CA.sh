#!/bin/bash
# This script generates a new private key and certificate sign request for the
# intermediate CA. 
#
# The CSR will be signed by the primary CA using another script.
# 
# This script is similar to gen_intermediate_CA.sh, except it will not ask you
# for a password or identifying information. It will use the default identifying 
# information provided by the -subj parameter and no password
#
# Keep in mind this is for demonstration purposes only! You should always use 
# strong passwords and correct identifying information for your CAs
# 
# The default values used here are:
#   Country:            BR
#   State/Province:     Espirito Santo
#   Locality:           Vitoria
#   Organization:       UFES - Universidade Federal do Espirito Santo
#   Organization unit:  CT
#   Common name:        MaisSegurancaEmComputacao.com
#   Email:              [none]
#
# The CSR is created at "../reqs/int_CA.crt"
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
            -subj "/C=BR/ST=Espirito Santo/L=Vitoria/O=UFES - Universidade Federal do Espirito Santo/OU=CT/CN=MaisSegurancaEmComputacao.com"