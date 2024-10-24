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

st.markdown("<div class='title'> Statistiques</div>", unsafe_allow_html=True)
st.sidebar.markdown("# Page des statistiques")


# Moyenne des prix par catégorie
st.markdown(
    "<div class='subtitle'>Moyenne des prix par catégorie</div>",
    unsafe_allow_html=True,
)
avg_price = df.groupby("category")["price"].mean().reset_index()
st.dataframe(avg_price, height=300)

# Histogramme des prix
st.markdown(
    "<div class='subtitle'>Répartition des prix des produits</div>",
    unsafe_allow_html=True,
)
fig = px.histogram(df, x="price", nbins=20, title="Histogramme des prix")
fig.update_layout(title_font_size=24, legend_font_size=16)
st.plotly_chart(fig, use_container_width=True)

# Nuage de points (comparaison prix et catégorie)
st.markdown(
    "<div class='subtitle'>Nuage de points : Prix vs Catégorie</div>",
    unsafe_allow_html=True,
)
fig = px.scatter(
    df, x="category", y="price", color="category", title="Prix vs Catégorie"
)
fig.update_layout(title_font_size=24, legend_font_size=16)
st.plotly_chart(fig, use_container_width=True)
