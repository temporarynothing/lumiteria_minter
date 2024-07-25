import os
from web3 import Web3
from simple_cache import SimpleCache


def generate_public_addresses():
    # Initialize SimpleCache for storing public-private key mappings
    cache = SimpleCache('public_private_keys')

    # Load private keys from the file
    private_keys_file = os.path.join(os.path.dirname(__file__), '../data/private_keys.txt')
    with open(private_keys_file, 'r') as f:
        private_keys = [line.strip() for line in f]

    # Initialize Web3
    web3 = Web3(Web3.HTTPProvider())

    # Generate public addresses and store them in the cache
    for private_key in private_keys:
        account = web3.eth.account.from_key(private_key)
        public_address = account.address
        cache.set(public_address, private_key)
        print(f'Generated public address {public_address} for private key {private_key}')

    print('Public-private key mapping has been saved.')


if __name__ == "__main__":
    generate_public_addresses()
