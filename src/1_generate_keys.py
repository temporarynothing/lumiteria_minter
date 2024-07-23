import os
from eth_account import Account

private_keys_path = '../data/private_keys.txt'

def generate_keys():
    if os.path.exists(private_keys_path) and os.path.getsize(private_keys_path) > 0:
        input("private_keys.txt is not empty. Press Enter to confirm overwriting...")

    num_keys = int(input("Enter the number of private keys to generate: "))
    with open(private_keys_path, 'w') as f:
        for _ in range(num_keys):
            account = Account.create()
            f.write(f"{account.key.hex()}\n")

if __name__ == "__main__":
    generate_keys()
