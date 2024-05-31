use stellar_sdk::{KeyPair, Network, TransactionBuilder, Operation, Asset, IntoTransactionBuilder};
use soroban_sdk::xdr::Memo;


pub fn create_loan_request(
    borrower_secret: &str,
    collateral_asset: &str,
    collateral_amount: &str,
    loan_amount: &str,
    loan_duration: u64,
    intermediary_pubkey: &str
) -> Result<(), Box<dyn std::error::Error>> {
    let borrower = KeyPair::from_secret(borrower_secret)?;
    let account = stellar_sdk::endpoints::account::for_account(borrower.public_key().to_string()).execute()?;
    let collateral = Asset::native();

    let tx = TransactionBuilder::new(account)
        .add_operation(Operation::payment()
            .with_destination(intermediary_pubkey)
            .with_asset(&collateral)
            .with_amount(collateral_amount)
            .build()?)
        .with_memo(stellar_sdk::Memo::text("Loan Request"))
        .build()?;

    tx.sign(&borrower, &Network::new_test());
    stellar_sdk::endpoints::submit_transaction(&tx).execute()?;

    Ok(())
}

pub fn fund_loan(
    lender_secret: &str,
    borrower_pubkey: &str,
    loan_amount: &str
) -> Result<(), Box<dyn std::error::Error>> {
    let lender = KeyPair::from_secret(lender_secret)?;
    let account = stellar_sdk::endpoints::account::for_account(lender.public_key().to_string()).execute()?;
    let loan_asset = Asset::native();

    let tx = TransactionBuilder::new(account)
        .add_operation(Operation::payment()
            .with_destination(borrower_pubkey)
            .with_asset(&loan_asset)
            .with_amount(loan_amount)
            .build()?)
        .with_memo(stellar_sdk::Memo::text("Loan Funded"))
        .build()?;

    tx.sign(&lender, &Network::new_test());
    stellar_sdk::endpoints::submit_transaction(&tx).execute()?;

    Ok(())
}

pub fn repay_loan(
    borrower_secret: &str,
    lender_pubkey: &str,
    repayment_amount: &str
) -> Result<(), Box<dyn std::error::Error>> {
    let borrower = KeyPair::from_secret(borrower_secret)?;
    let account = stellar_sdk::endpoints::account::for_account(borrower.public_key().to_string()).execute()?;
    let repayment_asset = Asset::native();

    let tx = TransactionBuilder::new(account)
        .add_operation(Operation::payment()
            .with_destination(lender_pubkey)
            .with_asset(&repayment_asset)
            .with_amount(repayment_amount)
            .build()?)
        .with_memo(stellar_sdk::Memo::text("Loan Repaid"))
        .build()?;

    tx.sign(&borrower, &Network::new_test());
    stellar_sdk::endpoints::submit_transaction(&tx).execute()?;

    Ok(())
}
