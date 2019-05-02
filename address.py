import click
from monero.backends.jsonrpc import JSONRPCWallet
from monero.numbers import from_atomic
from monero.wallet import Wallet

import settings


def get_address():
    wallet = Wallet(
        JSONRPCWallet(
            host=settings.RPC_WALLET_HOST,
            port=settings.RPC_WALLET_PORT,
            user=settings.RPC_WALLET_USER,
            password=settings.RPC_WALLET_PASSWORD,
        )
    )
    return wallet.address()


def represent_simple_address():
    return f"0 {get_address()} Primary address"


@click.command()
def main():
    click.echo(represent_simple_address())


if __name__ == "__main__":
    main()
