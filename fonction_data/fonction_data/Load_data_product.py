from typing import List
from datetime import date
import pymysql
import pandas as pd

def load_data_product(product: int):
    # Connexion à la base de données
    conn = pymysql.connect(
        host="db-auchan.c5esoc4g6qck.eu-west-3.rds.amazonaws.com",
        user="admin",
        password="MNdione2024",# Utilisation de DictCursor pour des résultats sous forme de dictionnaire
        database="bdccAuchan"
    )

    cursor = conn.cursor()
    
    # Exécuter une requête pour récupérer les informations de produits correspondant à un ID produit donnée
    query = """
    SELECT * FROM suivi
    WHERE idProduit = %s 
            """
    cursor.execute(query, (product))
    
    # Récupérer les résultats
    result = cursor.fetchall()
     
# Récupère les noms des colonnes de la table pour le DataFrame
    colonne = ['product_id','scraping_date','price','old_price','is_out_of_stock'] 
       
    # Fermer la connexion
    conn.close()
    # Convertir les résultats en DataFrame
    df = pd.DataFrame(result, columns=colonne)
    
    return df
