document.getElementById("fetchData").addEventListener("click", async () => {
    const apiUrl = "https://uj7xmcs218.execute-api.ap-northeast-1.amazonaws.com/default/stocks"; // ← ここをAPIのURLに変更
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error(`HTTPエラー！ステータス: ${response.status}`);
        }
        const data = await response.json();
        displayData(data);
    } catch (error) {
        console.error("データ取得エラー:", error);
    }
});

function displayData(stocks) {
    const tableBody = document.getElementById("stockTable");
    tableBody.innerHTML = ""; // 一度リセット

    stocks.forEach(stock => {
        const row = document.createElement("tr");
        row.innerHTML = \`
            <td>\${stock.Ticker}</td>
            <td>\${stock.CompanyNameJP}</td>
            <td>\${stock.PBR.toFixed(2)}</td>
        \`;
        tableBody.appendChild(row);
    });
}
