function connectToLobstr() {
    // Redirect to the Lobstr app or handle connection
    const lobstrUrl = 'lobstr://connect';
    window.location.href = lobstrUrl;
}

document.getElementById('loanForm').addEventListener('submit', function(e) {
    e.preventDefault();
    console.log("Submit request initiated.");
    const secretKey = document.getElementById('secretKey').value;
    const collateralAsset = document.getElementById('collateralAsset').value;
    const collateralAmount = document.getElementById('collateralAmount').value;
    const loanAmount = document.getElementById('loanAmount').value;
    const loanDuration = document.getElementById('loanDuration').value;

    // Handling XLSX operations or AJAX request here
});

function submitRequest() {
    console.log("Submit request initiated.");
    var secretKey = document.getElementById('secretKey').value;
    var collateralAsset = document.getElementById('collateralAsset').value;
    var collateralAmount = document.getElementById('collateralAmount').value;
    var loanAmount = document.getElementById('loanAmount').value;
    var loanDuration = document.getElementById('loanDuration').value;

    var wb = XLSX.utils.book_new();
    var ws_data = [
        ["Wallet Public Address", "Collateral Asset", "Collateral Amount", "Loan Amount", "Loan Duration"],
        [secretKey, collateralAsset, collateralAmount, loanAmount, loanDuration]
    ];
    var ws = XLSX.utils.aoa_to_sheet(ws_data);
    XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
    XLSX.writeFile(wb, "LoanRequest.xlsx");
}
