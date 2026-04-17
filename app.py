from flask import Flask, render_template, request, jsonify
import fraud_detection  # your fraud detection logic

app = Flask(__name__)

# Serve index.html from static
@app.route('/')
def index():
    return app.send_static_file("index.html")

# Prediction API
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    amount = float(data.get("amount", 0))
    time = float(data.get("time", 0))
    result = fraud_detection.check_transaction(amount, time)
    return jsonify({"prediction": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


