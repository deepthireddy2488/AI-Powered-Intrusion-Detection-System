🛡️ AI-Powered Intrusion Detection System

An AI-powered Intrusion Detection System (IDS) that analyzes network traffic to detect malicious activities, classify attacks, assign threat severity, and provide security recommendations through a web-based dashboard.

## 🚀 Features

* User Registration and Login with JWT Authentication
* AI-Based Network Traffic Analysis
* CSV Upload and Batch Prediction
* Detection of BENIGN and Malicious Traffic
* Attack Classification and Severity Detection
* Security Recommendations
* Live Network Monitoring using Scapy
* Real-Time Packet Capture and Analysis
* Attack Logs and Prediction History
* Security Dashboard and Statistics
* PDF Security Report Generation

## 🧠 How the System Works

1. User registers and logs into the system.
2. User selects **CSV Prediction** or **Live Network Monitoring**.
3. CSV traffic data or live network packets are collected.
4. Network traffic features are processed and analyzed.
5. The trained Machine Learning model predicts whether traffic is benign or an attack.
6. Detected attacks are classified and assigned a severity level.
7. Security recommendations and alerts are generated.
8. Predictions and attack logs are stored in the database.
9. Results are displayed on the dashboard and reports can be generated.

## 🛠️ Technology Stack

**Frontend:** React.js, Vite, Bootstrap, Chart.js
**Backend:** Python, FastAPI, SQLAlchemy
**Database:** PostgreSQL
**Machine Learning:** Scikit-learn, Pandas, NumPy, Joblib, XGBoost
**Network Monitoring:** Scapy
**Authentication:** JWT
**Dataset:** CICIDS2017

## 🧠 Machine Learning Workflow
CICIDS2017 Dataset
        ↓
Data Preprocessing
        ↓
Feature Preparation
        ↓
Model Training & Evaluation
        ↓
Attack Prediction

## 📂 Project Structure

AI-Powered-Intrusion-Detection-System/
│
├── backend/        # FastAPI backend
├── frontend/       # React frontend
├── dataset/        # Network traffic dataset
├── ml/             # ML models and scripts
├── .gitignore
└── README.md

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/deepthireddy2488/AI-Powered-Intrusion-Detection-System.git
```

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## 🎯 Future Enhancements

* Real-time alerts and notifications
* WebSocket-based monitoring
* Advanced AI/DL models
* Cloud deployment
* Automated threat response

## 👩‍💻 Author
Deepthi Reddy
**Deepthi Reddy**
B.Tech Final Year Major Project
