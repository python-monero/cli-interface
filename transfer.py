from decimal import Decimal
from typing import Iterable

import click
from monero.address import address as monero_address
from monero.backends.jsonrpc import JSONRPCWallet
from monero.numbers import from_atomic
from monero.wallet import Wallet

import settings


class Destination:
    def __init__(self, address: str, amount: str):
        self.address = monero_address(address)
        if settings.RPC_WALLET_TESTNET:
            err = f"Expected testnet address, got {address}"
            assert self.address.is_testnet(), err
        if settings.RPC_WALLET_STAGENET:
            err = f"Expected stagenet address, got {address}"
            assert self.address.is_stagenet(), err
        if not settings.RPC_WALLET_STAGENET:
            err = f"Expected mainnet address, got {address}"
            assert self.address.is_mainnet(), err

        self.amount = Decimal(amount)

    def to_tuple(self) -> tuple:
        return self.address, self.amount

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.address} {self.amount}>"


def parse_destinations(*args) -> Iterable[Destination]:
    assert len(args) % 2 == 0, "Expected pair number of arguments"
    for addr, amount in zip(args[:-1:2], args[1::2]):
        yield Destination(addr, amount)


def represent_result(transactions):
    header = "Transaction successfully submited. Transactions:"
    txs_str = "\n".join(tx.hash for tx in transactions)
    return f"{header}\n{txs_str}"


def transfer(*destinations: Destination):
    wallet = Wallet(
        JSONRPCWallet(
            host=settings.RPC_WALLET_HOST,
            port=settings.RPC_WALLET_PORT,
            user=settings.RPC_WALLET_USER,
            password=settings.RPC_WALLET_PASSWORD,
        )
    )
    return wallet.transfer_multiple([dest.to_tuple() for dest in destinations])


def confirm_transfer(*destinations: Destination) -> bool:
    total = sum(dest.amount for dest in destinations)
    confirmation_text = f"Sending {total} xmr.\nIs this ok? (y/yes/n/no)"
    click.echo(confirmation_text)
    answer = input()
    return answer.lower() in ["yes", "y"]


@click.command()
@click.argument("args", nargs=-1)
def main(args):
    right_args_len = len(args) % 2 == 0 and len(args) <= 30 and len(args)
    assert right_args_len, "Invalid number of arguments"
    destinations = list(parse_destinations(*args))
    if not confirm_transfer(*destinations):
        return click.echo("Transfer cancelled")
    transfers = transfer(*destinations)
    click.echo(represent_result(transfers))


if __name__ == "__main__":
    main()
