from flask import Flask, request, jsonify, send_from_directory
from stellar_sdk import Asset, Keypair, Server, TransactionBuilder, Network
from utils import fund_account, check_balance, generate_keypair, load_account, submit_transaction, create_trustline, create_payment

app = Flask(__name__)
server = Server("https://horizon-testnet.stellar.org")

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/fund_account', methods=['POST'])
def fund_account_endpoint():
    public_key = request.json.get('public_key')
    if not public_key:
        return jsonify({"error": "public_key is required"}), 400
    
    fund_account(public_key)
    return jsonify({"message": f"Account {public_key} funded successfully"}), 200

@app.route('/create_trustline', methods=['POST'])
def create_trustline_endpoint():
    secret = request.json.get('secret')
    asset_code = request.json.get('asset_code')
    asset_issuer = request.json.get('asset_issuer')
    if not secret or not asset_code or not asset_issuer:
        return jsonify({"error": "secret, asset_code, and asset_issuer are required"}), 400

    keypair = Keypair.from_secret(secret)
    asset = Asset(asset_code, asset_issuer)
    
    try:
        account = server.load_account(keypair.public_key)
        transaction = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100
        ).append_change_trust_op(
            asset_code=asset.code,
            asset_issuer=asset.issuer,
        ).set_timeout(30).build()

        transaction.sign(keypair)
        response = server.submit_transaction(transaction)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/transfer_collateral', methods=['POST'])
def transfer_collateral_endpoint():
    borrower_secret = request.json.get('borrower_secret')
    intermediary_public_key = request.json.get('intermediary_public_key')
    asset_code = request.json.get('asset_code')
    asset_issuer = request.json.get('asset_issuer')
    amount = request.json.get('amount')
    if not borrower_secret or not intermediary_public_key or not asset_code or not asset_issuer or not amount:
        return jsonify({"error": "All fields are required"}), 400

    borrower_keypair = Keypair.from_secret(borrower_secret)
    asset = Asset(asset_code, asset_issuer)
    
    try:
        borrower_account = server.load_account(borrower_keypair.public_key)
        transaction = TransactionBuilder(
            source_account=borrower_account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100
        ).append_payment_op(
            destination=intermediary_public_key,
            asset=asset,
            amount=amount
        ).set_timeout(30).build()

        transaction.sign(borrower_keypair)
        response = server.submit_transaction(transaction)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
