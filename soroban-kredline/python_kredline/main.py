import time
from stellar_sdk import Asset, Keypair, Network, Server, TransactionBuilder
from stellar_sdk.exceptions import NotFoundError, BadResponseError, BadRequestError
from stellar import generate_keypair, load_account, submit_transaction, check_balance, create_trustline, create_payment
from config import NETWORK_PASSPHRASE
from utils import fund_account

# Function to send payment
def send_payment(source_keypair, destination_id, amount, memo_text):
    server = Server("https://horizon-testnet.stellar.org")

    # Check if the destination account exists
    try:
        server.load_account(destination_id)
    except NotFoundError:
        raise Exception("The destination account does not exist!")

    # Load source account
    source_account = server.load_account(source_keypair.public_key)

    # Fetch base fee
    base_fee = server.fetch_base_fee()

    # Build the transaction
    transaction = (
        TransactionBuilder(
            source_account=source_account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=base_fee,
        )
        .append_payment_op(destination=destination_id, asset=Asset.native(), amount=amount)
        .add_text_memo(memo_text)
        .set_timeout(30)
        .build()
    )

    # Sign the transaction
    transaction.sign(source_keypair)

    # Submit the transaction
    try:
        response = server.submit_transaction(transaction)
        print(f"Response: {response}")
    except (BadRequestError, BadResponseError) as err:
        print(f"Something went wrong!\n{err}")

# Generate keypairs
lender_keypair = generate_keypair()
borrower_keypair = generate_keypair()
intermediary_keypair = generate_keypair()

# Fund accounts
fund_account(lender_keypair.public_key)
fund_account(borrower_keypair.public_key)
fund_account(intermediary_keypair.public_key)

# Check balances after funding
print("Lender Balance:")
check_balance(lender_keypair.public_key)

print("Borrower Balance:")
borrower_balance_info = check_balance(borrower_keypair.public_key)

print("Intermediary Balance:")
check_balance(intermediary_keypair.public_key)

# Asset for collateral
collateral_asset = Asset("COLLATERAL", intermediary_keypair.public_key)

# Load borrower account
borrower_account = load_account(borrower_keypair.public_key)

# Calculate the minimum balance required for the borrower
min_balance = 2 + 1  # 2 base entries + 1 trustline
base_reserve = 0.5  # in XLM
min_balance_required = min_balance * base_reserve

# Print the borrower's current balance and the required minimum balance
borrower_balance = float(borrower_balance_info[0]['balance'])
print(f"Borrower's current balance: {borrower_balance} XLM")
print(f"Minimum balance required: {min_balance_required} XLM")

# Ensure borrower has enough balance to proceed with the transaction
required_for_operations = 0.00001 * 200  # Base fee is 100 stroops per operation, two operations
total_required = min_balance_required + required_for_operations + 1  # +1 for a small collateral
if borrower_balance < total_required:
    raise Exception(f"Borrower does not have enough balance to create a trustline and make the payment. Required: {total_required} XLM")

print(f"Total required: {total_required} XLM")
print("Proceeding with transaction creation...")

# Ensure borrower has a trustline for the collateral asset
transaction_builder = TransactionBuilder(
    source_account=borrower_account,
    network_passphrase=NETWORK_PASSPHRASE,
    base_fee=100
)
transaction_builder = create_trustline(transaction_builder, collateral_asset, borrower_keypair.public_key)
trustline_transaction = transaction_builder.set_timeout(30).build()

# Submit trustline transaction
try:
    response = submit_transaction(trustline_transaction, borrower_keypair)
    print(f"Trustline transaction response: {response}")
except (BadRequestError, BadResponseError) as err:
    print(f"Trustline transaction failed: {err}")
    raise

# Check borrower balance after trustline creation
borrower_balance_info = check_balance(borrower_keypair.public_key)
borrower_balance = float(borrower_balance_info[0]['balance'])
print(f"Borrower's balance after trustline creation: {borrower_balance} XLM")

# Ensure sufficient balance for collateral transfer
if borrower_balance < required_for_operations + 1:  # +1 for the collateral
    fund_account(borrower_keypair.public_key)

# Recheck borrower balance after funding
borrower_balance_info = check_balance(borrower_keypair.public_key)
borrower_balance = float(borrower_balance_info[0]['balance'])
print(f"Borrower's balance after funding: {borrower_balance} XLM")

# Build transaction to transfer collateral to intermediary
transaction_builder = TransactionBuilder(
    source_account=borrower_account,
    network_passphrase=NETWORK_PASSPHRASE,
    base_fee=100
)
transaction_builder = create_payment(transaction_builder, intermediary_keypair.public_key, "1", collateral_asset, borrower_keypair.public_key)
collateral_transaction = transaction_builder.set_timeout(30).build()

# Submit collateral transfer transaction
try:
    response = submit_transaction(collateral_transaction, borrower_keypair)
    print(f"Collateral transfer transaction response: {response}")
except (BadRequestError, BadResponseError) as err:
    print(f"Collateral transfer transaction failed: {err}")
    raise

# Check balances after collateral transfer
print("Lender Balance After Transaction:")
check_balance(lender_keypair.public_key)

print("Borrower Balance After Transaction:")
check_balance(borrower_keypair.public_key)

print("Intermediary Balance After Transaction:")
check_balance(intermediary_keypair.public_key)

# Simulate holding the collateral for 30 days
print("Simulating 30-day loan period...")
time.sleep(3)  # Use a shorter sleep for demonstration; replace with 30 days (30 * 24 * 60 * 60) in a real scenario

# Return the collateral to the borrower after the loan period
intermediary_account = load_account(intermediary_keypair.public_key)
transaction_builder = TransactionBuilder(
    source_account=intermediary_account,
    network_passphrase=NETWORK_PASSPHRASE,
    base_fee=100
)
transaction_builder = create_payment(transaction_builder, borrower_keypair.public_key, "1", collateral_asset, intermediary_keypair.public_key)
return_transaction = transaction_builder.set_timeout(30).build()

# Submit return transaction
try:
    response = submit_transaction(return_transaction, intermediary_keypair)
    print(f"Return transaction response: {response}")
except (BadRequestError, BadResponseError) as err:
    print(f"Return transaction failed: {err}")

# Check balances after returning collateral
print("Lender Balance After Releasing Collateral:")
check_balance(lender_keypair.public_key)

print("Borrower Balance After Releasing Collateral:")
check_balance(borrower_keypair.public_key)

print("Intermediary Balance After Releasing Collateral:")
check_balance(intermediary_keypair.public_key)
