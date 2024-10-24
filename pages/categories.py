
import streamlit as st
import pandas as pd
import plotly.express as px
import json
import numpy as np
import hashlib


# Charger les données JSON avec mise en cache pour améliorer les performances
@st.cache_data
def load_data():
    with open("out_of_stck.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    
    # Nettoyer les prix et gérer les erreurs de format
    df["price"] = df["price"].str.replace("\u202f", "").str.replace("\xa0CFA", "")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")  # Convertir en numérique, NaN pour erreurs
    
    # Remplacer les valeurs NaN dans is_out_of_stock par False si manquantes
    df["is_out_of_stock"] = df["is_out_of_stock"].fillna(False)
    
    # Optimiser les colonnes catégorielles
    df["category"] = pd.Categorical(df["category"])
    df["subcategory"] = pd.Categorical(df["subcategory"])
    
    return df

# Charger les données
df = load_data()

st.markdown(
    """
    <style>
        .title {
            font-size: 40px;
            color: blue;
            text-align: center;
            margin-bottom: 20px;
            bold: True;
        }
        .subtitle {
            font-size: 30px;
            color: #333;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .product-card {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .dataframe {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)



st.markdown(
    "<div class='title'>Catégories de Produits</div>", unsafe_allow_html=True
)
st.sidebar.markdown("# Categories")

# Tableau des catégories
st.markdown(
    "<div class='subtitle'>Liste des Catégories</div>", unsafe_allow_html=True
)
st.dataframe(df[["category_id", "category"]].drop_duplicates(), height=300)

# Diagramme circulaire de la répartition des produits dans chaque catégorie
st.markdown(
    "<div class='subtitle'>Répartition des Produits par Catégorie</div>",
    unsafe_allow_html=True,
)
fig = px.pie(
    df, names="category", title="Répartition des produits dans les catégories"
)
fig.update_layout(title_font_size=24, legend_font_size=16)
st.plotly_chart(fig, use_container_width=True)
