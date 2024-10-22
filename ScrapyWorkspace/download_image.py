import json
import os
import requests
from concurrent.futures import ThreadPoolExecutor

# Charger les données du fichier JSON avec l'encodage UTF-8
with open('data_base_final.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Créer un dossier pour stocker les images 
os.makedirs('images', exist_ok=True)

# Fonction pour télécharger une image
def download_image(product):
    image_url = product.get('image_url')
    product_id = product.get('product_id')

    if image_url and product_id:
        try:
            response = requests.get(image_url, timeout=10)
            if response.status_code == 200:
                # Déterminer l'extension de l'image à partir de l'URL
                extension = image_url.split('.')[-1]
                image_path = os.path.join('images', f'{product_id}.{extension}')
                
               
                with open(image_path, 'wb') as img_file:
                    img_file.write(response.content)
                print(f"Image téléchargée et sauvegardée sous {image_path}")
            else:
                print(f"Échec du téléchargement pour {product_id}: statut {response.status_code}")
        except Exception as e:
            pass # ce qui ne marche pas on le charge depuis le site de Auchan
# Utiliser un ThreadPoolExecutor pour paralléliser le téléchargement
with ThreadPoolExecutor(max_workers=80) as executor:
    executor.map(download_image, data)
