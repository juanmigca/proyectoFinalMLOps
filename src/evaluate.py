# src/evaluate_mlflow.py
import os
import joblib
import mlflow
import pandas as pd
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

DATOS = "datos/procesados"
MODEL_PATH = "models/rf_pipeline.joblib"  # cambia según el pipeline que guardaste

mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI","http://127.0.0.1:5000"))
mlflow.set_experiment("credito_evaluation_final")

if __name__ == "__main__":
    X_test = pd.read_csv(os.path.join(DATOS, "X_test.csv"))
    y_test = pd.read_csv(os.path.join(DATOS, "y_test.csv")).squeeze()

    # intenta cargar pipeline local
    if os.path.exists(MODEL_PATH):
        pipeline = joblib.load(MODEL_PATH)
    else:
        raise FileNotFoundError(MODEL_PATH + " no existe. Ejecuta train_mlflow.py primero.")

    preds = pipeline.predict(X_test)
    probs = pipeline.predict_proba(X_test)[:,1] if hasattr(pipeline, "predict_proba") else None

    acc = accuracy_score(y_test, preds)
    auc = roc_auc_score(y_test, probs) if probs is not None else None
    report = classification_report(y_test, preds, output_dict=True)

    with mlflow.start_run(run_name="final_eval"):
        mlflow.log_metric("accuracy", float(acc))
        if auc is not None:
            mlflow.log_metric("roc_auc", float(auc))
        # guardar report como artifact
        import json
        with open("evaluation_report.json","w") as f:
            json.dump(report, f, indent=2)
        mlflow.log_artifact("evaluation_report.json")
    print("Evaluation: acc=",acc, "auc=",auc)
