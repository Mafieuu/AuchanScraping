import streamlit as st
from typing import List
from datetime import date
import pymysql
import pandas as pd
@st.cache_data
def load_data(date_select: str):
    try:
        # Connexion à la base de données
        conn = pymysql.connect(
            host="db-auchan.c5esoc4g6qck.eu-west-3.rds.amazonaws.com",
            user="admin",
            password="MNdione2024",
            database="bdccAuchan"
        )

        cursor = conn.cursor()
        
            # Exécuter une requête pour récupérer les informations de toutes les tables pour une date donnée
        query = """
                SELECT c.*, sc.idSubCategorie, sc.nomSubCategorie,  p.nomProduit, p.imageURL, s.*
                FROM categorie c
                JOIN subcategorie sc ON c.idCategorie = sc.idCategorie
                JOIN produit p ON p.idSubcategorie = sc.idSubcategorie
                JOIN suivi s ON p.idProduit = s.idProduit
                WHERE s.dateCollecte = %s;
            """
        cursor.execute(query, (date_select))
            
            # Ajouter les résultats au tableau global
        result = cursor.fetchall()
        
        # Fermer la connexion
        conn.close()
        
        # Récupère les noms des colonnes de la table pour le DataFrame
        colonne = ['category_id','category','subcategory_id','subcategory',
                   'title','image_url','product_id','scraping_date','price',
                   'old_price','is_out_of_stock']  

        # Conversion des résultats en DataFrame
        data = pd.DataFrame(result,columns=colonne)
        return data
    
    except pymysql.MySQLError as e:
        print("Erreur lors de la connexion à la base de données :", e)
