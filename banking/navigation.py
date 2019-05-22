import base64
import errno
import json
import os
import re
from pathlib import Path

import click
import mechanicalsoup

from banking.credentials import Credentials


class Navigation:

    DB_LOGIN_URL = "https://meine.deutsche-bank.de/trxm/db/init.do"

    def navigate_page(self):
        browser = mechanicalsoup.StatefulBrowser(
            soup_config={'features': 'lxml'},
            raise_on_404=True
        )
        result = browser.open(self.DB_LOGIN_URL)

        if result.status_code != 200:
            click.echo(' Überprüfen Sie ihre Internetverbindung.')
            exit()

        browser.select_form('form[id="loginForm"]')

        page = browser.get_current_page()

        branch_tag = page.find('input', attrs={'id': 'branch'})
        account_tag = page.find('input', attrs={'id': 'account'})
        sub_account_tag = page.find('input', attrs={'id': 'subAccount'})
        pin_tag = page.find('input', attrs={'id': 'pin'})

        creds = Credentials().get_credentials()

        branch = creds['branch']
        account = creds['account']
        sub_account = creds['sub_account']
        pin = click.prompt(' PIN', hide_input=True)

        browser[branch_tag['id']] = branch
        browser[account_tag['id']] = account
        browser[sub_account_tag['name']] = sub_account
        browser[pin_tag['id']] = pin

        result = browser.submit_selected()

        if result.status_code != 200:
            click.echo(' Anmelde Daten sind falsch!')
            exit()

        page = browser.get_current_page()

        modal_form = page.find(
            'form', attrs={'id': 'displayNachrichtenboxForm'})

        if modal_form:
            browser.select_form('form[id="displayNachrichtenboxForm"]')
            browser.submit_selected()

        page = browser.get_current_page()

        link = page.find_all('a', attrs={'class': 'visuallyEnhanced'})

        result = browser.follow_link(link[0])

        page = browser.get_current_page()
        return page
