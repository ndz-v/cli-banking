import re

import click

from banking.navigation import Navigation


class DataTable:

    def __init__(self):
        # sp_balance = self.get_sp_position()
        db_balance = self.get_db_position()

        click.secho(f'\n{"Deutsche Bank"}')
        click.secho(f'\n{db_balance}\n')

    def get_db_position(self):
        page = Navigation().navigate_db_page()

        date = page.find_all('td', attrs={'class': 'roll', 'colspan': '4'})
        date = date[0].text
        date = date.strip()

        balance = page.find_all(
            'td', attrs={'class': 'balance credit', 'headers': 'oB'})

        if not balance:
            balance = page.find_all(
                'td', attrs={'class': 'balance credit', 'headers': 'aB'})

        # if not balance:
            # balance = page.find_all('td', attrs={'class': 'balance credit', 'headers': 'aB'})
            # balance = balance[len(balance)-1]

        balance = balance[len(balance)-1].text
        balance = balance.strip()

        return balance

    # def get_sp_position(self):

    #     page = Navigation().navigate_sp_page()

    #     tables = page.find_all('table')

    #     positionsIndex = len(tables) - 1
    #     # valueIndex = len(tables) - 2

    #     positionsTable = tables[positionsIndex].find_all('tr')
    #     currentValueText = positionsTable[0].get_text().strip().split()

    #     return currentValueText[3]
    #     # click.secho(f'\nSparkasse Ulm')

    #     click.secho(f'\nKontostand: {currentValueText[3]} {currentValueText[4]}')

        # for row in tables[valueIndex].find_all('tr'):
        #     text = row.get_text().strip().replace('\t', '').replace('\n', ' ')
        #     text = re.sub('  +', ' ', text)
        #     print(text)

        # if len(positionsTable) == 4:
        #     print()
        #     return

        # del positionsTable[0]
        # del positionsTable[0]
        # del positionsTable[len(positionsTable) - 1]

        # tableHeader = f'{"Buchung":<10} | {"Wertstellung"} | {"Betrag":>15} | {"Verwendungszweck":>34}'
        # click.echo()
        # click.secho(f'{"":-^80s}', fg='white', bold=True)
        # click.secho(tableHeader, bold=True)
        # click.secho(f'{"":-^80s}', fg='white', bold=True)

        # count = 0
        # for row in positionsTable:
        #     count += 1
        #     reasons = row.get_text('<wbr/>', ' ').replace('­<wbr/>', '').split('<wbr/>')

        #     row = row.get_text().replace('<br/>', ' ').splitlines()
        #     value = row[4].replace(',', '.').replace('EUR', '')
        #     value = float(value)

        #     color = ''

        #     if value <= 0:
        #         color = 'red'
        #     else:
        #         color = 'green'

        #     formatedRow = f'{row[1]} | {row[2]:<12} | {row[4]:>15} | {reasons[2]:>34}'
        #     click.secho(formatedRow, fg=color)
        #     formatedRow = f'{"":<10} | {"":<12} | {"":>15} | {reasons[3][:34]:>34}'
        #     click.secho(formatedRow, fg=color)
        #     formatedRow = f'{"":<10} | {"":<12} | {"":>15} | {reasons[4][:30]:>34}'
        #     click.secho(formatedRow, fg=color)
        #     formatedRow = f'{"":-^80s}'
        #     click.secho(formatedRow, fg=color)
        #     if (count == 10):
        #         exit()
