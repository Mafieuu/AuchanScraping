import streamlit as st
from streamlit_option_menu import option_menu
from my_pages import evolution,Visualisations,produits ,accueil 
from my_pages import Load_data_date

#--------------------------------------------  l'en-tête commun
st.set_page_config(
    page_title="Auchan",
      page_icon="♨️", 
      layout="wide",
    initial_sidebar_state="expanded"
)
#-------------------------------------------- chargement css

# Chargement du css personnalise (modifications des classe et id par defaut de streamlit)

with open("css/custom_style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

with open('css/style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)



#-------------------------------------------- Le sliderbar commun


with st.sidebar:
    st.markdown('<div class="sidebar-logo">', unsafe_allow_html=True)
    st.image(
        "images/Auchan-Logo.png",
        caption="Dashboard Auchan",
        use_column_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

def display_header():
    st.markdown("""
        <div class="dashboard-header animate-fade-in">
            <h1 style = "font-weight: bold;">DASHBOARD DE SUIVI DES PRIX DE AUCHAN SENEGAL</h1>
        </div>
    """, unsafe_allow_html=True)

#--------------------------------------------Affichage de l'en-tête 

display_header()




#-------------------------------------------- menu navigation

page = option_menu( # voir help du package streamlit_option_menu
    menu_title=None,
    options=["Accueil", "Produits",  "Visualisations", "Evolution"],
    icons=["house-fill", "tags-fill", "diagram-2-fill", "cart-fill", "graph-up-arrow"],
    menu_icon=None,
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important"},
        "icon": {"font-size": "1rem"},
        "nav-link": {"font-size": "0.9rem", "text-align": "center", "margin": "0px"},
        "nav-link-selected": {"background-color": "#e63946"},
    }
)

st.write("\n  ")

#--------------------------------------------Photo de Auchan du body for alls pages
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.markdown("""
        <div class="dashboard-header animate-fade-in">
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="dashboard-header animate-fade-in">
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="dashboard-header animate-fade-in">
        </div>
    """, unsafe_allow_html=True)
with col2: 
    st.image("images/Photo2.png", width=1000)
with col3:
    st.markdown("""
        <div class="dashboard-header animate-fade-in">
        </div>
    """, unsafe_allow_html=True)
    
st.markdown("---")

#--------------------------------------------Choix des dates dans sliderbar pour pages autres que Evolution

all_dates=Load_data_date.load_data_time() # Listes des dates dispo dans la base de donnee
if "all_dates" not in st.session_state:
    st.session_state["all_dates"]=list(sorted(all_dates,reverse=True))
    # les dates ne changeront pas aucour d'une session


st.sidebar.selectbox(
label="Choisissez une date :",
options=st.session_state["all_dates"],
key="choix_date"
)
#--------------------------------------------action sur les pages
 
if page == "Visualisations":
    Visualisations.display()
elif page == "Produits":
    produits.display()
elif page == "Evolution":
    evolution.display()
else:
    accueil.display()







#-------------------------------------------- Pied de page

st.markdown("""
    <div class="footer">
        <p>ENSAE 2024/2025- TP Big Data<br>
            -Fama
            -Maty
            -Famara
            -Larry
            -Moussa
            </p>
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)