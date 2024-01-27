import pandas as pd


df = pd.read_excel(r"D:\THB\Masterarbeit\scrapy_\immoscout\immoscout\dataset\5_Machine Learning\data.xlsx")
#df = pd.read_excel(r"D:\THB\Masterarbeit\scrapy_\immoscout\immoscout\dataset\5_Machine Learning\data_without_duplicates.xlsx")

from sklearn.model_selection import train_test_split
#Add the target
X = df.drop(['price'], axis=1)
y = df['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state=42)

print(X_train.shape)

import optuna
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error



class ModelOptimization:
    def __init__(self, X_train, X_test, y_train, y_test):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

    def objective(self, trial):
        
        criterion = trial.suggest_categorical('criterion', ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'])
        splitter = trial.suggest_categorical('splitter', ['best', 'random'])
        max_depth = trial.suggest_int("max_depth", 2, 1000)
        min_samples_split = trial.suggest_int('min_samples_split', 2, 20)
        min_samples_leaf = trial.suggest_int('min_samples_leaf', 2, 20)
        max_features = trial.suggest_int('max_features', 2, 10)
        random_state = trial.suggest_int('random_state', 42, 42)
        
        model = DecisionTreeRegressor(criterion = criterion, splitter = splitter, 
                                      max_depth = max_depth, min_samples_split= min_samples_split,
                                      min_samples_leaf = min_samples_leaf, max_features = max_features,
                                      random_state = random_state)
        
        model.fit(self.X_train, self.y_train)
        return model.score(self.X_test, self.y_test)
    
if __name__ == '__main__':
    
    model = ModelOptimization(X_train, X_test, y_train, y_test)
    study = optuna.create_study(direction='maximize')
    study.optimize(model.objective, n_trials=1500)
    print(f"Best parameters:{study.best_params}")
    print(f"Best value:{study.best_value}")
