
const ctx = document.getElementById('fraudChart').getContext('2d');
const fraudChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: ['Fraud', 'Not Fraud'],
    datasets: [{
      label: 'Predictions',
      data: [0, 0],
      backgroundColor: ['red', 'green']
    }]
  }
});

async function checkFraud() {
  const amount = document.getElementById("amount").value;
  const time = document.getElementById("time").value;

  if (!amount || !time) {
    document.getElementById("output").innerText = "Please enter both values.";
    return;
  }

  try {
    const response = await fetch(`/predict/${amount}/${time}`);
    const result = await response.json();

    const output = document.getElementById("output");
    if (result.is_fraud === 1) {
      output.innerText = "Prediction: Fraud";
      output.className = "fraud";
      fraudChart.data.datasets[0].data[0] += 1; // increment fraud count
    } else {
      output.innerText = "Prediction: Not Fraud";
      output.className = "safe";
      fraudChart.data.datasets[0].data[1] += 1; // increment safe count
    }
    fraudChart.update();

  } catch (error) {
    document.getElementById("output").innerText = "Error connecting to server.";
  }
}

