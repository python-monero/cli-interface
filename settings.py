import os

RPC_WALLET_HOST = os.environ["RPC_WALLET_HOST"]
RPC_WALLET_PORT = os.environ["RPC_WALLET_PORT"]
RPC_WALLET_USER = os.environ.get("RPC_WALLET_USER")
RPC_WALLET_PASSWORD = os.environ.get("RPC_WALLET_PASSWORD")
RPC_WALLET_STAGENET = bool(os.environ.get("RPC_WALLET_STAGENET", 1))
RPC_WALLET_TESTNET = bool(os.environ.get("RPC_WALLET_TESTNET", 0))
RPC_WALLET_REQUESTS_TIMEOUT = int(
    os.environ.get("RPC_WALLET_REQUESTS_TIMEOUT", 30)
)
