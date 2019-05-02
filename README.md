## cli-like commands for wallet rpc

These scripts intend to interface with the wallet-rpc, and provide a wallet-cli-like experience.

Eventually they should be wrapped to avoid invoking them separately, and instead provide a more wallet-cli-like experience

# Requirements:
Install requirements with
```shell
pip install -r requirements.txt
```

## Configuration
These scripts rely on the following envvars for configuration

* `RPC_WALLET_HOST`
* `RPC_WALLET_PORT`
* `RPC_WALLET_USER`
* `RPC_WALLET_PASSWORD`
* `RPC_WALLET_STAGENET`: Defaults to 1
* `RPC_WALLET_TESTNET`: Defaults to 0
* `RPC_WALLET_REQUESTS_TIMEOUT`: Expressed in seconds. Defaults to 20

## Examples

### `balance`

```shell
$ python balance.py
Balance: 6722.915229932574, unlocked balance: 6722.915229932574
```

### `address`

```shell
$ python address.py
0 548h3e2DrGyFjyQrj4DSRM8nJQRFZqAEcVqNhjqKg8RoW8vU551uaap4CLctr6oFZzPTiPiBNEB4a9NPbAVGGQWyPyZWnXp Primary address
```

### `unspent_outputs`

```shell
$ python unspent_outputs.py
Total count: 2225
Min amount found: 0.000000000050
Max amount found: 523.430541060000
```

### `transfer`

```shell
$ python transfer \
548h3e2DrGyFjyQrj4DSRM8nJQRFZqAEcVqNhjqKg8RoW8vU551uaap4CLctr6oFZzPTiPiBNEB4a9NPbAVGGQWyPyZWnXp 2 \
548h3e2DrGyFjyQrj4DSRM8nJQRFZqAEcVqNhjqKg8RoW8vU551uaap4CLctr6oFZzPTiPiBNEB4a9NPbAVGGQWyPyZWnXp 5

Sending 7 xmr.
Is this ok? (y/yes/n/no)

y

Transaction successfully submitted. Transactions:
2e8c16e3a3b603501992664acf35222c32e6a9dddca4affe822cfde60a8a159a
```

## TODO:

* Extend already implemented commands to take all the arguments that their wallet-cli equivalents take.
* Extend already implemented commands to return the same results that their wallet-cli equivalents return.
* Implement missing wallet-cli commands.
* Wrap with a wallet-cli-like session, to avoid having to invoke these scripts separately