from typing import List
from datetime import date
import pymysql
import pandas as pd

 # Le mot de passe se trouve dans le fichier .txt
        #

def load_data_product(nProduct: str):
    # Connexion à la base de données
    conn = pymysql.connect(
        host="db-auchan.c5esoc4g6qck.eu-west-3.rds.amazonaws.com",
        user="admin",
        password="MNdione2024",
        database="bdccAuchan"
    )

    cursor = conn.cursor()
    
    # Exécuter une requête pour récupérer les informations de produits correspondant à un ID produit donnée
    query = """
            SELECT c.*, sc.idSubCategorie, sc.nomSubCategorie,  p.nomProduit, p.imageURL, s.*
            FROM categorie c
            JOIN subcategorie sc ON c.idCategorie = sc.idCategorie
            JOIN produit p ON p.idSubcategorie = sc.idSubcategorie
            JOIN suivi s ON p.idProduit = s.idProduit
            WHERE p.nomProduit = %s;
            """
    cursor.execute(query, (nProduct))
    
    # Récupérer les résultats
    result = cursor.fetchall()
     
    # Récupère les noms des colonnes de la table pour le DataFrame
    colonne = ['category_id','category','subcategory_id','subcategory',
               'title','image_url','product_id','scraping_date','price',
               'old_price','is_out_of_stock']   
       
    # Fermer la connexion
    conn.close()
    # Convertir les résultats en DataFrame
    df = pd.DataFrame(result,columns=colonne)

    df['scraping_date'] = pd.to_datetime(df['scraping_date'])

    df['scraping_date'] = df['scraping_date'].dt.strftime("%Y-%m-%d")

    df['price'] = df["price"].str.replace("\u202f", "").str.replace("\xa0CFA", "")

    df.sort_values(by="scraping_date", ascending=True)
    
    return df
