#!/bin/sh

#Modificar repositories para instalar sudo

sed -i '3s/^#//' /etc/apk/repositories

#paquetes

paquetes="python3 python3-dev git nano sudo bash gcc g++ musl-dev linux-headers wget curl htop"


#Comprobar si los paquetes estan instalados

for paquete in $paquetes; do
	if ! apk list --installed | grep -q "$paquete"; then
		echo "Instalando $paquete"
		apk add "$paquete"
	else
		echo "$paquete ya instalado"
	fi
done

#Instalar libc-dev sin comprobar si ya existe

echo "Instalando libc-dev sin comprobacion"
apk add libc-dev

