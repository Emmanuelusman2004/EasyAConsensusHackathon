//server.js
const express = require('express');
const path = require('path');
const xlsx = require('xlsx');  // Make sure to require 'xlsx'
const fs = require('fs');      // Make sure to require 'fs'
const app = express();

app.use(express.json()); // Middleware to parse JSON bodies

// Serve static files from the specific directory (make sure this path is correct)
app.use(express.static('/Users/david/Desktop/KRED-Line'));

// Main route to serve the HTML file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'home_page.html'), { root: '' });
});

app.post('/submit-loan', (req, res) => {
    const { secretKey, collateralAsset, collateralAmount, loanAmount, loanDuration } = req.body;

    try {
        const wb = xlsx.utils.book_new();
        const ws_data = [
            ["Secret Key", "Collateral Asset", "Collateral Amount", "Loan Amount", "Loan Duration"],
            [secretKey, collateralAsset, collateralAmount, loanAmount, loanDuration]
        ];
        const ws = xlsx.utils.aoa_to_sheet(ws_data);
        xlsx.utils.book_append_sheet(wb, ws, "Loan Request");

        const dirPath = path.join(__dirname, 'loan_sheets');
        if (!fs.existsSync(dirPath)) {
            fs.mkdirSync(dirPath);
        }

        const filePath = path.join(dirPath, `loan_${Date.now()}.xlsx`);
        xlsx.writeFile(wb, filePath);

        res.send("Loan request submitted and saved!");
    } catch (error) {
        console.error("Failed to create or save file:", error);
        res.status(500).send("Error processing your request.");
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});