async function fetchESGData(year) {
    let response = await fetch(`/get_esg_trends/${year}`);
    let data = await response.json();
    return data;
}

async function renderChart() {
    let selectedYear = document.getElementById("yearFilter").value;
    let selectedCompany = document.getElementById("companyFilter").value;
    
    let esgData = await fetchESGData(selectedYear);

    let labels = ["2020", "2021", "2022", "2023"];
    
    esgData.forEach((entry) => {
        let ctx = document.getElementById(entry.metric).getContext("2d");

        new Chart(ctx, {
            type: "line",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: `Company ESG (${selectedCompany})`,
                        data: entry.company,
                        borderColor: "blue",
                        fill: false
                    },
                    {
                        label: "External ESG",
                        data: entry.external,
                        borderColor: "green",
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                title: { display: true, text: entry.metric }
            }
        });
    });
}

document.addEventListener("DOMContentLoaded", renderChart);
