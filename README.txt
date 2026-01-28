# URL Phishing Detection System
A machine learning–based system to classify URLs as phishing or benign using neural networks, built and deployed with FastAPI.

## Problem Statement
Phishing URLs pose a major cybersecurity threat by mimicking legitimate websites. 
The goal of this project is to automatically detect phishing URLs using machine learning techniques based on URL-level features.

## Approach
* Extracted 50+ URL-based features from the PhiUSIIL Phishing URL Dataset.
* Initially experimented with Random Forest, which resulted in overfitting.
* Switched to a Multi-Layer Perceptron (Neural Network) to improve generalization.
* Applied robust scaling, class weighting, dropout, and early stopping.
* Reduced false positives by improving model behavior on well-known benign URLs.

## Tech Stack
* Python
* Scikit-learn
* Neural Networks (MLP)
* FastAPI
* Uvicorn
* React.js
* Linux

## How to Run
1. Clone the repository 
   git clone https://github.com/AshikChristober/url-phishing-detection /.git

2. Install dependencies 
   pip install -r requirements.txt

3. Start the backend 
   uvicorn main:app --reload

4. Access the API 
   http://127.0.0.1:8000/docs
   
## Results
* Achieved 90%+ accuracy on the phishing URL dataset.
* Improved generalization compared to baseline Random Forest model.

## Future Improvements
 Integrate real-time URL fetching.
 Improve feature engineering for short URLs.
 Deploy the model using Docker.
