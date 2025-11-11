# Proyecto Final MLOps

Descripción corta
---------------

Breve resumen del proyecto: objetivo principal, problema que resuelve y por qué es importante. Una o dos frases que definan claramente el propósito del trabajo.

Autores
-------

- Juan Miguel González-Campo 21077.
- Sebastián Franco 21
- Diana Díaz
- Sebastián Reyes
- Carlos Aldana




Tabla de contenidos
-------------------

- [Proyecto Final MLOps](#proyecto-final-mlops)
  - [Descripción corta](#descripción-corta)
  - [Autores](#autores)
  - [Tabla de contenidos](#tabla-de-contenidos)
  - [Objetivos](#objetivos)
  - [Datos](#datos)
  - [Preprocesamiento](#preprocesamiento)
  - [Modelos y entrenamiento](#modelos-y-entrenamiento)
  - [Evaluación](#evaluación)
  - [Cómo ejecutar](#cómo-ejecutar)
  - [Referencias](#referencias)

Objetivos
---------

- Objetivo general del proyecto.
- Objetivos específicos (ej.: preparar datos, entrenar modelo X, implementar pipeline CI/CD, desplegar en Kubernetes, montar monitorización, etc.).

Datos
-----

- Fuente: describir el/los dataset(s) usados (origen, licencia, tamaño aproximado).
- Formato: columnas, variables objetivo y predictoras principales.
- Acceso: instrucciones para descargar o enlaces si aplicable. Si los datos son privados, indicar cómo obtenerlos o generar datos de ejemplo.

Preprocesamiento
-----------------

Describe pasos principales realizados sobre los datos:

- Limpieza (valores faltantes, duplicates).
- Transformaciones (normalización, codificación, generación de features).
- Split (train/val/test) y estrategia (temporal, estratificado, k-fold...).
- Herramientas/ scripts: indicar scripts o notebooks usados (ruta).

Modelos y entrenamiento
------------------------

- Modelos considerados: lista (ej.: XGBoost, RandomForest, NN con PyTorch/TensorFlow).
- Métricas de entrenamiento y validación.
- Hyperparameter tuning: método (GridSearch, Optuna, etc.) y rango de búsqueda.
- Checkpoints: dónde se guardan los modelos entrenados.

Evaluación
----------

- Métricas finales usadas para comparar modelos (ej.: accuracy, F1, ROC-AUC, RMSE).
- Procedimiento de evaluación (conjuntos de prueba, validación cruzada).
- Resultados clave (resumen numérico y tablas/figuras si aplican).

Cómo ejecutar
-------------

1) Requisitos:

	- Python >= 3.8
	- Docker (opcional para despliegue)
	- kubectl / minikube (si se usa k8s)

2) Instalación local (entorno virtual):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3) Preparar datos:

```bash
python src/data/download_data.py   # o script equivalente
python src/data/preprocess.py
```

4) Entrenamiento:

```bash
python src/train.py --config configs/train.yaml
```

5) Evaluación:

```bash
python src/evaluate.py --model outputs/models/best_model.pkl
```


Referencias
----------

- Lista de artículos, datasets y herramientas citadas en el proyecto.




