use stellar_sdk::{KeyPair, Network, TransactionBuilder, Operation, Asset, IntoTransactionBuilder};

pub fn release_collateral(
    intermediary_secret: &str,
    borrower_pubkey: &str,
    collateral_amount: &str
) -> Result<(), Box<dyn std::error::Error>> {
    let intermediary = KeyPair::from_secret(intermediary_secret)?;
    let account = stellar_sdk::endpoints::account::for_account(intermediary.public_key().to_string()).execute()?;
    let collateral_asset = Asset::native();

    let tx = TransactionBuilder::new(account)
        .add_operation(Operation::payment()
            .with_destination(borrower_pubkey)
            .with_asset(&collateral_asset)
            .with_amount(collateral_amount)
            .build()?)
        .with_memo(stellar_sdk::Memo::text("Collateral Released"))
        .build()?;

    tx.sign(&intermediary, &Network::new_test());
    stellar_sdk::endpoints::submit_transaction(&tx).execute()?;

    Ok(())
}
