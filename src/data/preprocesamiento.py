from __future__ import annotations
import json
from pathlib import Path
from typing import Tuple, Dict, Any, List

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# Paths
RAW_DIR = Path("../../datos/raw")
OUT_DIR = Path("../../datos/procesados")
CONFIG_PATH = Path("gen_config.json")

# Helpers
def amortization_payment(monto: float, tasa_anual: float, meses: int) -> float:
    """Cuota mensual de un préstamo amortizable. tasa_anual en decimal (0.30 = 30%)."""
    if meses is None or meses <= 0:
        return 0.0
    r = float(tasa_anual) / 12.0
    if r == 0:
        return float(monto) / meses
    return (monto * r) / (1 - (1 + r) ** (-meses))

def clip01(x: float, a: float = 0.0, b: float = 1.0) -> float:
    return max(a, min(b, float(x)))

def parse_income_bin(rango: str) -> float:
    """Convierte bins tipo '5,000-10,000' o '50,001+' a un valor aproximado mensual."""
    if not isinstance(rango, str):
        return 12000.0
    s = rango.strip().replace(" ", "")
    if not s:
        return 12000.0
    try:
        if "+" in s:
            lo = float(s.replace("+", "").replace(",", ""))
            return lo * 1.25
        if "-" in s:
            lo, hi = s.split("-")
            lo_v = float(lo.replace(",", ""))
            hi_v = float(hi.replace(",", ""))
            return (lo_v + hi_v) / 2.0
        return float(s.replace(",", ""))
    except Exception:
        return 12000.0

# Carga de datos
def load_raw() -> Tuple[pd.DataFrame, pd.DataFrame]:
    clientes_fp = RAW_DIR / "clientes.json"
    creditos_fp = RAW_DIR / "creditos.json"
    if not clientes_fp.exists() or not creditos_fp.exists():
        raise FileNotFoundError("No encontré clientes.json o creditos.json en datos/raw/")
    df_cli = pd.read_json(clientes_fp)
    df_cre = pd.read_json(creditos_fp)
    return df_cli, df_cre

def load_config() -> Dict[str, Any]:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Features
def engineer_features(df: pd.DataFrame, cfg: Dict[str, Any]) -> pd.DataFrame:
    # Fechas -> edad
    for col in ["fecha_nacimiento", "fecha_desembolso"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Edad al desembolso
    if {"fecha_nacimiento", "fecha_desembolso"}.issubset(df.columns):
        edad_years = (df["fecha_desembolso"] - df["fecha_nacimiento"]).dt.days // 365
        df["edad"] = edad_years.fillna(35).clip(lower=18, upper=85)
    else:
        df["edad"] = 35

    # Ingresos aproximados desde el bin
    if "rango_ingresos_mensuales" in df.columns:
        df["ingreso_aprox"] = df["rango_ingresos_mensuales"].map(parse_income_bin).fillna(12000.0)
    else:
        df["ingreso_aprox"] = 12000.0

    # Cuota estimada
    df["cuota_mensual"] = df.apply(
        lambda r: amortization_payment(
            r.get("monto_otorgado", 0.0),
            r.get("tasa_interes", 0.0),
            int(r.get("plazo", 0)) if pd.notna(r.get("plazo", None)) else 0,
        ),
        axis=1,
    )

    # Ratios de endeudamiento
    denom = (df["ingreso_aprox"].abs() + 1e-6)
    df["dti_total"] = (df.get("deuda_total", 0.0) / denom).fillna(0.0)
    df["dti_credito"] = (df.get("deuda_credito", 0.0) / denom).fillna(0.0)
    df["cuota_dti"] = (df["cuota_mensual"] / denom).fillna(0.0)

    # Normalización a [0,1] 
    df["dti_total_n"] = (df["dti_total"].clip(0, 3.0) / 3.0)
    df["dti_credito_n"] = (df["dti_credito"].clip(0, 3.0) / 3.0)
    df["cuota_dti_n"] = (df["cuota_dti"].clip(0, 1.5) / 1.5)
    df["edad_n"] = ((df["edad"] - 18) / (85 - 18)).clip(0, 1)

    # Dependientes y productos 
    if "numero_dependientes" in df.columns:
        dep_max = cfg.get("numero_dependientes_max", 10)
        df["dependientes_n"] = (df["numero_dependientes"].fillna(0) / max(dep_max, 1)).clip(0, 1)
    else:
        df["dependientes_n"] = 0.0

    if "num_productos_financieros" in df.columns:
        max_prod = cfg.get("num_productos_financieros_max", cfg.get("max_productos_financieros", 8))
        df["productos_n"] = ((df["num_productos_financieros"].fillna(1) - 1) / max(max_prod - 1, 1)).clip(0, 1)
    else:
        df["productos_n"] = 0.0

    # --- Convertir fecha_inicio_negocio a años de negocio (numérico) ---
    if "fecha_inicio_negocio" in df.columns:
        # convierte strings tipo 'YYYY-MM-DD' a datetime; valores no parseables -> NaT
        df["fecha_inicio_negocio"] = pd.to_datetime(df["fecha_inicio_negocio"], errors="coerce", format="%Y-%m-%d")

        # referencia: usar fecha_desembolso si está, si no usar fecha actual
        if "fecha_desembolso" in df.columns:
            ref_dates = df["fecha_desembolso"]
        else:
            ref_dates = pd.to_datetime("today")

        # calcular años de negocio (si fecha_inicio_negocio is NaT -> fill 0)
        years = ((ref_dates - df["fecha_inicio_negocio"]).dt.days / 365.0)
        df["years_in_business"] = years.fillna(0).clip(lower=0)

        # normalizar para tener versión en [0,1]
        max_y = df["years_in_business"].replace(0, np.nan).max()
        max_y = max_y if (pd.notna(max_y) and max_y > 0) else 1.0
        df["years_in_business_n"] = (df["years_in_business"] / max_y).clip(0, 1)
    else:
        df["years_in_business"] = 0.0
        df["years_in_business_n"] = 0.0
    # ------------------------------------------------------------------

    return df

# Categóricas
def encode_categoricals(df: pd.DataFrame, cfg: Dict[str, Any]) -> pd.DataFrame:
    
    cat_cols: List[str] = [
        c for c in [
            "municipio_residencia",
            "tipo_credito",
            "tipo_negocio",
            "nivel_educativo",
            "estado_civil",
            "genero",
        ]
        if c in df.columns
    ]
    if not cat_cols:
        return df

   
    dummies = pd.get_dummies(df[cat_cols], prefix=cat_cols, drop_first=False, dtype="int8")
    df = pd.concat([df.drop(columns=cat_cols), dummies], axis=1)
    return df

# Pipeline
def build_dataset() -> Tuple[pd.DataFrame, pd.Series]:
    cfg = load_config()
    df_cli, df_cre = load_raw()

    # join
    key = "id_cliente"
    if key not in df_cli.columns or key not in df_cre.columns:
        raise KeyError(f"'{key}' debe existir en clientes y créditos para hacer el join.")
    df = df_cre.merge(df_cli, on=key, how="left", suffixes=("", "_cli"))

    # ingeniería
    df = engineer_features(df, cfg)


    # quitar columnas que no se usaran en el modelo
    drop_cols = [c for c in [
        "fecha_nacimiento", "fecha_desembolso", "rango_ingresos_mensuales",
        "monto_otorgado", "tasa_interes", "plazo", "fecha_inicio_negocio"  # las capturamos en features
    ] if c in df.columns]
    df_model = df.drop(columns=drop_cols)

    # codificar categóricas
    df_model = encode_categoricals(df_model, cfg)

    # separar X, y
    target_col = "incumplimiento"
    if target_col not in df_model.columns:
        raise KeyError("No se encontró la columna objetivo 'incumplimiento'.")
    y = df_model[target_col].astype(int)
    X = df_model.drop(columns=[target_col])

    # llenar NaNs
    X = X.fillna(0)

    return X, y

def save_outputs(X: pd.DataFrame, y: pd.Series) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # dataset completo
    df_all = X.copy()
    df_all["incumplimiento"] = y.values
    df_all.to_csv(OUT_DIR / "dataset_procesado.csv", index=False)

    # split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y if y.nunique() == 2 else None
    )
    X_train.to_csv(OUT_DIR / "X_train.csv", index=False)
    X_test.to_csv(OUT_DIR / "X_test.csv", index=False)
    y_train.to_csv(OUT_DIR / "y_train.csv", index=False)
    y_test.to_csv(OUT_DIR / "y_test.csv", index=False)

def main():
    X, y = build_dataset()
    save_outputs(X, y)
    print(f"[OK] Guardado en {OUT_DIR}/: dataset_procesado.csv, X_train.csv, X_test.csv, y_train.csv, y_test.csv")
    print(f"Shape X: {X.shape} | y positivos: {int(y.sum())}/{len(y)}")

if __name__ == "__main__":
    main()
