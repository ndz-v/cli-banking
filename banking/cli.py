import os
from pathlib import Path

import click
import mechanicalsoup

from banking.credentials import Credentials
from banking.dataTable import DataTable
from banking.navigation import Navigation


@click.command()
# @click.option('--sp_credentials', '-csp', is_flag=True, required=False,
            #   help='Sparkassen Anmelde Daten erneut eingeben')
@click.option('--db_credentials', '-cdb', is_flag=True, required=False,
              help='Deutsche Bank Anmeldedaten Daten erneut eingeben')
def banking(db_credentials):
    creds = Credentials()
    # if not Path(creds.sp_credentialFile).is_file():
    #     creds.prompt_sp_credentials()
    #     return

    if not Path(creds.db_credentialFile).is_file():
        creds.prompt_db_credentials()
        return

    # if sp_credentials:
    #     click.echo(' Sparkassen Anmeldedaten erneuern.')
    #     creds.prompt_sp_credentials()
    #     return

    if db_credentials:
        click.echo(' Deutsche Bank Anmeldedaten erneuern.')
        creds.prompt_db_credentials()
        return

    DataTable()

    # test = Navigation()
    # test.navigate_db_page()
