import pandas as pd


df = pd.read_excel(r"D:\THB\Masterarbeit\scrapy_\immoscout\immoscout\dataset\5_Machine Learning\data_2.xlsx")

from sklearn.model_selection import train_test_split
#Add the target
X = df.drop(['price'], axis=1)
y = df['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state=42)

print(X_train.shape)

import optuna
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
#from sklearn.metrics import mean_squared_error




class ModelOptimization:
    def __init__(self, X_train, X_test, y_train, y_test):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

    def objective(self, trial):
        
        fit_intercept = trial.suggest_categorical('fit_intercept', [True, False])
        copy_X = trial.suggest_categorical('copy_X', [True, False])
        n_jobs = trial.suggest_int('n_jobs', 2, 5000)
        positive = trial.suggest_categorical('positive', [True, False])
        
       
        
        model = LinearRegression(fit_intercept = fit_intercept, copy_X = copy_X, 
                                      n_jobs = n_jobs, positive = positive)
        
        model.fit(self.X_train, self.y_train)
        return model.score(self.X_test, self.y_test)
    
if __name__ == '__main__':
    model = ModelOptimization(X_train, X_test, y_train, y_test)
    study = optuna.create_study(direction='maximize')
    study.optimize(model.objective, n_trials=1)
    print(f"Best parameters:{study.best_params}")
    print(f"Best value:{study.best_value}")


