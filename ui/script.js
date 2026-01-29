async function predict() {
  const symbol = document.getElementById("symbol").value.trim();
  const resultDiv = document.getElementById("result");
  const loading = document.getElementById("loading");

  if (!symbol) {
    alert("Please enter a stock symbol");
    return;
  }

  resultDiv.innerHTML = "";
  loading.style.display = "block";

  try {
    const response = await fetch(`http://127.0.0.1:8000/predict?symbol=${symbol}`);
    const data = await response.json();

    if (data.error) {
      resultDiv.innerHTML = `<p style="color:red">${data.error}</p>`;
    } else {
      resultDiv.innerHTML = `
        <b>Stock:</b> ${data.stock}<br>
        <b>Current Close:</b> ₹${data.current_close}<br>
        <b>Predicted Low:</b> ₹${data.predicted_low}<br>
        <b>Predicted High:</b> ₹${data.predicted_high}<br>
        <b>Range:</b> ${data.expected_range}<br>
        <b>Stock Move:</b> ${data.stock_move}<br>
        <b>NIFTY Trend:</b> ${data.index_trend}<br>
        <b>News Sentiment:</b> ${data.news_sentiment}<br>
        <b>Final Market Move:</b> <b>${data.final_market_move}</b><br>
        <b>Confidence:</b> ${data.confidence}
      `;
    }
  } catch (err) {
    resultDiv.innerHTML = "<p style='color:red'>Server error</p>";
  }

  loading.style.display = "none";
}
