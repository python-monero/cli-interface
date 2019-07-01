from monero.backends.jsonrpc import JSONRPCWallet
from monero.numbers import from_atomic
from monero.wallet import Wallet


COMMAND = 'balance'


def get_balance(wallet: Wallet, details=False):
    return wallet.balances()


def get_simple_balance(wallet: Wallet):
    total, unlocked = get_balance(wallet)
    return f"Balance: {total}, unlocked balance: {unlocked}"


def get_detailed_balance():
    raise NotImplementedError()

