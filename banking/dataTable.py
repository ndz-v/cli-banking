import re

import click

from banking.navigation import Navigation


class DataTable:

    def __init__(self):
        db_balance = self.get_position()

        click.secho(f'\n{"Deutsche Bank"}')
        click.secho(f'\n{db_balance}\n')

    def get_position(self):
        page = Navigation().navigate_page()

        date = page.find_all('td', attrs={'class': 'roll', 'colspan': '4'})
        date = date[0].text
        date = date.strip()

        balance = page.find_all(
            'td', attrs={'class': 'balance credit', 'headers': 'oB'})

        if not balance:
            balance = page.find_all(
                'td', attrs={'class': 'balance credit', 'headers': 'aB'})

        balance = balance[len(balance)-1].text
        balance = balance.strip()

        return balance
