mod loan;
mod collateral;

use loan::{create_loan_request, fund_loan, repay_loan};
use collateral::release_collateral;

fn main() {
    // Example usage
    let borrower_secret = "SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
    let lender_secret = "SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
    let intermediary_secret = "SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
    let borrower_pubkey = "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
    let lender_pubkey = "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
    let intermediary_pubkey = "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
    let collateral_amount = "100";
    let loan_amount = "50";
    let repayment_amount = "55"; // loan amount + interest
    let loan_duration = 86400; // 1 day in seconds

    // Create a loan request
    create_loan_request(borrower_secret, "native", collateral_amount, loan_amount, loan_duration, intermediary_pubkey).unwrap();

    // Fund the loan
    fund_loan(lender_secret, borrower_pubkey, loan_amount).unwrap();

    // Repay the loan
    repay_loan(borrower_secret, lender_pubkey, repayment_amount).unwrap();

    // Release the collateral
    release_collateral(intermediary_secret, borrower_pubkey, collateral_amount).unwrap();
}
