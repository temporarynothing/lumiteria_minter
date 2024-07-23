import random
import time
from web3 import Web3
from simple_cache import SimpleCache


def mint_nft():
    config = SimpleCache('config')
    print(config.data)
    rpc_url = "https://api.roninchain.com/rpc"
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    contract_address = "0x19f70ecd63f40f11716c3ce2b50a6d07491c12fe"
    contract_address = Web3.to_checksum_address(contract_address)
    contract_abi = [{"inputs":[{"internalType":"contract IConfig","name":"_config","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"previousAdmin","type":"address"},{"indexed":False,"internalType":"address","name":"newAdmin","type":"address"}],"name":"AdminChanged","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"beacon","type":"address"}],"name":"BeaconUpgraded","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint8","name":"version","type":"uint8"}],"name":"Initialized","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"user","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"inputs":[],"name":"config","outputs":[{"internalType":"contract IConfig","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"dailyUserMintLimit","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"inviteCode","type":"string"}],"name":"inviteCodeMintCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"inviteCode","type":"string"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"proxiableUUID","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"limit","type":"uint256"}],"name":"setDailyUserMintLimit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"}],"name":"upgradeTo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"upgradeToAndCall","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"userDailyMintLimit","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]  # Add the ABI of the contract here

    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    min_sleep_time_sec = config.get('min_sleep_time_sec')
    max_sleep_time_sec = config.get('max_sleep_time_sec')
    min_mint_percent = config.get('min_mint_addresses_percent')
    max_mint_percent = config.get('max_mint_addresses_percent')

    with open('../data/private_keys.txt', 'r') as f:
        private_keys = [line.strip() for line in f]

    total_addresses = len(private_keys)
    num_to_mint = random.randint(
        int(total_addresses * min_mint_percent / 100),
        int(total_addresses * max_mint_percent / 100)
    )
    print(f'minting on {num_to_mint} wallets')

    if config.get("do_shuffle_accounts"):
        random.shuffle(private_keys)

    for i in range(num_to_mint):
        private_key = private_keys[i]
        account = web3.eth.account.from_key(private_key)
        have_mints = contract.functions.userDailyMintLimit(account.address).call()
        if have_mints == 0:
            print(f'already minted on {account.address}')
            continue

        nonce = web3.eth.get_transaction_count(account.address)
        tx = contract.functions.mint('cbt').build_transaction({
            'chainId': 2020,
            'gas': 200000,
            'gasPrice': web3.to_wei(20, 'gwei'),
            'nonce': nonce
        })
        signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
        try:
            tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            print(f"Mint transaction sent: {web3.to_hex(tx_hash)}")
        except Exception as e:
            try:
                message = e.args[0]["message"]
                if "insufficient funds" in message:
                    print(f'no gas for {account.address}')
            except Exception as e:
                print('unknown exception')
                print(e)

        time.sleep(random.randint(min_sleep_time_sec, max_sleep_time_sec))


if __name__ == "__main__":
    mint_nft()
