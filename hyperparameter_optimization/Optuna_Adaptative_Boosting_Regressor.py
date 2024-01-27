import pandas as pd


df = pd.read_excel(r"D:\THB\Masterarbeit\scrapy_\immoscout\immoscout\dataset\5_Machine Learning\data_2.xlsx")

from sklearn.model_selection import train_test_split
#Add the target
X = df.drop(['price'], axis=1)
y = df['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state=42)

print(X_train.shape)

import optuna
from sklearn.ensemble import AdaBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error



class ModelOptimization:
    def __init__(self, X_train, X_test, y_train, y_test):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

    def objective(self, trial):
        loss = trial.suggest_categorical("loss", ['linear', 'square', 'exponential'])
        n_estimators = trial.suggest_int('n_estimators', 50, 10000)
        learning_rate = trial.suggest_float('learning_rate', 0.0001, 0.02)
        random_state = trial.suggest_int('random_state', 42, 42)
        
        
        
        
        model = AdaBoostRegressor(loss = loss, n_estimators = n_estimators, 
                                      learning_rate = learning_rate, random_state = random_state)
        
        model.fit(self.X_train, self.y_train)
        return model.score(self.X_test, self.y_test)
    
if __name__ == '__main__':
    model = ModelOptimization(X_train, X_test, y_train, y_test)
    study = optuna.create_study(direction='maximize')
    study.optimize(model.objective, n_trials=150)
    print(f"Best parameters:{study.best_params}")
    print(f"Best value:{study.best_value}")
