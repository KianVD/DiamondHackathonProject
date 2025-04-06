# DiamondHackathonProject
# 🧠 CredLess – No credit, no problem !!!

This is a fullstack web application that combines a **React frontend** with a **Flask backend** to analyze user data and generate concise credit risk reports using AI.

---

## 🗂️ Project Structure

```
credit-risk-analyzer/
├── frontend/              # React frontend
│   ├── public/
│   ├── src/
│   └── package.json
│
├── backend/               # Flask backend
│   ├── scripts/
        ├── app.py
│   └── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

- Node.js (for frontend)
- Python 3.8+ but <=3.12(for backend)
- npm or yarn

---

## ⚙️ Frontend Setup (React)

```bash
cd frontend
npm install
npm start
```

> Runs React app on [http://localhost:3000](http://localhost:3000)

---

## ⚙️ Backend Setup (Flask)

```bash
cd backend
python -m venv venv
source venv/bin/activate     # On Windows use venv\Scripts\activate
pip install -r requirements.txt
cd scripts
python app.py
```

> Starts backend at [http://localhost:5000](http://localhost:5000)

---

## 🔌 API Endpoints

| Method | Endpoint            | Description                            |
|--------|---------------------|----------------------------------------|
| `GET`  | `/generate-report`  | Generates a credit risk report         |

---

## 🎯 Features

- 📥 Upload & process user JSON data
- 🧠 Generate AI-powered risk reports
- 📄 Export or display PDF report (backend)
- ⚛️ Interactive React frontend
- 📡 RESTful API integration

---

## 🚢 Deployment

You can deploy this app using:

- **Frontend:** Vercel, Netlify
- **Backend:** Render, Railway, Heroku, AWS EC2

---

## 🧰 Tech Stack

- **Frontend:** React, JavaScript, CSS
- **Backend:** Flask, Python, ReportLab (PDF), Gemini, Auth0
- **Others:** Git, REST APIs

---

## step-by-step explanation

---

### 1️⃣ **Extract Data Files**

- The system accepts raw user data files in CSV format 
- These files contain various features
- The backend parses these files into a structured format (like Pandas DataFrames) to prepare for further processing.

---

### 2️⃣ **Do Clustering to Categorize Into Low, Medium, and High Risk**

- **Unsupervised Learning**: 
  - Before training any model, the system performs **clustering** (e.g., using K-Means or DBSCAN) on historical or simulated credit datasets.
- **Goal**: Automatically assign a **risk label** to each record:
  - `Low Risk`, `Medium Risk`, `High Risk`
- These labels serve as a **pseudo ground truth** for training the neural network.

---

### 3️⃣ **Train a Basic Neural Network on the Labelled Data**

- A simple **feedforward neural network** (using PyTorch or TensorFlow) is trained using the features and the risk labels from the clustering step.
- Architecture:
  - Input layer → Dense layers with Dropouts → ReLU activation → Output layer (with softmax or sigmoid for classification)
- This model learns to predict the risk category based on new unseen data.

---

### 4️⃣ **Make Predictions on the User Data**

- When a user uploads their data:
  - It is **preprocessed** to match the format expected by the neural net (scaling, encoding, etc.).
  - The trained model runs **inference** to output a **risk score** or category (e.g., `High Risk`).
- These predictions are stored temporarily and used in the report generation step.

---

### 5️⃣ **Use Gemini APIs to Generate Reports and Gather Insights**

- The predicted results are passed to **Google Gemini APIs** (or any Gemini-powered LLM endpoint) along with the original user data.
- The LLM is prompted to:
  - Generate a **concise, natural language explanation** of the risk.
  - Suggest actionable **financial tips** or highlight any **red flags**.
- Output: A well-structured, **human-readable report** in text form.

---

### 6️⃣ **Use Auth0 to Authorize Downloads for the PDF**

- To secure report downloads:
  - **Auth0** is integrated with the frontend and backend.
  - Users must **log in** using OAuth (e.g., Google, GitHub, etc.) before they can trigger a download.
- Backend checks for a valid **JWT access token** before allowing the request to proceed.
- Once verified, the system generates the **PDF version** of the report and displays it or makes it downloadable .

