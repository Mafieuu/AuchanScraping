# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 09:50:24 2024

@author: DELL
"""

from typing import List
from datetime import date
import pymysql
import pandas as pd

def load_data_time():
    try:
        # Connexion à la base de données
        conn = pymysql.connect(
            host="db-auchan.c5esoc4g6qck.eu-west-3.rds.amazonaws.com",
            user="admin",
            password="MNdione2024",
            database="bdccAuchan"
        )

        cursor = conn.cursor()
        
          # Exécuter une requête pour récupérer les dates
        query = """
                SELECT dateCollecte FROM suivi     
                """
        cursor.execute(query)
            
            # Ajouter les résultats au tableau global
        result = cursor.fetchall()
        
        # Fermer la connexion
        conn.close()
        
        # Récupère les noms des colonnes de la table pour le DataFrame
        colonne = ['scraping_date']  

        # Conversion des résultats en DataFrame
        data = pd.DataFrame(result,columns=colonne)
        data.drop_duplicates(inplace=True)
        return data
    
    except pymysql.MySQLError as e:
        print("Erreur lors de la connexion à la base de données :", e)
