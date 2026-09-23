const API_URL = "";


// ===============================
// ADD TRANSACTION
// ===============================

async function addTransaction() {

    const description =
        document.getElementById("description").value.trim();

    const amount =
        document.getElementById("amount").value;

    const type =
        document.getElementById("type").value;


    if (description === "" || amount === "") {

        alert("Please enter description and amount.");

        return;
    }


    try {

        const response = await fetch(
            API_URL + "/transactions",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    description: description,
                    amount: Number(amount),
                    type: type
                })
            }
        );


        if (!response.ok) {

            throw new Error(
                "Server error: " + response.status
            );
        }


        const data = await response.json();


        alert("Transaction added successfully!");


        document.getElementById(
            "description"
        ).value = "";


        document.getElementById(
            "amount"
        ).value = "";


        await loadTransactions();

        await loadSummary();

    }

    catch (error) {

        console.error(error);

        alert(
            "Could not add transaction.\n" +
            "Make sure Flask is running."
        );
    }
}



// ===============================
// LOAD TRANSACTIONS
// ===============================

async function loadTransactions() {

    try {

        const response = await fetch(
            API_URL + "/transactions"
        );


        const data = await response.json();


        const list =
            document.getElementById(
                "transactionList"
            );


        list.innerHTML = "";


        data.forEach(transaction => {

            const item =
                document.createElement("li");


            item.innerHTML =
                "<strong>" +
                transaction.description +
                "</strong>" +
                " - ₹" +
                transaction.amount +
                " (" +
                transaction.type +
                ")";


            list.appendChild(item);

        });

    }

    catch (error) {

        console.error(
            "Transaction loading error:",
            error
        );
    }
}



// ===============================
// LOAD SUMMARY
// ===============================

async function loadSummary() {

    try {

        const response = await fetch(
            API_URL + "/summary"
        );


        const data = await response.json();


        document.getElementById(
            "income"
        ).innerText =
            "₹" + data.income;


        document.getElementById(
            "expense"
        ).innerText =
            "₹" + data.expense;


        document.getElementById(
            "balance"
        ).innerText =
            "₹" + data.balance;

    }

    catch (error) {

        console.error(
            "Summary loading error:",
            error
        );
    }
}



// ===============================
// LOAD DATA WHEN PAGE OPENS
// ===============================

loadTransactions();

loadSummary();