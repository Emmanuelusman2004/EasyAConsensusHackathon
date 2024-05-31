#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_loan_request() {
        let result = create_loan_request(
            "SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "native",
            "100",
            "50",
            86400,
            "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        );
        assert!(result.is_ok());
    }

    #[test]
    fn test_fund_loan() {
        let result = fund_loan(
            "SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "50",
        );
        assert!(result.is_ok());
    }

    #[test]
    fn test_repay_loan() {
        let result = repay_loan(
            "SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "55",
        );
        assert!(result.is_ok());
    }
}
