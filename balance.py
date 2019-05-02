import click
from monero.backends.jsonrpc import JSONRPCWallet
from monero.numbers import from_atomic
from monero.wallet import Wallet

import settings


def get_balance(details=False):
    wallet = Wallet(
        JSONRPCWallet(
            host=settings.RPC_WALLET_HOST,
            port=settings.RPC_WALLET_PORT,
            user=settings.RPC_WALLET_USER,
            password=settings.RPC_WALLET_PASSWORD,
            timeout=settings.RPC_WALLET_REQUESTS_TIMEOUT,
        )
    )
    return wallet.balances()


def represent_simple_balance():
    total, unlocked = get_balance()
    return f"Balance: {total}, unlocked balance: {unlocked}"


def represent_detailed_balance():
    raise NotImplementedError()


@click.command()
@click.option(
    "--details", is_flag=True, help="Whether to include per-subaddress details"
)
def main(details):
    if not details:
        balance = represent_simple_balance()
    else:
        balance = represent_detailed_balance()

    click.echo(balance)


if __name__ == "__main__":
    main()
