
import streamlit as st
import pandas as pd
import plotly.express as px
from my_pages.call_local_function import *
from my_pages import Load_data_2_json

def display():

#-------------------------------------------- Chargement des donnes
    if "df" not in st.session_state:
        st.session_state["df"]=Load_data_2_json.load_data(str(st.session_state["all_dates"][0]))
    else:
        st.session_state["df"]=Load_data_2_json.load_data(
            st.session_state["choix_date"]
        )

    st.session_state["df"]["price"] = st.session_state["df"]["price"].str.replace("\u202f", "").str.replace("\xa0CFA", "")
    st.session_state["df"]["price"] = pd.to_numeric(st.session_state["df"]["price"], errors="coerce")  # Convertir en numérique, NaN pour erreurs
        
    st.session_state["df"]["is_out_of_stock"] = st.session_state["df"]["is_out_of_stock"].fillna(False)
        
    st.session_state["df"]["category"] = pd.Categorical(st.session_state["df"]["category"])
    st.session_state["df"]["subcategory"] = pd.Categorical(st.session_state["df"]["subcategory"])
        


#-------------------------------------------- chargement du style css pour les graphiques
    with open('my_pages/css/style.css')as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#-------------------------------------------- Chargement du css pour les textes
    with open('my_pages/css/style.css')as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#-------------------------------------------- Texte perso du siderbar
    st.sidebar.markdown("""
        <div class="dashboard-header animate-fade-in">
            <h1 style = "text-align: center;font-weight: bold;">Page d'accueil</h1>
        </div>
    """, unsafe_allow_html=True)

#-------------------------------------------- Affichage des donnes clef:Total produit,...

    total_products = st.session_state["df"]["product_id"].nunique()
    total_categories = st.session_state["df"]["category_id"].nunique()
    total_subcategories = st.session_state["df"]["subcategory_id"].nunique()
    out_of_stock_products = st.session_state["df"][st.session_state["df"]["is_out_of_stock"] == True].shape[0]
    on_promotion = st.session_state["df"][st.session_state["df"]["old_price"] != "Not concerned"].shape[0]

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.info('Total de produits',icon="📌")
        display_custom_metric("Total de produits", total_products, "#0000FF")
    with col2:
        st.info('Catégories',icon="📌")
        display_custom_metric("Catégories", total_categories, "#228B22")
    with col3:
        st.info('Sous-catégories',icon="📌")
        display_custom_metric("Sous-catégories", total_subcategories, "#FF0000")
    with col4:
        st.info('En rupture de stock',icon="⚠️")
        display_custom_metric("En rupture de stock", out_of_stock_products, "#FE9900")
    with col5:
        st.info('En promotion',icon="💯")
        display_custom_metric("En promotio", on_promotion, "#582698")


    st.markdown("---")

#--------------------------------------------Affichage du produit le plus cher et le moins 
    max_price_product = st.session_state["df"].loc[st.session_state["df"]['price'].idxmax()]
    min_price_product = st.session_state["df"].loc[st.session_state["df"]['price'].idxmin()]
    col1, col2 = st.columns([2, 2])

#-------------------------------------------- redefinition perso de display_product_info()
    def display_product_info(product):
        product_name = product.get("title", "Nom non disponible")
        product_price = product.get("price", "Prix non disponible")
        product_image = product.get("image_url", "")
        product_status = "En rupture de stock" if product.get("is_out_of_stock") else "En stock"
        st.markdown(
            """
            <style>
            .product-card {
                border: 1px solid #d1d1d1;
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 16px;
                background-color: #f9f9f9;
                text-align: center;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.markdown(f"""
        <div class="product-card">
            <img src="{product_image}" alt="Image du produit" style="width:50%; height:auto; border-radius: 8px;">
            <h4>{product_name}</h4>
            <p style = "font-weight: bold;font-size: 24px;">Prix : {product_price} CFA</p>
            <p>Statut : {product_status}</p>
        </div>
        """, unsafe_allow_html=True)

    #

    with col1: 
        st.markdown("""
            <div class="dashboard-header animate-fade-in">
                <h3 style = "text-align: center;font-weight: bold;">Produit le plus cher</h3>
            </div>
        """, unsafe_allow_html=True)
        display_product_info(max_price_product)

    with col2: 
        st.markdown("""
            <div class="dashboard-header animate-fade-in">
                <h3 style = "text-align: center; font-weight: bold;">Produit le moins cher</h3>
            </div>
        """, unsafe_allow_html=True)
        display_product_info(min_price_product)

    st.markdown("---")
#--------------------------------------------Graphique de repartition par categorie

    col1, col2 = st.columns([2, 2])

    category_count = st.session_state["df"]["category"].value_counts()
    fig = px.pie(
        values=category_count,
        names=category_count.index,
        title="Répartition par catégorie",
    )
    fig.update_layout(title_font_size=24, legend_font_size=16)
    with col1: st.plotly_chart(fig, use_container_width=True)

#--------------------------------------------Affichage des produits en rupture de stock par categorie

    out_of_stock_data = st.session_state["df"][st.session_state["df"]["is_out_of_stock"] == True]

    if not out_of_stock_data.empty:
        fig2 = px.pie(
            out_of_stock_data,
            names="category",      
            title="Produits en rupture de stock par catégorie",
            hole=0.3               
        )
        
        fig2.update_traces(textinfo="label+value", textfont_size=10) 
        fig2.update_layout(title_font_size=24, legend_font_size=16)
        
        with col2: 
            st.plotly_chart(fig2, use_container_width=True)

    else:
        with col2: 
            st.info("Aucun produit en rupture de stock.")

    # Fin de la page d'acceuil
