from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

print("Installing...")
install_solc("0.8.0")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)


with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode to deploy
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
privyet_key = os.getenv("PRIVATE_KEY")

# create the contract in py
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# get the latest transaction
nonce = w3.eth.get_transaction_count(my_address)
# build a transaction
transaction = SimpleStorage.constructor().build_transaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
# sign a transaction
signed_txn = w3.eth.account.sign_transaction(transaction, privyet_key)
# send a transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("Deploying contract...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")

# working with contract you need
# contract address
# contract abi
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Call -> dont change anything, return a value
# Transact -> Make a state change
print(
    simple_storage.functions.retrieve().call(
        {"from": w3.to_checksum_address("0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1")}
    )
)
print(
    simple_storage.functions.store(15).call(
        {"from": w3.to_checksum_address("0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1")}
    )
)
print(
    simple_storage.functions.retrieve().call(
        {"from": w3.to_checksum_address("0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1")}
    )
)
# nothing changed bc we didnt transact anything
# create the transaction
store_transaction = simple_storage.functions.store(15).build_transaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
# sign the transaction
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=privyet_key
)
# send the transaction
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
# wait for it to finish
print("Updating contract...")
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Updated!")
print(
    simple_storage.functions.retrieve().call(
        {"from": w3.to_checksum_address("0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1")}
    )
)
# now it changed because we made a state change with transact
