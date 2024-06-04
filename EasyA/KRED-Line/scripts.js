// scripts.js
function connectToLobstr() {
    const lobstrUrl = 'lobstr://connect';
    window.location.href = lobstrUrl;
}

document.getElementById('loanForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the form from submitting via default HTML form submission
    submitRequest(); // Call your submitRequest function when form is submitted
});

function submitRequest() {
    const secretKey = document.getElementById('secretKey').value;
    const collateralAsset = document.getElementById('collateralAsset').value;
    const collateralAmount = document.getElementById('collateralAmount').value;
    const loanAmount = document.getElementById('loanAmount').value;
    const loanDuration = document.getElementById('loanDuration').value;

    // Data to be sent in the POST request
    const data = {
        secretKey,
        collateralAsset,
        collateralAmount,
        loanAmount,
        loanDuration
    };

    fetch('/submit-loan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.text())
    .then(result => {
        console.log(result);
        alert("Loan request submitted successfully!");
    })
    .catch(error => {
        console.error('Error submitting loan request:', error);
        alert("Failed to submit loan request.");
    });
}
