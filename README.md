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

- Crédito:
  - Monto Otorgado: Decimal
  Monto otorgado en el crédito (capital).
  - Deuda Crédito
  Monto debido total del crédito (capital + intereses).
  - Fecha Desembolso: Fecha
  Fecha en que se entrego el dinero al cliente.
  - Plazo: Entero
  Número de meses del crédito.
  - Tasa de interés: Decimal
  Porcentaje de intereses en decimal.
  - Tipo Crédito: Categórica
  Tipo del crédito otorgado, clasificado en base al destino de los fondos (nuevo negocio, remodelación, adquisición o abasto).
  - ID Cliente: Categórica
  Identificador de cliente.
  - **Incumplimiento**: Booleana
  *Variable objetivo*, indica si el crédito ha estado en incumplimiento.
- Cliente:
  - ID Cliente: Categórica
  Identificador del cleinte.
  - Ingresos Mensuales: Categórica (e.g. 10,000-20,000)
  Rango de ingresos mensuales del cliente.
  - Tipo Negocio: Categórica
  Tipo de negocio que el cliente tiene (Tienda de Ropa, Venta Comida, etc.).
  - Fecha Nacimiento: Fecha
  Fecha de nacimiento del cliente
  - Municipio Residencia: Categórica
  Municipio de guatemala en el que recide.
  - Número de Productos Financieros: Entero
  Número de productos financieros activos del cliente (tarjetas, cuentas, créditos)
  - Deuda Total: Decimal
  Endeudamiento total del cleinte (este crédito + otros créditos + tarjetas)
  - Fecha Inicio Negocio: Fecha
  Fecha en la que comenzó a operar el negocio (Nula si el negocio es nuevo)
  - Nivel Educativo: Categórica
  Nivel educativo más alto alcanzado del cliente.
  - Estado Civil: Categórica
  Soltero/Casado.
  - Numero Dependientes: Entero
  Número de dependientes del cliente.
  - Genero: Categórica
  Genero del cliente
  



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




