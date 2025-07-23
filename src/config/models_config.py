from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.linear_model import RidgeClassifier
from xgboost import XGBClassifier

MODELS_CONFIG = {
    'QDA': {
        'model': QuadraticDiscriminantAnalysis(),
        'params': {
            'reg_param': [0.0, 0.001, 0.01, 0.1, 0.2],
            'store_covariance': [True, False, True, False, True],
            'tol': [1e-4, 1e-3, 1e-2, 1e-1, 1.0],
            'priors': [
                [0.5, 0.5],
                [0.6, 0.4],
                [0.4, 0.6],
                [0.7, 0.3],
                [0.3, 0.7]
            ]
        }
    },
    'RidgeClassifier': {
        'model': RidgeClassifier(random_state=42),
        'params': {
            'alpha': [0.01, 0.1, 1.0, 10.0, 100.0],
            'fit_intercept': [True, False, True, False, True],
            'solver': ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg'],
            'tol': [1e-4, 1e-3, 1e-2, 1e-1, 1.0]
        }
    },
    'RandomForest': {
        'model': RandomForestClassifier(random_state=42),
        'params': {
            'n_estimators': [50, 100, 200, 300, 500],
            'max_depth': [5, 10, 15, 20, None],
            'min_samples_split': [2, 5, 10, 15, 20],
            'min_samples_leaf': [1, 2, 4, 6, 8]
        }
    },
    'GradientBoosting': {
        'model': GradientBoostingClassifier(random_state=42),
        'params': {
            'n_estimators': [50, 100, 150, 200, 300],
            'learning_rate': [0.01, 0.05, 0.1, 0.15, 0.2],
            'max_depth': [3, 5, 7, 9, 12],
            'subsample': [0.6, 0.7, 0.8, 0.9, 1.0]
        }
    },
    'KNN': {
        'model': KNeighborsClassifier(),
        'params': {
            'n_neighbors': [3, 5, 7, 10, 15],
            'weights': ['uniform', 'distance', 'uniform', 'distance', 'uniform'],
            'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute', 'auto'],
            'metric': ['euclidean', 'manhattan', 'minkowski', 'chebyshev', 'euclidean']
        }
    },
    'XGBoost': {
        'model': XGBClassifier(random_state=42, eval_metric='logloss'),
        'params': {
            'n_estimators': [50, 100, 200, 300, 500],
            'learning_rate': [0.01, 0.05, 0.1, 0.2, 0.3],
            'max_depth': [3, 5, 7, 9, 12],
            'subsample': [0.6, 0.7, 0.8, 0.9, 1.0]
        }
    }
}

TRAINING_CONFIG = {
    'cv_folds': 5,
    'scoring': 'accuracy',
    'n_jobs': -1,
    'verbose': 1,
    'test_size': 0.3,
    'random_state': 42
}