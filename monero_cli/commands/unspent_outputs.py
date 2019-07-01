import click
from monero.backends.jsonrpc import JSONRPCWallet
from monero.numbers import from_atomic
from monero.wallet import Wallet

import settings


def get_unspent_outputs():
    wallet = Wallet(
        JSONRPCWallet(
            host=settings.RPC_WALLET_HOST,
            port=settings.RPC_WALLET_PORT,
            user=settings.RPC_WALLET_USER,
            password=settings.RPC_WALLET_PASSWORD,
            timeout=settings.RPC_WALLET_REQUESTS_TIMEOUT,
        )
    )
    return wallet.get_unspent_outputs()


def represent_outputs():
    outputs = get_unspent_outputs()
    outputs.sort(key=lambda elem: elem.atomic_amount)

    total_count = f"Total count: {len(outputs)}"

    smallest = "Min amount found: {:f}".format(outputs[0].amount)
    largest = "Max amount found: {:f}".format(outputs[-1].amount)
    return f"{total_count}\n{smallest}\n{largest}"


@click.command()
def main():
    click.echo(represent_outputs())


if __name__ == "__main__":
    main()
