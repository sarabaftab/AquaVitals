document.addEventListener("DOMContentLoaded", function () {
  const predictButton = document.getElementById("predictButton");
  const dateRangePickerInput = document.getElementById("date-range-picker");
  const predictionCard = document.getElementById("predictionCard");
  const predictionLeft = document.getElementById("predictionLeft");
  const predictionTableBody = document.querySelector("#predictionTable tbody");

  // Initialize Litepicker
  const picker = new Litepicker({
    element: dateRangePickerInput,
    singleMode: false,
    numberOfMonths: 2,
    numberOfColumns: 2,
    format: "YYYY-MM-DD",
    minDate: new Date(),
    maxDate: addDays(new Date(), 5),
    maxDays: 5,
    tooltipText: { one: "day", other: "days" },
    tooltipNumber: (totalDays) => totalDays,
  });

  // Helper function to add days
  function addDays(date, days) {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
  }
  // On Predict button click
  predictButton.addEventListener("click", async function () {
    const selectedDates = dateRangePickerInput.value.split(" - ");
    const fishCount = document.getElementById("fish-count").value;

    if (selectedDates.length !== 2 || !selectedDates[0] || !selectedDates[1]) {
      alert("Please select a valid start and end date.");
      return;
    }

    if (!fishCount) {
      alert("Please enter the fish count.");
      return;
    }

    const startDate = selectedDates[0];
    const endDate = selectedDates[1];

    predictionCard.style.display = "block";
    // predictionLeft.innerHTML = `<p>Processing...</p>`;
    predictionTableBody.innerHTML = `<tr><td colspan="5">Fetching prediction...</td></tr>`;

    try {
      const processRes = await fetch("/process_dates", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          start_date: startDate,
          end_date: endDate,
          fish_count: fishCount,
        }),
      });

      const weatherData = await processRes.json();

      // predictionLeft.innerHTML = `
      //   <h4>Selected Range</h4>
      //   <p><strong>Start:</strong> ${weatherData.start_date}</p>
      //   <p><strong>End:</strong> ${weatherData.end_date}</p>
      //   <p><strong>Fish Count:</strong> ${weatherData.fish_count}</p>
      //   <p><strong>Date Range:</strong> ${weatherData.date_range} days</p>
      // `;

      const predictionRes = await fetch("/predict_api", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(weatherData),
      });

      const predictionData = await predictionRes.json();

      if (!Array.isArray(predictionData)) {
        predictionTableBody.innerHTML = `<tr><td colspan="5">Error: ${predictionData.error}</td></tr>`;
        return;
      }

      populatePredictionTable(predictionData);
    } catch (error) {
      console.error("🔥 Error during prediction:", error);
      predictionLeft.innerHTML = `<p>Error fetching data</p>`;
      predictionTableBody.innerHTML = `<tr><td colspan="5">Failed to generate prediction</td></tr>`;
    }
  });

  function populatePredictionTable(data) {
    predictionTableBody.innerHTML = "";

    data.forEach((entry) => {
      const row = document.createElement("tr");
      row.innerHTML = `
          <td>${entry.date}</td>
          <td>${entry.am_transparency.toFixed(2)}</td>
          <td>${entry.pm_transparency.toFixed(2)}</td>
          <td>${entry.predicted_survival.toFixed(2)}</td>
          <td>${entry.risk_level}</td>
        `;
      predictionTableBody.appendChild(row);
    });
  }
});
