from monero.backends.jsonrpc import JSONRPCWallet
from monero.wallet import Wallet


COMMAND = "version"


def get_version(wallet: Wallet):
    return wallet.get_version()
