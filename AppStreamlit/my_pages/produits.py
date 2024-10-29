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


#-------------------------------------------- Nettoyer les prix et gérer les erreurs de format
    st.session_state["df"]["price"] = st.session_state["df"]["price"].str.replace("\u202f", "").str.replace("\xa0CFA", "")
    st.session_state["df"]["price"] = pd.to_numeric(st.session_state["df"]["price"], errors="coerce")  # Convertir en numérique, NaN pour erreurs
    
    # Remplacer les valeurs NaN dans is_out_of_stock par False si manquantes
    st.session_state["df"]["is_out_of_stock"] = st.session_state["df"]["is_out_of_stock"].fillna(False)
    
    # Optimiser les colonnes catégorielles
    st.session_state["df"]["category"] = pd.Categorical(st.session_state["df"]["category"])
    st.session_state["df"]["subcategory"] = pd.Categorical(st.session_state["df"]["subcategory"])


#--------------------------------------------   afficher un produit [ligne du st.session_state["df"]]
    # Oblige de redefinir la fonction car ajout de nouvelle fonctionnalite
    @st.cache_data
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
            <img src="{product_image}" alt="Image du produit" style="width:100%; height:auto; border-radius: 8px;">
            <h4>{product_name}</h4>
            <p style = "font-weight: bold;font-size: 24px;">Prix : {product_price} CFA</p>
            <p>Statut : {product_status}</p>
        </div>
        """, unsafe_allow_html=True)
    
    

#-------------------------------------------- Affichage <h1> du body produit
    st.markdown("""
        <div class="dashboard-header animate-fade-in">
            <h2 style = "text-align: center;font-weight: bold;">Page des produits</h2>
        </div>
    """, unsafe_allow_html=True)
#-------------------------------------------- Gestion du siderbar

    st.sidebar.markdown("""
        <div class="dashboard-header animate-fade-in">
            <h2 style = "text-align: center;font-weight: bold;">Produits</h2>
        </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("""
        <div class="dashboard-header animate-fade-in">
            <h2 style = "text-align: center;font-weight: bold;">Produits</h2>
        </div>
    """, unsafe_allow_html=True)

    filter_page = st.sidebar.radio(
        "Choisir un type de filtre",
        ["Filtre par Catégorie", "Filtre par Nom", "Filtre Combiné"]
    )

#-------------------------------------------- Affichage de la page en fonction du filtre
    #
    # 
    #

    cols_per_row = 6
#-------------------------------------------- Filtre par categorie
    if filter_page == "Filtre par Catégorie":

        category_options =  st.session_state["df"]["category"].unique().tolist() + ["Tous"]
        category_filter = st.sidebar.selectbox(
            "Sélectionnez une catégorie", options=category_options, index=0
        )
        
        if category_filter == "Tous":
            subcategory_options = st.session_state["df"]["subcategory"].unique().tolist() + ["Tous"]
        else:
            subcategory_options = st.session_state["df"][st.session_state["df"]["category"] == category_filter]["subcategory"].unique().tolist() + ["Tous"]

        subcategory_filter = st.sidebar.multiselect(
            "Sélectionnez une sous-catégorie",
            options=subcategory_options
        )

        
        if category_filter == "Tous" and subcategory_filter == "Tous":
            filtered_data = st.session_state["df"] 
        elif category_filter == "Tous":
            filtered_data = st.session_state["df"][st.session_state["df"]["subcategory"] == subcategory_filter]  
        elif subcategory_filter == "Tous":
            filtered_data = st.session_state["df"][st.session_state["df"]["category"] == category_filter]  
        else:
            filtered_data = st.session_state["df"][
                (st.session_state["df"]["category"] == category_filter) & 
                (st.session_state["df"]["subcategory"].isin(subcategory_filter))
            ] 

        # la variable d'etat i gere le nombre de colonne par ligne
        # st.session_state['i'] pour conserver sa valeur en cas de rechargement de la page

        if not filtered_data.empty:
            x = st.slider("Nombre maximum de produits", value = 15)
            if "i" not in st.session_state:
                st.session_state['i'] = 0
            st.session_state['i'] = 0
            cols = st.columns(cols_per_row)
            for index, row in filtered_data.iterrows():
                if  st.session_state["i"] > x:
                    break
                if st.session_state["i"] % cols_per_row == 0:
                    cols = st.columns(cols_per_row)
                col_idx = st.session_state["i"] % cols_per_row
                with cols[col_idx]:
                    st.write(st.session_state['i'])
                    display_product_info(row)
                st.session_state["i"] += 1
        else:
            st.info("Aucun produit trouvé.")


#-------------------------------------------- Filtre par nom
    elif filter_page == "Filtre par Nom": 
        search_term = st.text_input("Rechercher un produit par nom", value="")
        
        @st.cache_data
        def search_products(search_term):
            return st.session_state["df"][st.session_state["df"]["title"].str.contains(search_term, case=False)]

        filtered_data = search_products(search_term)

        if not filtered_data.empty:
            x = st.slider("Nombre maximum de produits", value = 15)
            if "i" not in st.session_state:
                st.session_state['i'] = 0
            st.session_state['i'] = 0
            cols = st.columns(cols_per_row)
            for index, row in filtered_data.iterrows():
                if  st.session_state["i"] > x:
                    break
                if st.session_state["i"] % cols_per_row == 0:
                    cols = st.columns(cols_per_row)
                col_idx = st.session_state["i"] % cols_per_row
                with cols[col_idx]:
                    st.write(st.session_state['i'])
                    display_product_info(row)
                st.session_state["i"] += 1
        else:
            st.info("Aucun produit trouvé pour cette recherche.")
#-------------------------------------------- Filtre combine

    elif filter_page == "Filtre Combiné":
        
        category_filter = st.selectbox("Sélectionnez une catégorie", options=st.session_state["df"]["category"].unique(), index=0)
        subcategory_filter = st.multiselect(
            "Sélectionnez une sous-catégorie",
            options=st.session_state["df"][st.session_state["df"]["category"] == category_filter]["subcategory"].unique(),

        )

        search_term = st.text_input("Rechercher un produit par nom", value="")

        filtered_data = st.session_state["df"][
            (st.session_state["df"]["category"] == category_filter)
            & (st.session_state["df"]["subcategory"].isin(subcategory_filter))
            & (st.session_state["df"]["title"].str.contains(search_term, case=False))
        ]

        if not filtered_data.empty:
            x = st.slider("Nombre maximum de produits", value = 15)
            if "i" not in st.session_state:
                st.session_state['i'] = 0
            st.session_state['i'] = 0
            cols = st.columns(cols_per_row)
            for index, row in filtered_data.iterrows():
                if  st.session_state["i"] > x:
                    break
                if st.session_state["i"] % cols_per_row == 0:
                    cols = st.columns(cols_per_row)
                col_idx = st.session_state["i"] % cols_per_row
                with cols[col_idx]:
                    st.write(st.session_state['i'])
                    display_product_info(row)
                st.session_state["i"] += 1
        else:
            st.info("Aucun produit trouvé pour ces filtres combinés.")
#-------------------------------------------- Affichage des produit en promotion

    #
    # Cette partie est independant des filtres
    #
    st.markdown("""
            <div class="dashboard-header animate-fade-in">
                <h3 style = "text-align: center;font-weight: bold;">Produits en promotion</h3>
            </div>
        """, unsafe_allow_html=True)

    on_promotion = st.session_state["df"][st.session_state["df"]["old_price"] != "Not concerned"]
    if not on_promotion.empty:
            if "i" not in st.session_state:
                st.session_state['i'] = 0
            st.session_state['i'] = 0
            cols = st.columns(cols_per_row)
            for index, row in on_promotion.iterrows():
                if st.session_state["i"] % cols_per_row == 0:
                    cols = st.columns(cols_per_row)
                col_idx = st.session_state["i"] % cols_per_row
                with cols[col_idx]:
                    st.write(st.session_state['i'])
                    display_product_info(row)
                st.session_state["i"] += 1

#-------------------------------------------- Affichage des produit en rupure de stock

    #
    # Cette partie est independant des filtres
    #
    st.markdown("""
            <div class="dashboard-header animate-fade-in">
                <h3 style = "text-align: center;font-weight: bold;">Produits en rupture de stock</h3>
            </div>
        """, unsafe_allow_html=True)
    out_of_stock_products = st.session_state["df"][st.session_state["df"]["is_out_of_stock"] == True]
    if not out_of_stock_products.empty:
            if "i" not in st.session_state:
                st.session_state['i'] = 0
            st.session_state['i'] = 0
            cols = st.columns(cols_per_row)
            for index, row in out_of_stock_products.iterrows():
                if st.session_state["i"] % cols_per_row == 0:
                    cols = st.columns(cols_per_row)
                col_idx = st.session_state["i"] % cols_per_row
                with cols[col_idx]:
                    st.write(st.session_state['i'])
                    display_product_info(row)
                st.session_state["i"] += 1




