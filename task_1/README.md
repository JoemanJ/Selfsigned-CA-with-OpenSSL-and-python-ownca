# PKI com Python - Tarefa 1

Sistema de PKI completo usando Python e cryptography: CA Raiz + CA Intermediária + Emissão de certificados com validação HTTP.

## Instalação

```bash
cd python
pip install -r requirements.txt
```

## Uso

### 1. Criar CA Raiz

```bash
python pki_manager.py init-root-ca
```

Cria `certs/CA.pem` e `keys/CA.key` (RSA 4096 bits, autoassinado).

Parâmetros opcionais:
- `--common-name` (default `rootca.com`)
- `--organization` (default `UFES`)
- `--organizational-unit` (default `CT`)
- `--country` (default `BR`)
- `--locality` (default `Vitoria`)
- `--state` (default `ES`)
- `--validity-days` (default `365`)


### 2. Criar CA Intermediária

```bash
python pki_manager.py init-intermediate-ca
```

Cria `certs/intermediate_CA.pem` e `keys/intermediate_CA.key` (RSA 4096 bits, assinado pela Raiz).

Parâmetros opcionais:
- `--common-name` (default `intermediateca.com`)
- `--organization` (default `UFES`)
- `--organizational-unit` (default `INF`)
- `--country` (default `BR`)
- `--locality` (default `Vitoria`)
- `--state` (default `ES`)
- `--validity-days` (default `365`)


### 3. Gerar Desafio para Domínio

```bash
python pki_manager.py generate-challenge localhost
```

Gera um token (GUID), salva internamente e mostra as instruções:
- Criar arquivo `challenges/.well-known/acme-challenge/<token>.txt` no servidor
- Conteúdo: `<token>.<domínio>`

### 4. Emitir Certificado

```bash
python pki_manager.py issue-certificate localhost
```

Valida o desafio (busca o token salvo internamente) fazendo requisição HTTP e emite o certificado se válido.

Cria:
- `certs/server.crt` - Certificado do servidor
- `certs/server.chained.crt` - Cadeia completa (server + intermediate)
- `keys/server.key` - Chave privada (RSA 4096 bits)

Parâmetros adicionais:
- `--organization` (default `UFES`)
- `--organizational-unit` (default `INF`)
- `--country` (default `BR`)
- `--locality` (default `Vitoria`)
- `--state` (default `ES`)
- `--validity-days` (default `365`)


## Fluxo Completo

```bash
# 1. Setup das CAs
python pki_manager.py init-root-ca
python pki_manager.py init-intermediate-ca

# 2. Gerar desafio (CA salva o token internamente)
python pki_manager.py generate-challenge localhost

# 3. No servidor, criar arquivo:
# challenges/.well-known/acme-challenge/<token>.txt
# com conteúdo: <token>.localhost

# 4. Emitir certificado (CA valida o token que ela gerou)
python pki_manager.py issue-certificate localhost
```

## Servidor Nginx

**IMPORTANTE:** Os arquivos já vêm configurados para iniciar apenas com HTTP. As linhas de certificado e o bloco HTTPS estão comentados.

1. **Inicie o servidor:**
```bash
cd docker
docker-compose up -d
```

O servidor inicia apenas com HTTP (porta 80) para servir os desafios.

2. **Após emitir o certificado**, descomente as linhas no `docker/docker-compose.yml`:
```yaml
# - ../certs/server.chained.crt:/etc/nginx/ssl/server.chained.crt
# - ../keys/server.key:/etc/nginx/ssl/server.key
```

E descomente o bloco HTTPS no `docker/nginx.conf`, depois reinicie:
```bash
docker-compose restart
```

Acessa `https://localhost` após emitir o certificado (importar `certs/CA.pem` no navegador primeiro).

## Verificação da Hierarquia de Certificados

Use `openssl verify` para verificar a cadeia de certificação:

```bash
openssl verify -CAfile certs/CA.pem -untrusted certs/intermediate_CA.pem certs/server.chained.crt
```

O comando deve retornar `OK` se a hierarquia estiver correta.

## Validação HTTP

A CA armazena os desafios pendentes em `certs/challenges.json`.

Quando você executa `issue-certificate`, a CA:
1. Busca o token que ela gerou para aquele domínio
2. Faz requisição GET para: `http://<domínio>/.well-known/acme-challenge/<token>.txt`
3. Verifica se o conteúdo é: `<token>.<domínio>`
4. Emite o certificado se válido

Simula o protocolo ACME HTTP-01 do Let's Encrypt.

## Comandos

- `init-root-ca` - Cria CA Raiz
- `init-intermediate-ca` - Cria CA Intermediária  
- `generate-challenge <domain>` - Gera e salva token de validação
- `issue-certificate <domain>` - Valida token e emite certificado
