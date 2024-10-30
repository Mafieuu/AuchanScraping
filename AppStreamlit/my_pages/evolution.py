import streamlit as st
import pandas as pd
import plotly.express as px
from my_pages.call_local_function import *
from my_pages import Load_data_2_json
from my_pages import Load_data_product2

def display():

#-------------------------------------------- Chargement des donnees
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
    st.markdown("""
    <style>
    /* Conteneurs personnalisés */
    [data-testid="metric-container"] {
        box-shadow: 0 0 4px #686664;
        padding: 10px;
    }

    .plot-container > div {
        box-shadow: 0 0 2px #070505;
        padding: 5px;
        border-color: #000000;
    }

    /* Expander */
    div[data-testid="stExpander"] div[role="button"] p {
        font-size: 1.2rem;
        color: rgb(0, 0, 0);
        border-color: #000000;
    }

    /* Barre latérale */
    .sidebar-content, [data-testid="stSidebar"] {
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

#-------------------------------------------- Texte perso du siderbar
    st.sidebar.markdown("""
        <div class="dashboard-header animate-fade-in">
            <h1 style = "text-align: center;font-weight: bold;">Page Evolution</h1>
        </div>
    """, unsafe_allow_html=True)

    #------------------------------------------------ Donnees de la date selectionnee


    df = st.session_state["df"]


    #------------------------------------------------

    
    #------------------------------------------------ Filtre des produits

    filter_page = st.sidebar.radio(
            "Choisir un type de filtre",
            ["Filtre par Catégorie", "Produits en promotion"]
        )
    
    if filter_page == "Filtre par Catégorie":
    
        category_options = ["Tous"] + df["category"].unique().tolist()
        st.sidebar.selectbox("Sélectionnez une catégorie", options=category_options, index=0, key="category_filter")
        
        
        if st.session_state["category_filter"] == "Tous":
            product_options = df["title"].unique().tolist()
        else:
            product_options =df[df["category"] == st.session_state["category_filter"]]["title"].unique().tolist()

        st.sidebar.selectbox("Sélectionnez un produit", options=product_options, index=0, key="product_filter")
        
        product_data = Load_data_product2.load_data_product(st.session_state["product_filter"])

        product_data["effective_price"] = product_data.apply(
            lambda row: row["old_price"] if row["old_price"] not in ["Not concerned", "True"] else row["price"],
            axis=1
        )

        product_data = product_data.sort_values(by="scraping_date", ascending=True)
        
        product_data["effective_price"] = product_data["effective_price"].str.replace("\u202f", "").str.replace("\xa0CFA", "").astype(int)

        product_filter = st.session_state["product_filter"]

        col1, col2, col3 = st.columns([1,1,2])
        with col1:
            display_product_info(product_data.loc[product_data.index[-1]])
        with col2:
            st.markdown(f"*Détails du produit : {product_filter}*")
            st.dataframe(product_data)
        
        with col3:
            fig = px.line(
            product_data,
            x="scraping_date",
            y="price",
            title=f"Évolution du prix pour {product_filter}",
            labels={"date": "Date", "effective_price": "Prix en CFA"}
            )
            st.plotly_chart(fig)
            

        #------------------------------------------

    if filter_page == "Produits en promotion":

        new_product_options = df[df["old_price"] != "Not concerned"]["title"].tolist()

        st.sidebar.selectbox("Sélectionnez un produit", options=new_product_options, index=0, key="new_product_filter")
        
        new_product_data = Load_data_product2.load_data_product(st.session_state["new_product_filter"])

        new_product_data["effective_price"] = new_product_data.apply(
            lambda row: row["old_price"] if row["old_price"] not in ["Not concerned", "True"] else row["price"],
            axis=1
        )

        # Tri des données par date dans l'ordre croissant
        new_product_data = new_product_data.sort_values(by="scraping_date", ascending=True)
        
        new_product_data["effective_price"] = new_product_data["effective_price"].str.replace("\u202f", "").str.replace("\xa0CFA", "").astype(int)

        new_product_filter = st.session_state["new_product_filter"]


        col1, col2, col3 = st.columns([1,1,2])
        with col1:
            display_product_info(new_product_data.loc[new_product_data.index[-1]])
        with col2:
            st.markdown(f"*Détails du produit : {new_product_filter}*")
            st.dataframe(new_product_data)
        
        with col3:
            fig = px.line(
            new_product_data,
            x="scraping_date",
            y="price",
            title=f"Évolution du prix pour {new_product_filter}",
            labels={"date": "Date", "effective_price": "Prix en CFA"}
            )
            st.plotly_chart(fig)