from monero.wallet import Wallet


COMMAND = "refresh"


def refresh(wallet: Wallet):
    print("Starting refresh...")
    wallet.refresh()
