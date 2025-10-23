#!/bin/sh


git clone https://github.com/pablosanchezp/ProyectoFuso.git

python3 -m venv entorno_virtual

source entorno_virtual/bin/activate

pip install -r requirements.txt

python3 ProyectoFuso/main.py

