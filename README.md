# alegraApp

## Inicio
La app se encarga de tomar los registros que se encuentran en el archivo de excel, y enviar cada conjunto de facturas o remisiones a la api de alegra según el estado de envío en el que se encuentre cada registro.

## Instalación
Despues de clonar proyecto:

1. Descargar e instalar [python](https://www.python.org/downloads/) y añadirlo a variables de entorno.
2. Para instalación de librerías: Abrir un cmd en la ruta del proyecto y correr:
>pip install -r requirements.txt

3. Módulo de entrada para correr el proyecto: app/lanzamiento.py

## Descripción del proyecto
### Modulos
#### **app**
En este módulo se encuentra la lógica de negocio para el proyecto.
#### **conf**
Configuración de correo y token asociados a la cuenta de alegra en archivo **Configuracion.txt**
#### **Instalación**
Guía de instalación y lanzamiento de la app.
#### **notas**
Archivos de texto para configurar anotaciones, observaciones y términos y condiciones.
#### **Otros**
La ruta donde se debe encontrar el archivo de registros debe ser en la raíz del proyecto con el nombre **Registros.xlsx**

## Extras
**Brayan Montoya Osorio**

**bmontoyaosorios@gmail.com**

2022
