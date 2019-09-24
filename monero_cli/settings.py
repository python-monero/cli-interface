import os

RPC_WALLET_HOST = os.environ.get("RPC_WALLET_HOST", "localhost")
RPC_WALLET_PORT = os.environ.get("RPC_WALLET_PORT", 38083)
RPC_WALLET_USER = os.environ.get("RPC_WALLET_USER", "")
RPC_WALLET_PASSWORD = os.environ.get("RPC_WALLET_PASSWORD", "")


class Network:
    TESTNET = "testnet"
    STAGENET = "stagenet"
    MAINNET = "mainnet"

    def __init__(self, value: str):
        valid_networks = [self.TESTNET, self.STAGENET, self.MAINNET]
        if value.lower() not in valid_networks:
            raise Exception(f"Invalid network value: {value}")
        self.value = value

    def is_mainnet(self) -> bool:
        return self.value == self.MAINNET

    def is_stagenet(self) -> bool:
        return self.value == self.STAGENET

    def is_testnet(self) -> bool:
        return self.value == self.TESTNET


NETWORK = Network(os.environ.get("NETWORK", Network.STAGENET))

RPC_WALLET_REQUESTS_TIMEOUT = int(
    os.environ.get("RPC_WALLET_REQUESTS_TIMEOUT", 30)
)
