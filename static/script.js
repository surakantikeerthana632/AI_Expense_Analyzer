const expenseForm =
    document.getElementById("expenseForm");

const amountInput =
    document.getElementById("amount");

const dateInput =
    document.getElementById("date");

const categoryInput =
    document.getElementById("category");


const message =
    document.getElementById("message");


/* Set today's date */

const today =
    new Date().toISOString().split("T")[0];

dateInput.value = today;


/* Add expense */

expenseForm.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();


        const expense = {

            amount:
                parseFloat(amountInput.value),

            date:
                dateInput.value,

            category:
                categoryInput.value
        };


        try {

            const response =
                await fetch("/expenses", {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(expense)
                });


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Failed to add expense"
                );

            }


            message.textContent =
                "Expense added successfully!";


            message.style.color =
                "green";


            expenseForm.reset();

            dateInput.value = today;


            await loadDashboard();

            await loadExpenses();

            await loadAIInsights();


        } catch (error) {

            message.textContent =
                error.message;

            message.style.color =
                "red";
        }

    }
);


/* Load dashboard */

async function loadDashboard() {

    try {

        const response =
            await fetch("/dashboard");

        const result =
            await response.json();

        const data =
            result.data;


        document.getElementById(
            "totalSpending"
        ).textContent =
            "₹" +
            Number(
                data.total_spending
            ).toFixed(2);


        const categories =
            data.category_wise;


        if (categories.length > 0) {

            document.getElementById(
                "topCategory"
            ).textContent =
                categories[0].category;

        } else {

            document.getElementById(
                "topCategory"
            ).textContent =
                "-";
        }


        createCategoryChart(
            categories
        );


        createMonthlyChart(
            data.monthly
        );


    } catch (error) {

        console.error(
            "Dashboard error:",
            error
        );

    }

}


/* Load expenses */

async function loadExpenses() {

    try {

        const response =
            await fetch("/expenses");

        const result =
            await response.json();

        const expenses =
            result.expenses;


        document.getElementById(
            "transactionCount"
        ).textContent =
            expenses.length;


        const table =
            document.getElementById(
                "expenseTable"
            );


        table.innerHTML = "";


        expenses.forEach(
            function(expense) {

                const row =
                    document.createElement("tr");


                row.innerHTML = `

                    <td>
                        ${escapeHTML(expense.date)}
                    </td>

                    <td>
                        ${escapeHTML(expense.category)}
                    </td>

                    <td>
                        ₹${Number(
                            expense.amount
                        ).toFixed(2)}
                    </td>

                    <td>

                        <button
                            class="delete-btn"
                            onclick="deleteExpense(
                                ${expense.id}
                            )"
                        >
                            Delete
                        </button>

                    </td>
                `;


                table.appendChild(row);

            }
        );


    } catch (error) {

        console.error(
            "Expense loading error:",
            error
        );

    }

}


/* Delete expense */

async function deleteExpense(id) {

    if (!confirm(
        "Are you sure you want to delete this expense?"
    )) {

        return;

    }


    try {

        const response =
            await fetch(
                `/expenses/${id}`,
                {
                    method: "DELETE"
                }
            );


        if (!response.ok) {

            throw new Error(
                "Could not delete expense"
            );

        }


        await loadDashboard();

        await loadExpenses();

        await loadAIInsights();


    } catch (error) {

        alert(error.message);

    }

}


/* Category chart */

function createCategoryChart(
    categories
) {

    const container =
        document.getElementById(
            "categoryChart"
        );


    container.innerHTML = "";


    if (categories.length === 0) {

        container.innerHTML =
            "<p>No category data available.</p>";

        return;
    }


    const maximum =
        Math.max(
            ...categories.map(
                item => item.total
            )
        );


    categories.forEach(
        function(item) {

            const percentage =
                maximum === 0
                    ? 0
                    : (
                        item.total /
                        maximum
                    ) * 100;


            const div =
                document.createElement(
                    "div"
                );


            div.className = "bar";


            div.innerHTML = `

                <div class="bar-label">

                    <span>
                        ${escapeHTML(
                            item.category
                        )}
                    </span>

                    <span>
                        ₹${Number(
                            item.total
                        ).toFixed(2)}
                    </span>

                </div>


                <div class="bar-background">

                    <div
                        class="bar-fill"
                        style="width:
                            ${percentage}%"
                    >
                    </div>

                </div>

            `;


            container.appendChild(div);

        }
    );

}


/* Monthly chart */

function createMonthlyChart(
    months
) {

    const container =
        document.getElementById(
            "monthlyChart"
        );


    container.innerHTML = "";


    if (months.length === 0) {

        container.innerHTML =
            "<p>No monthly data available.</p>";

        return;
    }


    const maximum =
        Math.max(
            ...months.map(
                item => item.total
            )
        );


    months.forEach(
        function(item) {

            const percentage =
                maximum === 0
                    ? 0
                    : (
                        item.total /
                        maximum
                    ) * 100;


            const div =
                document.createElement(
                    "div"
                );


            div.className = "bar";


            div.innerHTML = `

                <div class="bar-label">

                    <span>
                        ${escapeHTML(
                            item.month
                        )}
                    </span>

                    <span>
                        ₹${Number(
                            item.total
                        ).toFixed(2)}
                    </span>

                </div>


                <div class="bar-background">

                    <div
                        class="bar-fill"
                        style="width:
                            ${percentage}%"
                    >
                    </div>

                </div>

            `;


            container.appendChild(div);

        }
    );

}


/* AI insights */

async function loadAIInsights() {

    try {

        const response =
            await fetch(
                "/ai-insights"
            );


        const result =
            await response.json();


        const insights =
            result.insights;


        displayList(
            "highSpending",
            insights.high_spending_categories
        );


        displayList(
            "patterns",
            insights.spending_patterns
        );


        displayList(
            "suggestions",
            insights.suggestions
        );


        document.getElementById(
            "aiMessage"
        ).textContent =
            insights.message || "";


    } catch (error) {

        console.error(
            "AI insights error:",
            error
        );

    }

}


/* Display list */

function displayList(
    elementId,
    items
) {

    const element =
        document.getElementById(
            elementId
        );


    element.innerHTML = "";


    if (!items ||
        items.length === 0) {

        element.innerHTML =
            "<li>No information available.</li>";

        return;
    }


    items.forEach(
        function(item) {

            const li =
                document.createElement(
                    "li"
                );


            li.textContent =
                item;


            element.appendChild(li);

        }
    );

}


/* Basic HTML escaping */

function escapeHTML(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}
/* Initial page loading */

window.addEventListener(
    "load",
    async function() {

        await loadDashboard();

        await loadExpenses();

        await loadAIInsights();

    }
);