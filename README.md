Proyecto FUSO – Despliegue y Automatización en Alpine Linux

Este proyecto desarrolla el despliegue automatizado de una aplicación Flask sobre Alpine Linux, incluyendo la instalación de dependencias, ejecución de servicios y despliegue final en la nube (Google Cloud VM).
Incluye scripts Bash y Python para la instalación, el tratamiento de datos, el análisis de rendimiento y el despliegue completo de la aplicación.

🧠 Autores

Bertrán Vidal Campos

Javier Mendoza Guerrero

⚙️ Estructura
├── javierbertran.sh                    # Instalación de paquetes en Alpine
├── apartado_despliegue_Bash_javierbertran.sh  # Clonado, entorno virtual y ejecución Flask
├── apartado3.sh                         # Descarga y procesamiento de datos Gowalla + mapas
├── topn_selection_javierbertran.py      # Selección de usuarios más activos
├── train_request.py                     # Peticiones automáticas al servidor Flask
├── model.py                             # Modelos ML, EDA y comparación de rendimiento
├── requirements.txt                     # Dependencias locales
├── requirements_google.txt              # Dependencias para Google Cloud VM
├── Memoria Proyecto Final Fuso BUENA.pdf
└── Póster Proyecto Final.pdf

🚀 Ejecución Básica

Instalar dependencias del sistema:

sh javierbertran.sh


Clonar y desplegar la app Flask:

sh apartado_despliegue_Bash_javierbertran.sh


Procesar datos y generar mapas:

sh apartado3.sh


Entrenar modelos o realizar peticiones automáticas:

python3 train_request.py

🧩 Tecnologías

Bash · Python · Flask · Pandas · scikit-learn · Matplotlib · Seaborn · Folium · Alpine Linux · Google Cloud VM

📄 Licencia

MIT License