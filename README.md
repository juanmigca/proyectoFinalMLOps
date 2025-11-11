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

- Generación propia. Ver [Cómo ejecutar](#cómo-ejecutar) para información sobre generación.
  
Variables:

- TODO

Preprocesamiento
-----------------

El pipeline se conforma de la siguiente manera:

- Limpieza
TODO
- Transformaciones
TODO
- Split (train/val/test)
TODO

Modelos y entrenamiento
------------------------

- Modelos considerados: 
TODO
- Métricas de entrenamiento y validación:
TODO
- Hiperparámetros:
TODO
- Repositorio de modelos: 
MLFLOW/TODO

Evaluación
----------

- Métricas utilizadas: 
TODO
- Procedimiento de evaluación: 
TODO
- Resultados clave obtenidos: 
TODO

Cómo ejecutar
-------------

1) Requisitos:

- Python >= 3.13
- Ver **requirements.txt**

2) Instalación local (entorno virtual):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3) Preparar datos:

```bash
python src/data/generacion.py   
python src/data/preprocesamiento.py
```

4) Entrenamiento:

```bash
python src/train.py 
```

5) Evaluación:

```bash
python src/evaluate.py 
```

Referencias
----------

- Lista de artículos, datasets y herramientas citadas en el proyecto.




