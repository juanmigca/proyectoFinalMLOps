# src/train_mlflow.py
import os
import argparse
import json
import joblib
import tempfile
from pathlib import Path
import subprocess
from datetime import datetime

import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix
import xgboost as xgb
import lightgbm as lgb

ROOT = Path(__file__).resolve().parents[1]  # repo/src -> parent is repo
DATOS_PROCESADOS = ROOT / "datos" / "procesados"
MODELS_DIR = ROOT / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_EXPERIMENT = os.environ.get("MLFLOW_EXPERIMENT_NAME", "credito_experiment")
MLFLOW_URI = os.environ.get("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
mlflow.set_tracking_uri(MLFLOW_URI)
mlflow.set_experiment(DEFAULT_EXPERIMENT)
client = MlflowClient(tracking_uri=MLFLOW_URI)

def ensure_data():
    # Si no existen los CSVs procesados, ejecuta el preprocesamiento
    expected = [DATOS_PROCESADOS / p for p in ("X_train.csv","X_test.csv","y_train.csv","y_test.csv")]
    if not all(p.exists() for p in expected):
        print("[INFO] No encontré datos procesados. Ejecutando preprocesamiento...")
        # llama al script que ya tienes
        subprocess.check_call(["python", "src/data/preprocesamiento.py"])

def load_data():
    X_train = pd.read_csv(DATOS_PROCESADOS / "X_train.csv")
    X_test = pd.read_csv(DATOS_PROCESADOS / "X_test.csv")
    y_train = pd.read_csv(DATOS_PROCESADOS / "y_train.csv").squeeze()
    y_test = pd.read_csv(DATOS_PROCESADOS / "y_test.csv").squeeze()
    return X_train, X_test, y_train, y_test

def make_pipeline(model, model_name):
    return Pipeline([("scaler", StandardScaler()), (model_name, model)])

def _maybe_register_model(run_id, registered_name):
    try:
        model_uri = f"runs:/{run_id}/model"
        mv = client.create_model_version(name=registered_name, source=model_uri, run_id=run_id)
        print(f"[OK] Registro creado: {registered_name} v{mv.version}")
        return mv
    except Exception as e:
        print(f"[WARN] No pude registrar automáticamente: {e}")
        return None

def train_one(model_key, params):
    ensure_data()
    X_train, X_test, y_train, y_test = load_data()

    # Instanciamos modelos por short-key
    if model_key == "logistic":
        model = LogisticRegression(**params, max_iter=2000)
    elif model_key == "rf":
        model = RandomForestClassifier(**params, n_jobs=-1, random_state=42)
    elif model_key == "xgb":
        model = xgb.XGBClassifier(**params, use_label_encoder=False, eval_metric="logloss", random_state=42)
    elif model_key == "lgb":
        model = lgb.LGBMClassifier(**params, random_state=42)
    else:
        raise ValueError("Modelo no soportado")

    pipeline = make_pipeline(model, model_key)

    with mlflow.start_run(run_name=f"{model_key}-{datetime.utcnow().isoformat()}", nested=False) as run:
        run_id = run.info.run_id
        # log params
        mlflow.log_params(params)
        # fit
        pipeline.fit(X_train, y_train)

        # preds & metrics
        preds = pipeline.predict(X_test)
        probs = pipeline.predict_proba(X_test)[:, 1] if hasattr(pipeline, "predict_proba") else None
        acc = float(accuracy_score(y_test, preds))
        mlflow.log_metric("accuracy", acc)
        if probs is not None:
            auc = float(roc_auc_score(y_test, probs))
            mlflow.log_metric("roc_auc", auc)

        # confusion matrix
        tn, fp, fn, tp = confusion_matrix(y_test, preds).ravel()
        mlflow.log_metric("tn", int(tn)); mlflow.log_metric("fp", int(fp))
        mlflow.log_metric("fn", int(fn)); mlflow.log_metric("tp", int(tp))

        # guardar pipeline local y log artifact
        model_fname = MODELS_DIR / f"{model_key}_pipeline.joblib"
        joblib.dump(pipeline, model_fname)
        mlflow.log_artifact(str(model_fname), artifact_path="pipelines")

        # log model in MLflow format (sklearn flavor)
        try:
            mlflow.sklearn.log_model(pipeline, artifact_path="model")
        except Exception as e:
            print(f"[WARN] log_model falló: {e}")

        # intentar registrar en Model Registry (puede fallar si server no permite registry)
        reg_name = f"CreditModel-{model_key}"
        try:
            # si ya existe el nombre, mlflow.create_registered_model fallará; usamos client
            # crear registered model si no existe
            try:
                client.create_registered_model(reg_name)
            except Exception:
                pass
            mv = _maybe_register_model(run_id, reg_name)
            if mv:
                print(f"[OK] Model version: {mv.version}")
        except Exception as e:
            print(f"[WARN] Registro programático falló: {e}")

        print(f"[OK] Run logged: {run_id}")
        return run_id

def parse_params_list(param_pairs):
    params = {}
    if not param_pairs:
        return params
    for p in param_pairs:
        if "=" not in p:
            continue
        k,v = p.split("=",1)
        # try cast
        if v.isdigit():
            v = int(v)
        else:
            try:
                v = float(v)
            except:
                pass
        params[k] = v
    return params

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["logistic","rf","xgb","lgb"], required=True)
    parser.add_argument("--param", action="append", help="param in key=value (repeatable)")
    args = parser.parse_args()

    params = parse_params_list(args.param)
    train_one(args.model, params)
