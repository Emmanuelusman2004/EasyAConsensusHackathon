// tests/integration_tests.rs

use stellar_pawnshop::loan::{create_loan_request, fund_loan, repay_loan};
use stellar_pawnshop::collateral::release_collateral;

#[test]
fn test_full_workflow() {
    let borrower_secret = "SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
    let lender_secret = "SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
    let intermediary_secret = "SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
    let borrower_pubkey = "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
    let lender_pubkey = "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
    let intermediary_pubkey = "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
    let collateral_amount = "100";
    let loan_amount = "50";
    let repayment_amount = "55";
    let loan_duration = 86400;

    // Step 1: Create a loan request
    let result = create_loan_request(borrower_secret, "native", collateral_amount, loan_amount, loan_duration, intermediary_pubkey);
    assert!(result.is_ok());

    // Step 2: Fund the loan
    let result = fund_loan(lender_secret, borrower_pubkey, loan_amount);
    assert!(result.is_ok());

    // Step 3: Repay the loan
    let result = repay_loan(borrower_secret, lender_pubkey, repayment_amount);
    assert!(result.is_ok());

    // Step 4: Release the collateral
    let result = release_collateral(intermediary_secret, borrower_pubkey, collateral_amount);
    assert!(result.is_ok());
}
