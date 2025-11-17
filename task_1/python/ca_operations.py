import os
import datetime
from pathlib import Path

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Helper functions para chaves e certificados

def generate_private_key(key_path, key_size=4096):
    """Gera e salva uma chave privada RSA."""
    # gera chave com expoente fixo e grava em PEM
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size
    )
    with open(key_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    return private_key

def load_private_key(key_path):
    """Carrega uma chave privada RSA."""
    # leitura simples do arquivo PEM
    with open(key_path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def load_certificate(cert_path):
    """Carrega um certificado X.509."""
    # abre o arquivo PEM do certificado
    with open(cert_path, "rb") as f:
        return x509.load_pem_x509_certificate(f.read())

def get_project_paths():
    base_dir = Path(__file__).parent.parent
    certs_dir = base_dir / 'certs'
    keys_dir = base_dir / 'keys'
    
    # garante existencia dos diretorios base
    certs_dir.mkdir(exist_ok=True)
    keys_dir.mkdir(exist_ok=True)
    
    return {'certs': certs_dir, 'keys': keys_dir}


def create_root_ca(
    common_name="rootca.com",
    organization="UFES",
    organizational_unit="CT",
    country="BR",
    locality="Vitoria",
    state="ES",
    validity_days=365
):
    paths = get_project_paths()
    key_path = paths['keys'] / 'CA.key'
    cert_path = paths['certs'] / 'CA.pem'

    if key_path.exists() and cert_path.exists():
        print("CA Raiz já existe.")
        return load_certificate(cert_path), load_private_key(key_path)

    # gera novo par de chaves para a raiz
    private_key = generate_private_key(key_path)
    public_key = private_key.public_key()

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, country),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
        x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, organizational_unit),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])

    cert_builder = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        public_key
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=validity_days)
    ).add_extension(
        x509.SubjectKeyIdentifier.from_public_key(public_key),
        critical=False
    ).add_extension(
        x509.BasicConstraints(ca=True, path_length=None),
        critical=True
    )

    # assina o certificado com a propria chave
    certificate = cert_builder.sign(private_key, hashes.SHA256())

    with open(cert_path, "wb") as f:
        f.write(certificate.public_bytes(serialization.Encoding.PEM))

    print(f"\n✓ CA Raiz criada com sucesso!")
    print(f"  Certificado: {cert_path}")
    print(f"  Chave privada: {key_path}")
    
    return certificate, private_key


def create_intermediate_ca(
    common_name="intermediateca.com",
    organization="UFES",
    organizational_unit="INF",
    country="BR",
    locality="Vitoria",
    state="ES",
    validity_days=365
):
    paths = get_project_paths()
    root_cert_path = paths['certs'] / 'CA.pem'
    root_key_path = paths['keys'] / 'CA.key'
    
    if not (root_cert_path.exists() and root_key_path.exists()):
        raise FileNotFoundError("CA Raiz não encontrada. Crie a CA Raiz primeiro.")

    root_cert = load_certificate(root_cert_path)
    root_key = load_private_key(root_key_path)

    int_key_path = paths['keys'] / 'intermediate_CA.key'
    int_cert_path = paths['certs'] / 'intermediate_CA.pem'

    if int_key_path.exists() and int_cert_path.exists():
        print("CA Intermediária já existe.")
        return load_certificate(int_cert_path), load_private_key(int_key_path)

    # gera chaves para a CA intermediaria
    private_key = generate_private_key(int_key_path)
    public_key = private_key.public_key()

    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, country),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
        x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, organizational_unit),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])

    cert_builder = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        root_cert.subject
    ).public_key(
        public_key
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=validity_days)
    ).add_extension(
        x509.SubjectKeyIdentifier.from_public_key(public_key),
        critical=False
    ).add_extension(
        x509.AuthorityKeyIdentifier.from_issuer_public_key(root_cert.public_key()),
        critical=False
    ).add_extension(
        x509.BasicConstraints(ca=True, path_length=0),
        critical=True
    )

    certificate = cert_builder.sign(root_key, hashes.SHA256())

    with open(int_cert_path, "wb") as f:
        f.write(certificate.public_bytes(serialization.Encoding.PEM))

    print(f"\n✓ CA Intermediária criada com sucesso!")
    print(f"  Certificado: {int_cert_path}")
    print(f"  Chave privada: {int_key_path}")
    
    return certificate, private_key

