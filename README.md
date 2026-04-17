Fraud Detection Dashboard

A cloud‑deployed web application for detecting fraudulent transactions.  
Built with **Flask**, **Gunicorn**, **Nginx**, and deployed on **AWS EC2**.

---

## Project Structure
Fraud_detection_COMP4442_Project/
│── app.py                # Flask backend entrypoint
│── fraud_detection.py     # Fraud detection model logic
│── transactions.csv       # Sample dataset
│── index.html             # Frontend dashboard
│── style.css              # Dashboard styling
│── script.js              # Frontend logic (AJAX calls)
│── static/                # Static assets folder


---

Setup on EC2

1. Upload Project
bash
scp -i ~/.ssh/fraud-key.pem -r Fraud_detection_COMP4442_Project ec2-user@<EC2_PUBLIC_DNS>:/home/ec2-user/

2. Connect to EC2
ssh -i ~/.ssh/fraud-key.pem ec2-user@<EC2_PUBLIC_DNS>

3. Install Dependencies
sudo yum update -y
sudo yum install python3-pip nginx -y
pip3 install flask gunicorn scikit-learn pandas numpy

-Run Backend with Gunicorn
Create a systemd service:
/etc/systemd/system/fraud.service

[Unit]
Description=Gunicorn instance to serve Fraud Detection app
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/Fraud_detection_COMP4442_Project
ExecStart=/usr/local/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target

Enable service:
sudo systemctl daemon-reload
sudo systemctl start fraud
sudo systemctl enable fraud


-Configure Nginx

/etc/nginx/conf.d/fraud.conf

server {
    listen 80;
    server_name <EC2_PUBLIC_DNS>;

    # Serve frontend
    location / {
        root /home/ec2-user/Fraud_detection_COMP4442_Project;
        index index.html;
    }

    # Serve static assets
    location /static/ {
        alias /home/ec2-user/Fraud_detection_COMP4442_Project/static/;
    }

    # Proxy backend API
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

-Access Dashboard
Open in browser:
http://<EC2_PUBLIC_DNS>/

-Frontend → Backend Connection
In script.js, example AJAX call:

javascript
fetch('/api/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ transaction: {...} })
})
.then(res => res.json())
.then(data => {
    console.log('Prediction:', data.result);
});

-To stop Gunicorn service:
sudo systemctl stop fraud

-To restart:
sudo systemctl restart fraud

---
Frontend served by Nginx (HTML/CSS/JS).

Backend served by Gunicorn (Flask), proxied via /api.

Accessible via EC2 public DNS on port 80.
---
by Anoushka ^_^




