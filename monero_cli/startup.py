from monero.backends.jsonrpc import JSONRPCWallet
from monero.numbers import from_atomic
from monero.wallet import Wallet
from . import settings


def connect_to_wallet():
    """
    Connects to the wallet RPC interface, with the configuration provided
    by the settings module.
    """
    return Wallet(
        JSONRPCWallet(
            host=settings.RPC_WALLET_HOST,
            port=settings.RPC_WALLET_PORT,
            user=settings.RPC_WALLET_USER,
            password=settings.RPC_WALLET_PASSWORD,
            timeout=settings.RPC_WALLET_REQUESTS_TIMEOUT,
        )
    )
