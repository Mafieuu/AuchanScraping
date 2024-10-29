from my_pages.call_local_function import *
import streamlit as st
import pandas as pd
import plotly.express as px
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


#-------------------------------------------- Etiquette de page
    col1, col2, col3 = st.sidebar.columns([1, 2, 1])
    with col2: 
        st.sidebar.markdown("""
            <div class="dashboard-header animate-fade-in">
                <h2 style = "text-align: center;font-weight: bold;">Visualisations</h2>
            </div>
        """, unsafe_allow_html=True)
#============================================= Section statistique
    st.markdown("""
            <div class="dashboard-header animate-fade-in">
                <h2 style = "text-align: center;font-weight: bold;">Statistiques</h2>
            </div>
        """, unsafe_allow_html=True)

#-------------------------------------------- Fonction afficheur de statistiquesde prix par categorie

    def display_price_statistics(df, type, category): #on conserve ici car utulise une seul fois

        # Filtrer le DataFrame pour la catégorie sélectionnée
        category_data = df[df[type] == category]

        
        # Calcul des statistiques
        mean_price = category_data["price"].mean()
        median_price = category_data["price"].median()
        price_variance = category_data["price"].var()
        max_price = category_data["price"].max()
        min_price = category_data["price"].min()

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.info('Moyenne des prix',icon="📌")
            display_custom_metric("Moyenne des prix", int(mean_price), "#0000FF")
        with col2:
            st.info('Médiane des prix',icon="📌")
            display_custom_metric("Médiane des prix", int(median_price), "#228B22")
        with col3:
            st.info('Variance des prix',icon="📌")
            display_custom_metric("Variance des prix", int(price_variance), "#FF0000")
        with col4:
            st.info('Prix maximal',icon="📌")
            display_custom_metric("Prix maximal", int(max_price), "#FE9900")
        with col5:
            st.info('Prix minimal',icon="📌")
            display_custom_metric("Prix minimal", int(min_price), "#582698")

#--------------------------------------------siderbar widget choix categorie et affichage section statistique
    st.sidebar.selectbox("Choisissez une catégorie", options=st.session_state["df"]["category"].unique(), key="key_categories")
    display_price_statistics(st.session_state["df"], "category",st.session_state["key_categories"])

#============================================= Repartition

#-------------------------------------------- Figures de la section
    filtered_df = st.session_state["df"][st.session_state["df"]["category"] == st.session_state["key_categories"]]

    filtered_df = st.session_state["df"][st.session_state["df"]["category"] == st.session_state["key_categories"]]
    fig = px.pie(
        filtered_df,
        names="subcategory",
        values="price",
        title=f"Répartition des sous-catégories pour la catégorie '{st.session_state['key_categories']}'",
        labels={"subcategory": "Sous-Catégorie"},
        hole=0.3,
    )
    fig.update_traces(textinfo="label+percent", textfont_size=16)
    fig.update_layout(title_font_size=24, legend_font_size=14)

    st.markdown("""
            <div class="dashboard-header animate-fade-in">
                <h3 style = "text-align: center;font-weight: bold;">Repartition des sous-categories par categorie</h3>
            </div>
        """, unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
#============================================= section moyenne par categorie et nombre produit par intervalle

    col1, col2 = st.columns([2, 2])

    with col1: 
        st.markdown("""
            <div class="dashboard-header animate-fade-in">
                <h3 style = "text-align: center;font-weight: bold;">Moyenne des prix par categories</h3>
            </div>
        """, unsafe_allow_html=True)

    avg_price = st.session_state["df"].groupby("category")["price"].mean().reset_index()
    with col1:
        fig_price_mean_cat = px.bar(
        avg_price,
        y="price",
        color="category",
        title=" ",
        labels={"category": "Catégorie", "price": "Valeur en CFA"})
        fig_price_mean_cat.update_layout(
        title_font_size=9,         # Taille du titre
        legend_font_size=14,        # Taille de la légende
        xaxis_title_font_size=14,   # Taille de l'axe des X
        yaxis_title_font_size=14,   # Taille de l'axe des Y
        xaxis=dict(tickfont=dict(size=16)),  # Taille des étiquettes des X
        yaxis=dict(tickfont=dict(size=16))   # Taille des étiquettes des Y
    ) 
        fig_price_mean_cat.update_xaxes(showticklabels=False)
        st.plotly_chart(fig_price_mean_cat, use_container_width=True)
        

    with col2: 
        st.markdown("""
            <div class="dashboard-header animate-fade-in">
                <h3 style = "text-align: center;font-weight: bold;">Nombre de produits pour chaque intervalle de prix</h3>
            </div>
        """, unsafe_allow_html=True)

    max_price = st.sidebar.slider("Choisissez le prix maximum", min_value=10000, max_value=int(st.session_state["df"]["price"].max()), step=2500)

    # Filtrer les produits en dessous du prix sélectionné
    filtered_df = st.session_state["df"][st.session_state["df"]["price"] <= max_price]

    # Créer une colonne pour les intervalles de prix
    filtered_df["price_range"] = pd.cut(filtered_df["price"], bins=range(0, max_price + 2500, 2500)).astype(str)

    # Créer un histogramme coloré par intervalle de prix
    fig_inter_prix = px.histogram(
        filtered_df,
        x="price_range",
        color="price_range",
        title= " ",
        labels={"price_range": "Intervalle de prix", "count": "Nombre de produits"}
    )

    fig_inter_prix.update_xaxes(showticklabels=False)

    fig_inter_prix.update_layout(
        title_font_size=9,         
        legend_font_size=14,        
        xaxis_title_font_size=14,   
        yaxis_title_font_size=14,   
        xaxis=dict(tickfont=dict(size=16)),  # Taille des étiquettes des X
        yaxis=dict(tickfont=dict(size=16))   # Taille des étiquettes des Y
    ) 
    # Afficher le graphique
#============================================= Section nuage de point

    with col2: st.plotly_chart(fig_inter_prix, use_container_width=True)

    st.markdown("""
            <div class="dashboard-header animate-fade-in">
                <h3 style = "text-align: center;font-weight: bold;">Nuage de points de prix par categorie</h3>
            </div>
        """, unsafe_allow_html=True)

    fig = px.scatter(
        st.session_state["df"], x="category", y="price", color="category", title=" ")
    fig.update_layout(
        title_font_size=9,         # Taille du titre
        legend_font_size=14,        # Taille de la légende
        xaxis_title_font_size=14,   # Taille de l'axe des X
        yaxis_title_font_size=14,   # Taille de l'axe des Y
        xaxis=dict(tickfont=dict(size=16)),  # Taille des étiquettes des X
        yaxis=dict(tickfont=dict(size=16))   # Taille des étiquettes des Y
    ) 
    fig.update_xaxes(showticklabels=False)
    st.plotly_chart(fig, use_container_width=True)
