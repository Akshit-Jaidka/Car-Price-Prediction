# Car Sale Price Prediction

A Machine Learning web application that predicts the resale value of used cars based on vehicle specifications such as manufacturing year, kilometers driven, ownership history, city, transmission type, body type, make, model, and other attributes.

## Features

* Predicts used car sale prices in real time
* Handles missing values using imputation
* Encodes categorical variables using One-Hot Encoding
* Random Forest Regression model
* Interactive Streamlit web interface

## Model Performance

* Algorithm: Random Forest Regressor
* R² Score: ~0.89

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Streamlit

## Run Locally

Clone the repository:

```bash
git clone <repository-url>
cd Car-Price-Prediction
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## Project Structure

```text
app.py
Car_sale_price_model.pkl
ct.pkl
num_imputer.pkl
cat_imputer.pkl
requirements.txt
runtime.txt
README.md
```

## Author

Akshit Jaidka
B.Tech CSE, NSUT
