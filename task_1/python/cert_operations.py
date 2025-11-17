import uuid
import json
import requests
import datetime
from pathlib import Path

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from ca_operations import (
    get_project_paths, 
    generate_private_key, 
    load_certificate, 
    load_private_key
)


def get_challenges_file():
    paths = get_project_paths()
    # Certifique-se de que o diretório 'certs' exista
    paths['certs'].mkdir(exist_ok=True)
    return paths['certs'] / 'challenges.json'


def load_challenges():
    challenges_file = get_challenges_file()
    if challenges_file.exists():
        with open(challenges_file, 'r') as f:
            return json.load(f)
    return {}


def save_challenges(challenges):
    challenges_file = get_challenges_file()
    with open(challenges_file, 'w') as f:
        json.dump(challenges, f, indent=2)


def generate_challenge(domain):
    challenge_token = str(uuid.uuid4())
    challenge_content = f"{challenge_token}.{domain}"
    
    challenges = load_challenges()
    challenges[domain] = {
        'token': challenge_token,
        'content': challenge_content
    }
    save_challenges(challenges)
    
    print(f"\n{'='*60}")
    print(f"DESAFIO GERADO PARA: {domain}")
    print(f"{'='*60}")
    print(f"\nToken: {challenge_token}")
    print(f"\n1. Crie o arquivo no seu servidor:")
    print(f"   Caminho: .well-known/acme-challenge/{challenge_token}.txt")
    print(f"   Conteúdo: {challenge_content}")
    print(f"\n2. Certifique-se que está acessível em:")
    print(f"   http://{domain}/.well-known/acme-challenge/{challenge_token}.txt")
    print(f"\n3. Emita o certificado:")
    print(f"   python pki_manager.py issue-certificate {domain}")
    print(f"{'='*60}\n")


def validate_challenge(domain):
    challenges = load_challenges()
    
    if domain not in challenges:
        print(f"✗ Nenhum desafio pendente para {domain}")
        print(f"  Execute: python pki_manager.py generate-challenge {domain}")
        return False
    
    challenge = challenges[domain]
    token = challenge['token']
    expected_content = challenge['content']
    
    url = f"http://{domain}/.well-known/acme-challenge/{token}.txt"
    
    print(f"Validando desafio para {domain}...")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, timeout=5)
        
        if response.status_code != 200:
            print(f"✗ Falha: HTTP {response.status_code}")
            return False
        
        content = response.text.strip()
        
        if content == expected_content:
            print(f"✓ Desafio validado!")
            return True
        else:
            print(f"✗ Conteúdo incorreto")
            print(f"  Esperado: {expected_content}")
            print(f"  Recebido: {content}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Erro ao acessar URL: {e}")
        return False


def issue_server_certificate(
    domain,
    organization="UFES",
    organizational_unit="INF",
    country="BR",
    locality="Vitoria",
    state="ES",
    validity_days=365
):
    paths = get_project_paths()
    
    print(f"\n[1/3] Validando desafio HTTP...")
    if not validate_challenge(domain):
        raise ValueError("Validação falhou.")
    
    print(f"\n[2/3] Carregando CA Intermediária...")
    int_cert_path = paths['certs'] / 'intermediate_CA.pem'
    int_key_path = paths['keys'] / 'intermediate_CA.key'

    if not (int_cert_path.exists() and int_key_path.exists()):
        raise FileNotFoundError("CA Intermediária não encontrada.")

    intermediate_ca_cert = load_certificate(int_cert_path)
    intermediate_ca_key = load_private_key(int_key_path)

    print(f"\n[3/3] Emitindo certificado para {domain}...")
    
    server_key_path = paths['keys'] / 'server.key'
    server_cert_path = paths['certs'] / 'server.crt'
    
    private_key = generate_private_key(server_key_path)
    public_key = private_key.public_key()

    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, country),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
        x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, organizational_unit),
        x509.NameAttribute(NameOID.COMMON_NAME, domain),
    ])

    san_list = [x509.DNSName(domain)]
    if not domain.startswith("*."):
        san_list.append(x509.DNSName(f"*.{domain}"))
    san_list.append(x509.DNSName("localhost"))

    cert_builder = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        intermediate_ca_cert.subject
    ).public_key(
        public_key
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=validity_days)
    ).add_extension(
        x509.SubjectAlternativeName(san_list),
        critical=False,
    ).add_extension(
        x509.BasicConstraints(ca=False, path_length=None),
        critical=True
    )

    certificate = cert_builder.sign(intermediate_ca_key, hashes.SHA256())

    with open(server_cert_path, "wb") as f:
        f.write(certificate.public_bytes(serialization.Encoding.PEM))

    # Criar a cadeia de certificados
    chained_cert_path = paths['certs'] / 'server.chained.crt'
    with open(chained_cert_path, 'wb') as f_chain:
        f_chain.write(certificate.public_bytes(serialization.Encoding.PEM))
        f_chain.write(b'\n')
        f_chain.write(intermediate_ca_cert.public_bytes(serialization.Encoding.PEM))

    challenges = load_challenges()
    if domain in challenges:
        del challenges[domain]
        save_challenges(challenges)
    
    print(f"\n✓ Certificado emitido!")
    print(f"  Cert: {server_cert_path}")
    print(f"  Key: {server_key_path}")
    print(f"  Chain: {chained_cert_path}")
    
    return certificate, private_key



