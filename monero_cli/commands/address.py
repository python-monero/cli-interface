import click
from monero.backends.jsonrpc import JSONRPCWallet
from monero.numbers import from_atomic
from monero.wallet import Wallet


COMMAND = "address"


def get_address(wallet: Wallet):
    return wallet.address()


def represent_simple_address(wallet: Wallet):
    return f"0 {get_address(wallet)} Primary address"


# @click.command()
# def main():
#     click.echo(represent_simple_address())
