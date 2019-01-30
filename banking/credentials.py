import base64
import errno
import json
import os
from pathlib import Path

import click


class Credentials:

    path = os.path.abspath(__file__)
    db_credentialFile = os.path.dirname(path) + '/credentials.json'

    def prompt_db_credentials(self):
        try:
            if click.confirm(' Wollen Sie die Anmeldedaten eingeben?', abort=True):
                branch = click.prompt(' Branch')
                account = click.prompt(' Account')
                sub_account = click.prompt(' Sub-Account')

                data = {
                    'branch': str(base64.b64encode(bytes(branch, 'UTF-8')), 'UTF-8'),
                    'account': str(base64.b64encode(bytes(account, 'UTF-8')), 'UTF-8'),
                    'sub_account': str(base64.b64encode(bytes(sub_account, 'UTF-8')), 'UTF-8')
                }

                with open(self.db_credentialFile, 'w') as outfile:
                    json.dump(data, outfile)

        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    def get_db_credentials(self):
        if Path(self.db_credentialFile).is_file():
            try:
                with open(self.db_credentialFile) as creds:
                    data = json.load(creds)
                    branch = str(base64.b64decode(data['branch']), 'UTF-8')
                    account = str(base64.b64decode(data['account']), 'UTF-8')
                    sub_account = str(base64.b64decode(
                        data['sub_account']), 'UTF-8')

                    encodedData = {
                        'branch': branch,
                        'account': account,
                        'sub_account': sub_account
                    }

                    return encodedData
            except OSError as exco:
                if exco.errno != errno.EEXIST:
                    raise

    # def prompt_sp_credentials(self):
    #     try:
    #         if click.confirm(' Wollen Sie die Anmeldedaten eingeben?', abort=True):
    #             username = click.prompt(' Konto Name')
    #             password = click.prompt(' Passwort', hide_input=True)

    #             data = {
    #                 'username': str(base64.b64encode(bytes(username, 'UTF-8')), 'UTF-8'),
    #             }

    #             with open(self.sp_credentialFile, 'w') as outfile:
    #                 json.dump(data, outfile)

    #     except OSError as exc:
    #         if exc.errno != errno.EEXIST:
    #             raise

    # def get_sp_credentials(self):
    #     if Path(self.sp_credentialFile).is_file():
    #         try:
    #             with open(self.sp_credentialFile) as creds:
    #                 data = json.load(creds)
    #                 username = str(base64.b64decode(data['username']), 'UTF-8')

    #                 encodedData = {
    #                     'username': username
    #                 }

    #                 return encodedData
    #         except OSError as exco:
    #             if exco.errno != errno.EEXIST:
    #                 raise
