#!/usr/bin/env python3

import click
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ca_operations import create_root_ca, create_intermediate_ca
from cert_operations import generate_challenge, issue_server_certificate


# grupo principal de comandos
@click.group()
def cli():
    pass


@cli.command('init-root-ca')
@click.option('--common-name', default='rootca.com', help='Common Name (CN) do certificado')
@click.option('--organization', default='UFES', help='Nome da organização (O)')
@click.option('--organizational-unit', default='CT', help='Unidade organizacional (OU)')
@click.option('--country', default='BR', help='Código do país (C)')
@click.option('--locality', default='Vitoria', help='Localidade (L)')
@click.option('--state', default='ES', help='Estado/Província (ST)')
@click.option('--validity-days', default=365, type=int, help='Validade em dias')
def init_root_ca(common_name, organization, organizational_unit, country, locality, state, validity_days):
    try:
        # cria a CA raiz com os dados fornecidos
        create_root_ca(
            common_name=common_name,
            organization=organization,
            organizational_unit=organizational_unit,
            country=country,
            locality=locality,
            state=state,
            validity_days=validity_days
        )
    except Exception as e:
        click.echo(f"✗ Erro: {e}", err=True)
        sys.exit(1)


@cli.command('init-intermediate-ca')
@click.option('--common-name', default='intermediateca.com', help='Common Name (CN) do certificado')
@click.option('--organization', default='UFES', help='Nome da organização (O)')
@click.option('--organizational-unit', default='INF', help='Unidade organizacional (OU)')
@click.option('--country', default='BR', help='Código do país (C)')
@click.option('--locality', default='Vitoria', help='Localidade (L)')
@click.option('--state', default='ES', help='Estado/Província (ST)')
@click.option('--validity-days', default=365, type=int, help='Validade em dias')
def init_intermediate_ca(common_name, organization, organizational_unit, country, locality, state, validity_days):
    try:
        # cria a CA intermediaria com base na raiz
        create_intermediate_ca(
            common_name=common_name,
            organization=organization,
            organizational_unit=organizational_unit,
            country=country,
            locality=locality,
            state=state,
            validity_days=validity_days
        )
    except Exception as e:
        click.echo(f"✗ Erro: {e}", err=True)
        sys.exit(1)


@cli.command('generate-challenge')
@click.argument('domain')
def generate_challenge_cmd(domain):
    try:
        # gera desafio HTTP para o dominio
        generate_challenge(domain)
    except Exception as e:
        click.echo(f"✗ Erro: {e}", err=True)
        sys.exit(1)


@cli.command('issue-certificate')
@click.argument('domain')
@click.option('--organization', default='UFES', help='Nome da organização (O)')
@click.option('--organizational-unit', default='INF', help='Unidade organizacional (OU)')
@click.option('--country', default='BR', help='Código do país (C)')
@click.option('--locality', default='Vitoria', help='Localidade (L)')
@click.option('--state', default='ES', help='Estado/Província (ST)')
@click.option('--validity-days', default=365, type=int, help='Validade em dias')
def issue_certificate(domain, organization, organizational_unit, country, locality, state, validity_days):
    try:
        # emite certificado server usando CA intermediaria
        issue_server_certificate(
            domain=domain,
            organization=organization,
            organizational_unit=organizational_unit,
            country=country,
            locality=locality,
            state=state,
            validity_days=validity_days
        )
    except Exception as e:
        click.echo(f"✗ Erro: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
