import json
import os
import random
from datetime import datetime, timedelta

# Cargamos la configuracion
with open("gen_config.json", "r") as f:
    config = json.load(f)

output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), config["output_data_dir"]))

# Asegura que el directorio de salida exista
os.makedirs(output_dir, exist_ok=True)

# Numero de registros a generar

num_records = config["num_records"]

# Rangos de generación

monto_otorgado_range = {
    "min": config["monto_otorgado_min"],
    "max": config["monto_otorgado_max"]
}
plazo_meses_options = config["plazo_meses_options"]
tasa_interes_options = config["tasa_interes_options"]
fecha_desembolso_range = {
    "start": config["fecha_desembolso_start"],
    "end": config["fecha_desembolso_end"]
}
tipos_credito = config["tipos_credito"]
ingresos_mensuales_options = config["ingresos_mensuales_options"]
tipos_negocio = config["tipos_negocio"]
fecha_nacimiento_range = {
    "start": config["fecha_nacimiento_start"],
    "end": config["fecha_nacimiento_end"]
}
municipios_options = config["municipios_options"]
num_productos_financieros_range = {
    "min": config["num_productos_financieros_min"],
    "max": config["num_productos_financieros_max"]
}
fecha_inicio_negocio_range = {
    "start": config["fecha_inicio_negocio_start"],
    "end": config["fecha_inicio_negocio_end"]
}
nivel_educativo_options = config["nivel_educativo_options"]
generos_options = config["generos_options"]
numero_dependientes_range = {
    "min": config["numero_dependientes_min"],
    "max": config["numero_dependientes_max"]
}
generos_options = config["generos_options"]


def validate_payment(monto_otorgado, plazo_meses, tasa_interes, rango_ingresos):
    tasa_mensual = tasa_interes / 12 
    cuota_mensual = (monto_otorgado * tasa_mensual) / (1 - (1 + tasa_mensual) ** -plazo_meses)
    # Validar que la cuota mensual no exceda los ingresos mensuales
    if rango_ingresos == "50,001+":
        return True
    else:
        #print("Rango ingresos:", rango_ingresos)
        ingresos_valor = int(rango_ingresos.split("-")[1].replace(",", ""))
        if cuota_mensual > ingresos_valor:
            return False
        else:
            return True


def generar_record(last_id):
    valid = False
    id_cliente = last_id + 1
    rango_ingresos = random.choice(ingresos_mensuales_options)
    while not valid:
        monto_otorgado = float(random.randint(monto_otorgado_range["min"]*100, monto_otorgado_range["max"]*100) / 100.0)
        plazo_meses = random.choice(plazo_meses_options)
        tasa_interes = random.choice(tasa_interes_options)
        valid = validate_payment(monto_otorgado, plazo_meses, tasa_interes, rango_ingresos)
    # Fecha de desembolso
    start_date = datetime.strptime(fecha_desembolso_range["start"], "%Y-%m-%d")
    end_date = datetime.strptime(fecha_desembolso_range["end"], "%Y-%m-%d")
    delta_days = (end_date - start_date).days
    fecha_desembolso = start_date + timedelta(days=random.randint(0, delta_days))
    fecha_desembolso_str = fecha_desembolso.strftime("%Y-%m-%d")
    # Fecha de nacimiento
    start_date_nac = datetime.strptime(fecha_nacimiento_range["start"], "%Y-%m-%d")
    end_date_nac = datetime.strptime(fecha_nacimiento_range["end"], "%Y-%m-%d")
    delta_days_nac = (end_date_nac - start_date_nac).days
    fecha_nacimiento = start_date_nac + timedelta(days=random.randint(0, delta_days_nac))
    fecha_nacimiento_str = fecha_nacimiento.strftime("%Y-%m-%d")
    tipo_credito = random.choice(tipos_credito)
    tipo_negocio = random.choice(tipos_negocio)
    municipio = random.choice(municipios_options)
    num_productos_financieros = random.randint(num_productos_financieros_range["min"], num_productos_financieros_range["max"])
    # Fecha de inicio del negocio
    if tipo_credito == "Nuevo Negocio": 
        fecha_inicio_negocio = None
    else:
        start_date_neg = datetime.strptime(fecha_inicio_negocio_range["start"], "%Y-%m-%d")
        end_date_neg = datetime.strptime(fecha_inicio_negocio_range["end"], "%Y-%m-%d")
        delta_days_neg = (end_date_neg - start_date_neg).days
        fecha_inicio_negocio_dt = start_date_neg + timedelta(days=random.randint(0, delta_days_neg))
        fecha_inicio_negocio = fecha_inicio_negocio_dt.strftime("%Y-%m-%d")
    nivel_educativo = random.choice(nivel_educativo_options)
    estado_civil = random.choice(["Soltero", "Casado", "Divorciado", "Viudo"])
    genero = random.choice(generos_options)
    numero_dependientes = random.randint(numero_dependientes_range["min"], numero_dependientes_range["max"])

    deuda_credito = monto_otorgado * (1 + tasa_interes * (plazo_meses / 12))  
    if num_productos_financieros == 1:
        deuda_total = deuda_credito
    else:
        deuda_total = deuda_credito * random.uniform(1.0, 3.0)


    record_credito = {
        "id_cliente": id_cliente,
        "monto_otorgado": monto_otorgado,
        "plazo": plazo_meses,
        "tasa_interes": tasa_interes,
        "fecha_desembolso": fecha_desembolso_str,
        "tipo_credito": tipo_credito,
        "deuda_credito": round(deuda_credito, 2)
        
    }
    record_cliente = {
        "id_cliente": id_cliente,
        "fecha_nacimiento": fecha_nacimiento_str,
        "nivel_educativo": nivel_educativo,
        "estado_civil": estado_civil,
        "genero": genero,
        "numero_dependientes": numero_dependientes,
        "deuda_total": round(deuda_total, 2),
        "fecha_inicio_negocio": fecha_inicio_negocio,
        "rango_ingresos_mensuales": rango_ingresos,
        "tipo_negocio": tipo_negocio,
        "municipio_residencia": municipio,
        "num_productos_financieros": num_productos_financieros,
        "numero_dependientes": numero_dependientes
    }
    return record_credito, record_cliente

def decidir_incumplimiento(credito, cliente):
 
    def _get_config(key, fallback_key=None, default=None):
        if key in config:
            return config[key]
        if fallback_key and fallback_key in config:
            return config[fallback_key]
        return default

    def _parse_income(rango: str) -> float:
        """
        Convierte un bin de ingresos tipo '5,000-10,000' o '50,001+' en un valor numérico aproximado (mensual).
        Método: usa el punto medio; para '+' toma el límite inferior + 25%.
        """
        rango = (rango or "").strip()
        if not rango:
            return 12000.0  
        rango = rango.replace(" ", "")
        if "+" in rango:
            low = rango.replace("+", "").replace(",", "")
            try:
                low_v = float(low)
            except:
                low_v = 12000.0
            return low_v * 1.25 
        if "-" in rango:
            lo, hi = rango.split("-")
            try:
                lo_v = float(lo.replace(",", ""))
                hi_v = float(hi.replace(",", ""))
                return (lo_v + hi_v) / 2.0
            except:
                return 12000.0
        try:
            return float(rango.replace(",", ""))
        except:
            return 12000.0

    def _amortization_payment(monto, tasa_anual, meses):
        """Cuota mensual de un préstamo amortizable clásico."""
        tasa_mensual = float(tasa_anual) / 12.0
        if meses <= 0:
            return 0.0
        if tasa_mensual == 0:
            return monto / meses
        return (monto * tasa_mensual) / (1 - (1 + tasa_mensual) ** (-meses))

    def _enforzar_rango_prob(x, a=0.0, b=1.0):
        return max(a, min(b, x))

    def _norm_cap(x, cap=3.0):
        """Normaliza un ratio positivo capándolo a 'cap' y llevándolo a [0,1]."""
        if x < 0:
            return 0.0
        return _enforzar_rango_prob(x / cap)

    # Ingresos
    ingresos_bins = _get_config("ingresos_mensuales_options", "ingresos_mensuales_bins", [])
    rango_ingresos = cliente.get("rango_ingresos_mensuales")
    ingreso_mensual_aprox = _parse_income(rango_ingresos)

    # Endeudamiento
    deuda_total = max(float(cliente.get("deuda_total", 0.0)), 0.0)
    deuda_credito = max(float(credito.get("deuda_credito", 0.0)), 0.0)
    monto = float(credito.get("monto_otorgado", 0.0))
    tasa = float(credito.get("tasa_interes", 0.0))
    plazo = int(credito.get("plazo", 0))

    cuota = _amortization_payment(monto, tasa, plazo)

    denom = max(ingreso_mensual_aprox, 1.0)

    dti_total = deuda_total / denom
    dti_credit = deuda_credito / denom
    cuota_dti = cuota / denom

    dti_total_n = _norm_cap(dti_total, cap=3.0)
    dti_credit_n = _norm_cap(dti_credit, cap=3.0)
    cuota_dti_n = _norm_cap(cuota_dti, cap=1.5) 

    def _parse_date(s):
        try:
            return datetime.strptime(s, "%Y-%m-%d")
        except:
            return None

    f_des = _parse_date(credito.get("fecha_desembolso"))
    f_nac = _parse_date(cliente.get("fecha_nacimiento"))
    edad = None
    if f_des and f_nac:
        edad = max(0, (f_des - f_nac).days // 365)
    else:
        edad = 35 

    if edad < 25:
        riesgo_edad = 0.7
    elif edad <= 60:
        if edad <= 35:
            riesgo_edad = 0.45
        elif edad <= 45:
            riesgo_edad = 0.40
        else:
            riesgo_edad = 0.46
    else:
        riesgo_edad = 0.62


    municipios = _get_config("municipios_options", None, [])
    tipos_credito = _get_config("tipos_credito", None, [])
    tipos_negocio = _get_config("tipos_negocio", None, [])
    niveles = _get_config("nivel_educativo_options", None, [])
    estados = _get_config("estado_civil_options", None, ["Soltero", "Casado", "Divorciado", "Viudo"])

    # Pesos por categoría
    municipio_val = {
        "Ciudad de Guatemala": 0.45,
        "Mixco": 0.60,
        "Villa Nueva": 0.55,
        "Quetzaltenango": 0.50,
        "Escuintla": 0.65,
    }
    tipo_credito_val = {
        "Nuevo Negocio": 0.60,
        "Vehículo": 0.35,
        "Abasto": 0.45,
        "Adquisición de Equipo": 0.40,
    }
    tipo_negocio_val = {
        "Restaurante": 0.50,
        "Abarrotería": 0.45,
        "Manufactura": 0.40,
        "Tecnología": 0.35,
        "Salud": 0.30,
    }
    nivel_val = {
        "Primaria": 0.60,
        "Secundaria": 0.50,
        "Bachillerato": 0.45,
        "Universidad": 0.35,
        "Postgrado": 0.30,
    }
    estado_val = {
        "Soltero": 0.50,
        "Casado": 0.40,
        "Divorciado": 0.55,
        "Viudo": 0.50,
    }
    genero_val = {
        "M": 0.48,
        "F": 0.47,
        "O": 0.50,
    }

    # Lectura de categorías presentes en el registro
    municipio = cliente.get("municipio_residencia")
    tipo_cre = credito.get("tipo_credito")
    tipo_neg = cliente.get("tipo_negocio")
    nivel = cliente.get("nivel_educativo")
    estado = cliente.get("estado_civil")
    genero = cliente.get("genero")

    cat_muni = municipio_val.get(municipio, 0.50)
    cat_tcredito = tipo_credito_val.get(tipo_cre, 0.45)
    cat_tneg = tipo_negocio_val.get(tipo_neg, 0.45)
    cat_nivel = nivel_val.get(nivel, 0.45)
    cat_estado = estado_val.get(estado, 0.48)
    cat_genero = genero_val.get(genero, 0.49)

    # Productos y dependientes
    max_prod = _get_config("num_productos_financieros_max", "max_productos_financieros", 8)
    dep_max = _get_config("numero_dependientes_max", None, 10)

    n_prod = int(cliente.get("num_productos_financieros", 1))
    n_dep = int(cliente.get("numero_dependientes", 0))

    prod_n = _enforzar_rango_prob((n_prod - 1) / max(1, (max_prod - 1)))  
    dep_n = _enforzar_rango_prob(n_dep / max(1, dep_max))

    # Score
    w = {
        "dti_total": 0.30,
        "dti_credit": 0.20,
        "cuota_dti": 0.15,
        "municipio": 0.10,
        "tipo_credito": 0.05,
        "tipo_negocio": 0.05,
        "nivel": 0.05,
        "estado": 0.03,
        "genero": 0.02,
        "productos": 0.025,
        "dependientes": 0.025,
        "edad": 0.05,
    }

    score = (
        w["dti_total"]   * dti_total_n +
        w["dti_credit"]  * dti_credit_n +
        w["cuota_dti"]   * cuota_dti_n +
        w["municipio"]   * cat_muni +
        w["tipo_credito"]* cat_tcredito +
        w["tipo_negocio"]* cat_tneg +
        w["nivel"]       * cat_nivel +
        w["estado"]      * cat_estado +
        w["genero"]      * cat_genero +
        w["productos"]   * prod_n +
        w["dependientes"]* dep_n +
        w["edad"]        * _enforzar_rango_prob((riesgo_edad - 0.30) / 0.70)  
    )


    noise = random.uniform(-0.03, 0.03)
    score = _enforzar_rango_prob(score + noise)

  
    threshold = 0.50
    incumplimiento = 1 if score >= threshold else 0
    return incumplimiento


def generar_datos():
    creditos = []
    clientes = []
    last_id = 0
    for _ in range(num_records):
        record_credito, record_cliente = generar_record(last_id)
        incumplimiento = decidir_incumplimiento(record_credito, record_cliente)
        record_credito["incumplimiento"] = incumplimiento
        creditos.append(record_credito)
        clientes.append(record_cliente)
        last_id += 1
    # Guardar los datos generados en archivos JSON
    with open(os.path.join(output_dir, "creditos.json"), "w") as f:
        json.dump(creditos, f, indent=4)
    with open(os.path.join(output_dir, "clientes.json"), "w") as f:
        json.dump(clientes, f, indent=4)

if __name__ == "__main__":
    generar_datos()
