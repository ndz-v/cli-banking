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

    # SP_LOGIN_URL = "https://www.sparkasse-ulm.de/de/home.html"
    DB_LOGIN_URL = "https://meine.deutsche-bank.de/trxm/db/init.do"

    def navigate_db_page(self):
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

        creds = Credentials().get_db_credentials()

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

    # def navigate_sp_page(self):
    #     browser = mechanicalsoup.StatefulBrowser(
    #         soup_config={'features': 'lxml'},
    #         raise_on_404=True
    #     )
    #     result = browser.open(self.SP_LOGIN_URL)

    #     if result.status_code != 200:
    #         click.echo(' Überprüfen Sie ihre Internetverbindung.')
    #         exit()

    #     browser.select_form('form[class="header-login"]')
    #     page = browser.get_current_page()
    #     user_input = page.find_all(
    #         'input', attrs={'value': '', 'maxlength': '16'})
    #     password_input = page.find_all(
    #         'input', attrs={'value': '', 'maxlength': '5'})

    #     user_attribute_name = user_input[0]['name']
    #     password_attribute_name = password_input[0]['name']

    #     creds = Credentials().get_sp_credentials()
    #     username = creds['username']
    #     password = click.prompt(' PIN', hide_input=True)

    #     browser[user_attribute_name] = username
    #     browser[password_attribute_name] = password
    #     result = browser.submit_selected()

    #     if result.status_code != 200:
    #         click.echo(' Anmelde Daten sind falsch!')
    #         exit()

    #     page = browser.get_current_page()

    #     link = page.find('a', text='Umsätze abrufen')
    #     result = browser.follow_link(link)

    #     page = browser.get_current_page()
    #     return page
