# stellar.py

from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset
from config import NETWORK_PASSPHRASE, HORIZON_URL

server = Server(horizon_url="https://horizon-testnet.stellar.org")

def generate_keypair():
    return Keypair.random()

def load_account(public_key):
    return server.load_account(public_key)

def check_balance(public_key):
    account = load_account(public_key)
    balances = account.raw_data["balances"]
    for balance in balances:
        asset_type = balance["asset_type"]
        asset_code = balance.get("asset_code", "XLM")
        balance_amount = balance["balance"]
        print(f"Asset: {asset_code}, Balance: {balance_amount}")
    return balances

def create_trustline(transaction_builder, asset, source_public_key):
    return transaction_builder.append_change_trust_op(
        asset=asset,
        source=source_public_key
    )

def create_payment(transaction_builder, destination, amount, asset, source):
    return transaction_builder.append_payment_op(
        destination=destination,
        amount=amount,
        asset=asset,
        source=source
    )

def submit_transaction(transaction, keypair):
    transaction.sign(keypair)
    response = server.submit_transaction(transaction)
    return response
