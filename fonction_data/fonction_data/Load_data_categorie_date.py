from typing import List
from datetime import date
import pymysql
import pandas as pd

def load_data_cat_date(_id_categorie: int, liste_id_subcategorie: List[int], date_select: str):
    try:
        # Connexion à la base de données
        conn = pymysql.connect(
            host="db-auchan.c5esoc4g6qck.eu-west-3.rds.amazonaws.com",
            user="admin",
            password="MNdione2024",
            database="bdccAuchan"
        )

        cursor = conn.cursor()
        
        # Initialiser une liste pour stocker tous les résultats
        all_results = []

        # Parcourir chaque ID de sous-catégorie dans la liste
        for subcat_id in liste_id_subcategorie:
            # Exécuter une requête pour récupérer les informations de produits  pour une catégorie et liste
            #de sous catégorie et date donnée
            query = """
                SELECT p.nomProduit,p.idSubCategorie, p.idCategorie, p.imageURL, s.*
                FROM produit p
                JOIN suivi s ON p.idProduit = s.idProduit
                WHERE p.idCategorie = %s 
                AND p.idSubCategorie = %s 
                AND s.dateCollecte = %s;
            """
            cursor.execute(query, (_id_categorie, subcat_id, date_select))
            
            # Ajouter les résultats au tableau global
            all_results.extend(cursor.fetchall())

        
        # Fermer la connexion
        conn.close()
        
        # Récupère les noms des colonnes de la table pour le DataFrame
        
        colonne = ['product_id','subcategory_id','category_id',
                   'title','image_url','scraping_date','price',
                   'old_price','is_out_of_stock']

        # Conversion des résultats en DataFrame
        df_results = pd.DataFrame(all_results, columns=colonne)
        return df_results
    
    except pymysql.MySQLError as e:
        print("Erreur lors de la connexion à la base de données :", e)
