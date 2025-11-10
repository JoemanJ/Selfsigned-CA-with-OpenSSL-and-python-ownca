- o comando abaixo starta o container do Docker com o Nginx. (dentro da pasta docker)
```sh
docker-compose up -d
```

- O comando abaixo derruba o container do Docker com o Nginx.
```sh
docker-compose down
```

- O servidor espera os arquivos de nome `selfsigned.crt` e `selfsigned.key` na pasta `task_2/certs`.
- O servidor deve funcionar se as certificações estiverem corretas.

- Gerei chaves usando o comando [Fonte](https://linuxize.com/post/creating-a-self-signed-ssl-certificate/):
```sh

openssl req -newkey rsa:4096 \
            -x509 \
            -sha256 \
            -days 3650 \
            -nodes \
            -out task_2/certs/selfsigned.crt \
            -keyout task_2/certs/selfsigned.key
```



- Acessa o servidor Nginx via HTTPS:
```sh
https://localhost
```

- [Esse link mostra como configurar um servidor HTTPS no Nginx](https://nginx.org/en/docs/http/configuring_https_servers.html)
- [Esse outro mostra como gerar um certificado com openSSL e colocar no Nginx](https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-nginx-in-ubuntu-18-04)
- Misturei conceitos