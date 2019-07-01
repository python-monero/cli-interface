import sys
from PyInquirer import prompt, print_json

from .startup import connect_to_wallet
from .validation import CommandValidator
from .commands import balance
from .commands import help
from .commands.address import get_address
from .commands import version
from .commands import refresh
from .commands import exit


def entry_point():
    wallet = connect_to_wallet()

    questions = [
        {
            'type': 'input',
            'name': 'command',
            'message': f'[wallet {str(get_address(wallet))[:5]}]',
            'validate': CommandValidator,
        }
    ]

    while 1:
        answers = prompt(questions)
        command = answers.get('command')
        if command == exit.COMMAND:
            exit.exit()
        elif command == help.COMMAND:
            print(help.get_help())
        elif command == balance.COMMAND:
            print(balance.get_simple_balance(wallet))
        elif command == version.COMMAND:
            print(version.get_version(wallet))
        elif command == refresh.COMMAND:
            refresh.refresh(wallet)

    