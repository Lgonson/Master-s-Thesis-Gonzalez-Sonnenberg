# Master’s thesis Price prediction of real estate using machine learning techniques in the city of Berlin
**Overview**

This project aims to forecast the purchasing prices of homes in Berlin using various machine learning algorithms. The dataset was gathered through web scraping from two major German real estate platforms, Immowelt and Wohnungsboerse, resulting in a dataset of 14,869 observations, each with 14 features.

**Data Collection**
The data for this study was sourced from:

- [Immowelt](https://www.immowelt.de/)
- [Wohnungsboerse](https://www.wohnungsboerse.net/)

Web scraping techniques were employed to gather data on residential properties listed on these sites, focusing on houses located within Berlin.

**Dataset**

    Observations: 14,869
    Features: 14 attributes per observation
    Data Split:
        Training Set: 75% (11,115 observations)
        Test Set: 25% (3,718 observations)

**Objective**

The objective is to determine the purchasing prices of Berlin homes and identify the algorithm that provides the most accurate price forecasts.

**Methodology**

**Algorithms Used**

Four machine learning algorithms were trained and evaluated:

    Linear Regression
    Decision Trees
    Random Forest
    Adaptive Boosting (AdaBoost)

**Evaluation Metrics**

To assess the performance of each model, the following metrics were used:

    Coefficient of Determination (R²)
    Mean Squared Error (MSE)
    Root Mean Squared Error (RMSE)
    Mean Absolute Error (MAE)

## Results

The models were evaluated on the test set, with **Random Forest** achieving the best performance:

- **Random Forest**: R² = 83.90%
- **Decision Trees**: R² = 77,34%
- **Random Forest**: R² = 67,50%
- **Linear Regression**: R² = 57.56% 

