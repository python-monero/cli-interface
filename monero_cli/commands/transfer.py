from decimal import Decimal
from typing import Iterable, Optional, Tuple, List

import click
from PyInquirer import prompt
from monero.address import address as monero_address
from monero.backends.jsonrpc import JSONRPCWallet
from monero.numbers import from_atomic
from monero.wallet import Wallet

from .. import settings
from ..exceptions import ValidationError


COMMAND = "transfer"

DEFAULT_RINGSIZE = 12

DEFAULT_PRIORITY = "normal"


class Destination:
    """
    Represents one of the address-amount recipient pairs.
    """

    def __init__(self, address: str, amount: str):
        self.address = monero_address(address)
        err = f"failed to parse address {address}"
        if settings.NETWORK.is_testnet() and not self.address.is_testnet():
            raise ValidationError(err)
        elif settings.NETWORK.is_stagenet() and not self.address.is_stagenet():
            raise ValidationError(err)
        elif settings.NETWORK.is_mainnet() and not self.address.is_mainnet():
            raise ValidationError(err)

        try:
            self.amount = Decimal(amount)
        except:
            err_msg = (
                f"amount is wrong: {address} {amount}, "
                "expected number from 0 to 18446744.073709551615"
            )
            raise ValidationError(err_msg)

    def to_tuple(self) -> tuple:
        return self.address, self.amount

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.address} {self.amount}>"


def parse_command(command: str) -> Tuple[Optional[int], str, list]:
    """
    Parses the command into its elements, extracting ring_size 
    and priority and destinations, if present.
    """
    args = command.split()
    if len(args) < 2:
        raise ValidationError("invalid number of arguments")

    try:
        ring = int(args[0])
        args = args[1:]
    except:
        ring = DEFAULT_RINGSIZE

    if args[0] in ["unimportant", "normal", "elevated", "priority"]:
        priority = args[0]
        args = args[1:]
    else:
        priority = DEFAULT_PRIORITY

    return ring, priority, args


def parse_destinations(*args: List[str]) -> List[Destination]:
    """
    Parses the list of traling arguments into Destinations, if valid.
    """
    if not args or len(args) % 2 != 0:
        raise ValidationError("invalid number of arguments")

    return [
        Destination(addr, amount)
        for addr, amount in zip(args[:-1:2], args[1::2])
    ]


def represent_result(transactions):
    header = "Transaction successfully submitted. Transactions:"
    txs_str = "\n".join(tx.hash for tx in transactions)
    return f"{header}\n{txs_str}"


def make_transfer(destinations: List[Destination], priority=DEFAULT_PRIORITY):
    wallet = Wallet(
        JSONRPCWallet(
            host=settings.RPC_WALLET_HOST,
            port=settings.RPC_WALLET_PORT,
            user=settings.RPC_WALLET_USER,
            password=settings.RPC_WALLET_PASSWORD,
            timeout=settings.RPC_WALLET_REQUESTS_TIMEOUT,
        )
    )
    return wallet.transfer_multiple(
        [dest.to_tuple() for dest in destinations], priority=priority
    )


def confirm_transfer(destinations: List[Destination]) -> bool:
    total = sum(dest.amount for dest in destinations)
    confirmation_text = f"Sending {total} xmr.\nIs this ok? (y/yes/n/no)"
    questions = [
        {"type": "input", "name": "confirmation", "message": confirmation_text}
    ]
    answer = prompt(questions).get("confirmation", "no")
    return answer.lower() in ["yes", "y"]


def transfer(wallet: Wallet, command: str):
    _, prio, args = parse_command(command)
    right_args_len = len(args) and len(args) % 2 == 0 and len(args) <= 30
    assert right_args_len, "Invalid number of arguments"
    destinations = list(parse_destinations(*args))
    if not confirm_transfer(destinations):
        return "Transfer cancelled"
    transfers = make_transfer(destinations, priority=prio)
    return represent_result(transfers)
