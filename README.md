# 🎯 IBM SkillsBuild Capstone Project – User Ad Click Prediction

Welcome to the **User Ad Click Prediction Capstone Project**, created as part of the IBM SkillsBuild learning path. This project applies machine learning to predict whether a user will click on an advertisement based on demographic and behavioral data.

---

## 📌 Project Objective

The objective is to build a supervised machine learning model that predicts if a user will click on an ad, using features such as age, gender, estimated salary, and social network behavior.

---

## 🗂️ Project Structure

IBM-Skillsbuild-Capstone-Project/
│
- ├── User_add_click_prediction.ipynb # Main notebook: EDA, preprocessing, model training
- ├── appflask.py # Flask web app for prediction
- ├── Main.py # Entry point (if used for deployment)
- ├── model_pred1.pkl # Trained ML model (pickled)
- ├── dataset.pkl # Pickled dataset (optional)
- ├── Social_Network_Ads.csv # Dataset used for training/testing
- ├── User_Ad_Click_Prediction_Capstone_Project.pptx # Presentation slides
- ├── virtualEnv/ # Virtual environment files
- ├── pycache/ # Python cache files
- └── README.md # Project documentation (you're here)

yaml
Copy
Edit

---

## 🧠 Technologies & Libraries Used

- Python
- Pandas, NumPy
- Matplotlib, Seaborn
- Scikit-learn
- Flask
- Pickle

---

## 📊 Dataset

- **Name:** `Social_Network_Ads.csv`
- **Features:** Age, Estimated Salary, Gender, Purchased (target)
- The dataset is used to train and evaluate a classification model.

---

## 🚀 How to Run the Project

### 1. Clone the repository:
```bash
git clone https://github.com/manvichaturvedi/IBM-Skillsbuild-Capstone-Project.git
cd IBM-Skillsbuild-Capstone-Project
2. Set up the virtual environment:
bash
Copy
Edit
python -m venv virtualEnv
source virtualEnv/bin/activate  # On Windows: virtualEnv\Scripts\activate
pip install -r requirements.txt  # Create this file if not added yet
3. Run the Flask App:
bash
Copy
Edit
python appflask.py
Navigate to http://127.0.0.1:5000/ in your browser to use the ad click prediction web app.

📎 Presentation
📊 A PowerPoint presentation explaining the project's pipeline, evaluation metrics, and results is included:
User_Ad_Click_Prediction_Capstone_Project.pptx

✅ Features Implemented
Exploratory Data Analysis (EDA)

Feature scaling and preprocessing

Binary classification model

Model saving/loading using Pickle

Web app deployment using Flask

Clean UI for predictions based on user input

🙋‍♀️ Author
Manvi Chaturvedi


⭐ Support
If you found this project helpful or inspiring, don’t forget to star ⭐ the repository!

