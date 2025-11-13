# src/tune_optuna_mlflow.py
import os
import optuna
import mlflow
from mlflow.tracking import MlflowClient
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

DATOS_PROCESADOS = "datos/procesados"
X_train = pd.read_csv(os.path.join(DATOS_PROCESADOS, "X_train.csv"))
y_train = pd.read_csv(os.path.join(DATOS_PROCESADOS, "y_train.csv")).squeeze()

mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI","http://127.0.0.1:5000"))
mlflow.set_experiment("credito_optuna_rf")

def objective(trial):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 50, 500),
        "max_depth": trial.suggest_int("max_depth", 3, 20),
        "min_samples_split": trial.suggest_int("min_samples_split", 2, 10),
    }
    with mlflow.start_run(nested=True):
        mlflow.log_params(params)
        model = Pipeline([("scaler", StandardScaler()), ("rf", RandomForestClassifier(**params, n_jobs=-1, random_state=42))])
        score = cross_val_score(model, X_train, y_train, cv=3, scoring="roc_auc").mean()
        mlflow.log_metric("cv_roc_auc", float(score))
    return score

if __name__ == "__main__":
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=30)
    print("Best params:", study.best_params)
