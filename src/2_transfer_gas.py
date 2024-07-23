import json
from web3 import Web3
from simple_cache import SimpleCache
import random

from utils import sleep


def transfer_gas():
    config = SimpleCache('config')
    print(config.data)
    rpc_url = "https://api.roninchain.com/rpc"
    web3 = Web3(Web3.HTTPProvider(rpc_url))

    main_gas_account_key = config.get('main_gas_account_key')
    if not main_gas_account_key:
        main_gas_account_key = input("Enter the private key for the main gas-source address: ")
    if not main_gas_account_key.startswith('0x'):
        main_gas_account_key = '0x' + main_gas_account_key

    main_gas_address = web3.eth.account.from_key(main_gas_account_key.strip()).address

    with open('../data/private_keys.txt', 'r') as f:
        addresses = [web3.eth.account.from_key(line.strip()).address for line in f]

    if config.get("do_shuffle_accounts"):
        random.shuffle(addresses)

    nonce = web3.eth.get_transaction_count(main_gas_address)
    for address in addresses:
        balance = web3.eth.get_balance(address)
        balance_ether = web3.from_wei(balance, 'ether')
        print(f"Address: {address}, Balance: {balance_ether} Ether")
        if balance > web3.to_wei(0.005, 'ether'):
            print('skip')
            continue

        # confirm = input(f"Do you want to transfer gas to {address}? (YES/NO): ").strip().lower()
        confirm = "yes"
        if confirm == 'yes':
            tx = {
                'nonce': nonce,
                'to': address,
                'value': web3.to_wei(random.uniform(0.005, 0.01), 'ether'),
                'gas': 21000,
                'gasPrice': web3.to_wei(random.randint(20, 22), 'gwei')
            }
            signed_tx = web3.eth.account.sign_transaction(tx, private_key=main_gas_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            print(f"Transaction sent: {web3.to_hex(tx_hash)}")
            nonce += 1
            sleep_time = random.uniform(config.get("min_sleep_time_sec"), config.get("max_sleep_time_sec"))
            sleep(sleep_time)


if __name__ == "__main__":
    transfer_gas()
