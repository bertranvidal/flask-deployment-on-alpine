

URL="https://drive.google.com/uc?export=download&id=1PHWBGuwDHw4ZEIlCbgMTiEUrG8FmlJK2"

PATH_MAIN_PYTHON="ProyectoFuso/generate_maps.py"
PATH_MAIN_PYTHON_INDIVIDUAL="ProyectoFuso/generate_individual_maps.py"
PATH_GOWALLA_FILES="DatasetsGowalla/"
PATH_OUTPUT_GOWALLA_FILES="ProyectoFuso/templates/html_files/"
ARCHIVO_ZIP="DatasetsGowalla.zip"
PATH_PYTHON_TOPN="ProyectoFuso/topn_selection_javierbertran.py"


#wget --no-check-certificate "$URL" -O "$ARCHIVO_ZIP"



#unzip "$ARCHIVO_ZIP"

mkdir -p filtered_files

source entorno_virtual/bin/activate

for fichero in "$PATH_GOWALLA_FILES"*; do

	# Obtener el nombre base del archivo (sin la extension)
	ciudad=$(basename "$fichero" Gowalla.txt)

	# Extraer columnas 3, 4 y 5 y anadir al archivo ALL_LOCATIONS.txt
   	cut -f3-5 "$fichero" >> ALL_LOCATIONS.txt

	# Extraer columnas 1, 2 y 5 y redirigir al archivo filtrado de la ciudad
	cut -f1-2,5 "$fichero" > "filtered_files/${ciudad}_filtered.txt"




	# estad�sticas
	echo "Estad�sticas para ${ciudad}.txt:"

	# usuarios distintos
	num_usuarios=$(cut -f1 "$fichero" | sort | uniq | wc -l)
	echo "N�mero de usuarios distintos: $num_usuarios"

	# lugares distintos
 	num_lugares=$(cut -f5 "$fichero" | sort | uniq | wc -l)
 	echo "N�mero de lugares distintos: $num_lugares"

 	# N�mero total de filas
   	num_filas=$(wc -l < "$fichero")
   	echo "N�mero de filas completas: $num_filas"

   	# interacciones en 2010-07
   	interacciones_2010_07=$(grep "2010-07" "$fichero" | wc -l)
   	echo "N�mero de check-ins en 2010-07: $interacciones_2010_07"

	# interacciones en 2010-08
   	interacciones_2010_08=$(grep "2010-08" "$fichero" | wc -l)
   	echo "N�mero de check-ins en 2010-08: $interacciones_2010_08"

	



	
	# Generar el mapa general solo para las ciudades espec�ficas
    	if [[ "$ciudad" == "ElPaso" || "$ciudad" == "Glasgow" || "$ciudad" == "Manchester" || "$ciudad" == "WashingtonDC" ]]; then
		
        	
        	python3 "$PATH_MAIN_PYTHON" --input_file "$fichero" --city_name "$ciudad" --output_html "$PATH_OUTPUT_GOWALLA_FILES${ciudad}GowallaMap"

		# Asignar el user_id seg�n la ciudad
    		if [ "$ciudad" == "ElPaso" ]; then
       			user_id=667
    		elif [ "$ciudad" == "WashingtonDC" ]; then
       			user_id=22
   		elif [ "$ciudad" == "Glasgow" ]; then
      			user_id=268
    		elif [ "$ciudad" == "Manchester" ]; then
        		user_id=332
    		fi
		python3 "$PATH_MAIN_PYTHON_INDIVIDUAL" --user_id "$user_id" --city_name "$ciudad" --input_file "$fichero" --output_html "$PATH_OUTPUT_GOWALLA_FILES${ciudad}_${user_id}_IndividualMap.html"

        	
    	fi  


done

input_file="filtered_files/ElPaso_filtered.txt"
output_file="filtered_files/ElPaso_top5.txt"

# Generar el archivo con los 5 usuarios m�s activos
python3 "$PATH_PYTHON_TOPN" --input_file "$input_file" --top 5 --output_file "$output_file"



ciudad="ElPaso"
PATH_ELPASO="DatasetsGowalla/ElPasoGowalla.txt"
output_file="filtered_files/${ciudad}_top5.txt"



# Leer el archivo y generar los mapas individuales para cada usuario
while read -r user_id; do
    
    echo "Generando mapa para el usuario ID: $user_id en la ciudad $ciudad"
    output_html="ProyectoFuso/templates/html_files/${ciudad}_${user_id}_topn_selection_Map.html"
    
    # Llamar al script para generar el mapa individual
    python3 "$PATH_MAIN_PYTHON_INDIVIDUAL" --user_id "$user_id" --city_name "$ciudad" --input_file "$PATH_ELPASO" --output_html "$output_html"
done < "$output_file"


deactivate
