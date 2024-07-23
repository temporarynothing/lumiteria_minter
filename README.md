
# Lumiterra NFT mint

This project provides a series of modules for minting NFTs on the Ronin blockchain, including generating private keys, transferring gas, and minting NFTs.

## Prerequisites

- Python 3.9 or higher
  Install Python via conda or download from [Python.org](https://www.python.org/).

## Installation

Follow these steps to install and set up the NFT minting project:

1. **Clone the Repository**
   ```sh
   git clone https://github.com/YourUsername/nft_minting_project
   cd nft_minting_project
   ```

2. **Create and Activate a Virtual Environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

## Setup

1. **Edit the Configuration File**
   - Open the `src/config.json` file and edit the necessary parameters.
   - Example `config.json`:
     ```json
     {
         "main_gas_account_key": "",
         "min_sleep_time_sec": 30,
         "max_sleep_time_sec": 200,
         "min_mint_addresses_percent": 85,
         "max_mint_addresses_percent": 95,
         "do_shuffle_accounts": true
     }
     ```
   - **Note:**
     - `main_gas_account_key`: The private key of the main gas account (you can also enter it on request in 2_transfer_gas.py)
     - `min_sleep_time_sec` and `max_sleep_time_sec`: The minimum and maximum sleep time in seconds between minting actions.
     - `min_mint_addresses_percent` and `max_mint_addresses_percent`: The minimum and maximum percentage of addresses that will mint NFTs that day.
     - `do_shuffle_accounts`: Whether to shuffle the order of accounts before minting/transferring gas.

2. **Add Private Keys**
   - Add your private keys to `src/private_keys.txt`, one per line or generate them using 1_generate_keys.py

## Running the Scripts

#### If you have PyCharm, just run the files from it. It would be the easiest way. If not:

0. **Go to src directory**
    ```sh
    cd src
    ```

1. **Generate Private Keys**
   ```sh
   python 1_generate_keys.py
   ```
   - This script will generate new private keys and save them to `src/private_keys.txt`.

2. **Transfer Gas**
   ```sh
   python 2_transfer_gas.py
   ```
   - This script transfers gas from the main gas account to other accounts listed in `src/private_keys.txt`.

3. **Mint NFTs**
   ```sh
   python 3_mint_nft.py
   ```
   - This script mints NFTs using the accounts listed in `src/private_keys.txt`.

## Troubleshooting

- Ensure Python version 3.9 or higher is installed.
- Verify all dependencies are correctly installed using `pip install -r requirements.txt`.
- Double-check your private keys and ensure they are entered correctly in `src/private_keys.txt`.
- Verify the `src/config.json` file is correctly configured.

## Additional Information

- **Chain ID (network ID):** 2020
- **RPC endpoint:** https://api.roninchain.com/rpc
- **Explorer:** app.roninchain.com
- **Min Gas price:** 20 gwei
- **Contract address:** 0xac1e564a6ef85c0aff9b3681a6ad3c37dee71b73
