import pandas as pd


df = pd.read_excel(r"D:\THB\Masterarbeit\scrapy_\immoscout\immoscout\dataset\5_Machine Learning\data_2.xlsx")


from sklearn.model_selection import train_test_split
#Add the target
X = df.drop(['price'], axis=1)
y = df['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 42)

print(X_train.shape)

import optuna
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from optuna.samplers import TPESampler
import optuna.visualization as vis



class ModelOptimization:
    def __init__(self, X_train, X_test, y_train, y_test):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

    def objective(self, trial):
        
        n_estimators = trial.suggest_int('n_estimators', 140, 180)
        criterion = trial.suggest_categorical("criterion", ['squared_error'])#, 'absolute_error', 'friedman_mse', 'poisson'])
        max_depth = trial.suggest_int('max_depth', 5, 45)
        min_samples_split = trial.suggest_int('min_samples_split', 2, 7)
        min_samples_leaf = trial.suggest_int("min_samples_leaf", 2, 7)
        max_features = trial.suggest_int('max_features', 2, 15)
        max_leaf_nodes = trial.suggest_int('max_leaf_nodes', 6000, 100000)
        bootstrap = trial.suggest_categorical('bootstrap', [True, True])
        oob_score = trial.suggest_categorical('oob_score', [True, False])
        random_state = trial.suggest_int('random_state', 42, 42)
        
        
        
        
        
        model = RandomForestRegressor(n_estimators = n_estimators, criterion = criterion, max_depth=max_depth, min_samples_split = min_samples_split, 
                                      min_samples_leaf=min_samples_leaf, 
                                      max_features=max_features, max_leaf_nodes=max_leaf_nodes, #min_impurity_decrease = min_impurity_decrease,
                                      bootstrap = bootstrap, oob_score = oob_score, 
                                      random_state = random_state)
        
        model.fit(self.X_train, self.y_train)
        return model.score(self.X_test, self.y_test)
    
if __name__ == '__main__':
    #sampler = optuna.samplers.RandomSampler()
    pruner = optuna.pruners.NopPruner()
    
    model = ModelOptimization(X_train, X_test, y_train, y_test)
    sampler = TPESampler(seed=42)
    study = optuna.create_study(direction='maximize', sampler = sampler)
    study.optimize(model.objective, n_trials= 250)
    print(f"Best parameters:{study.best_params}")
    print(f"Best value:{study.best_value}")
    optuna.visualization.plot_optimization_history(study)
    optuna.visualization.plot_param_importances(study)
    optuna.visualization.plot_slice(study)
        
        
        

