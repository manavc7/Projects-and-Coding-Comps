# Stock Market Direction Prediction

This project is focused on predicting whether stock indices (like the S&P 500) or individual stocks will increase or decrease in value the next trading day. The model combines historical market data with machine learning techniques to make informed predictions.

## Motivation
The main reason I decided to create this project was to experiment with machine learning tools within python. Being someone who is aiming for a career in quantitative finance, I hope that this project gives me a taste of the type of programming that one might encounter in this industry.

# Project Overview

## Data Source:
I used historical data from Yahoo Finance for the S&P 500 index (^GSPC), including features like open, close, high, low prices, and trading volume. 

## Modelling
For my modelling approach I implemented an ensemble learning approach combining a RandomForestClassifier and XGBoost through a VotingClassifier. This method leveraged the strengths of both models for improved prediction accuracy. It generates additional predictors using rolling averages and trend indicators over multiple time horizons, enhancing the model's ability to capture market patterns.

## Backtesting:
The model is rigorously backtested over historical data to evaluate its performance, with results showing promising accuracy in predicting market direction. The ensemble model proved to acheive higher precision compared to individual models, demonstrating its effectiveness in predicting market trends. By using a combination of the RandomForest and XGBoost models, the ensemble approach reduces overfitting and improves generalisation across different market conditions.

## Prediction:
In terms of its usage, the trained model aims to predict the likelihood of the market moving up or down the next trading day based on the latest available data.

## Customisation: 
The project can be extended to other stock indices or individual stocks by modifying the data source and retraining the models. However, the predictive accuracy will not always be maintained


