import os
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv

import deploy

# Load environment variables
load_dotenv()

# Set up web3 connection
provider_url = os.getenv("CELO_PROVIDER_URL")
w3 = Web3(HTTPProvider(provider_url))
assert w3.is_connected(), "Not connected to a Celo node"

# Add PoA middleware to web3.py instance
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Get contract ABI and address
abi = deploy.abi
contract_address = deploy.contract_address
contract = w3.eth.contract(address=contract_address, abi=abi)

# Initialize account
account_address = os.getenv("CELO_DEPLOYER_ADDRESS")
private_key = os.getenv("CELO_DEPLOYER_PRIVATE_KEY")


# Send transaction method
def send_transaction(function, *args, value=0):
    function_with_args = function(*args)
    nonce = w3.eth.get_transaction_count(account_address, 'pending')
    gas_price = w3.eth.gas_price
    gas_estimate = function_with_args.estimate_gas(
        {'from': account_address, 'value': value})

    transaction = function_with_args.build_transaction({
        'from': account_address,
        'value': value,
        'gas': gas_estimate,
        'gasPrice': gas_price,
        'nonce': nonce
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    return w3.eth.send_raw_transaction(signed_txn.rawTransaction)


# Add a beneficiary
beneficiary = '0x8BdDeC1b7841bF9eb680bE911bd22051f6a00815'  # 'BENEFICIARY_ADDRESS'


add_beneficiary_function = contract.functions.addBeneficiary
add_beneficiary_tx_hash = send_transaction(
    add_beneficiary_function, beneficiary)
print(
    f"Beneficiary added with transaction hash: {add_beneficiary_tx_hash.hex()}")


# Replace with the desired amount
amount = w3.to_wei(0.00001, 'ether')  # Convert to the smallest unit of CELO

# Receive an inheritance
receive_inheritance_function = contract.functions.receiveInheritance
receive_inheritance_tx_hash = send_transaction(
    receive_inheritance_function, value=amount)  # Replace 1 with the amount of CELO you want to send
print(
    f"Inheritance received with transaction hash: {receive_inheritance_tx_hash.hex()}")


# Distribute an inheritance
distribute_inheritance_function = contract.functions.distributeInheritance
distribute_inheritance_tx_hash = send_transaction(
    distribute_inheritance_function, beneficiary, amount)
print(
    f"Inheritance distributed with transaction hash: {distribute_inheritance_tx_hash.hex()}")


# Remove a beneficiary
remove_beneficiary_function = contract.functions.removeBeneficiary
remove_beneficiary_tx_hash = send_transaction(
    remove_beneficiary_function, beneficiary)
print(
    f"Beneficiary removed with transaction hash: {remove_beneficiary_tx_hash.hex()}")
