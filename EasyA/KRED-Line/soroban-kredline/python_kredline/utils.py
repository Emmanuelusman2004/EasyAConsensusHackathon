import requests
from stellar_sdk import Server, Keypair, Network, TransactionBuilder

server = Server("https://horizon-testnet.stellar.org")

def fund_account(public_key):
    # Function to fund account using Friendbot
    response = requests.get(f"https://friendbot.stellar.org?addr={public_key}")
    return response.json()

def check_balance(public_key):
    account = server.accounts().account_id(public_key).call()
    return account['balances']

def generate_keypair():
    return Keypair.random()

def load_account(public_key):
    return server.load_account(public_key)

def submit_transaction(transaction):
    return server.submit_transaction(transaction)

def create_trustline(transaction_builder, asset, public_key):
    return transaction_builder.append_change_trust_op(
        asset_code=asset.code,
        asset_issuer=asset.issuer,
    )

def create_payment(transaction_builder, destination, amount, asset, public_key):
    return transaction_builder.append_payment_op(
        destination=destination,
        asset=asset,
        amount=amount,
    )
