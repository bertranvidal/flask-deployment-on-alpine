import requests

url = 'http://10.120.148.183:5000/train'

for train_size in [i/10 for i in range(1, 10)]:
    test_size = 1 - train_size
    data = {
    	'dataset': 'iris',
        'model': 'RandomForest',
        'train_size': train_size,
        'test_size': test_size
           }
    response = requests.post(url, data=data)

    if response.status_code == 200:
        print(f"Entrenamiento exitoso para iris y RandomForest con train_size={train_size} y test_size={test_size}.")
        # Suponiendo que la imagen generada es referenciada en la respuesta
        img_url = response.text  # Suponiendo que la URL de la imagen esta en la respuesta
        img_response = requests.get(f'http://10.120.148.183:5000/{img_url}')
        with open(f'iris_RandomForest_{train_size}_{test_size}.png', 'wb') as f:
            f.write(img_response.content)
    else:
        print("Error en la peticion:", response.status_code)

