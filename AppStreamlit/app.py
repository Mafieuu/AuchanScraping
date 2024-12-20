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

st.markdown("""
<style>

/* Variables globales */
:root {
    --auchan-red: #e63946;
    --auchan-red-dark: #e63946;
    --auchan-red-light: #fde8eb;
    --background-light: #f8f9fa;
    --shadow-sm: 0 2px 4px rgba(0,0,0,0.1);
    --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
    --border-radius: 8px;
}



.main {
    padding: 1.5rem;
}

/* Sidebar */
.sidebar .sidebar-content {
    background-color: white;
    padding: 1rem;
}

.sidebar-logo {
    padding: 1rem;
    margin-bottom: 2rem;
}

.sidebar-logo img {
    border-radius: var(--border-radius);
    box-shadow: var(--shadow-sm);
    transition: transform 0.3s ease;
}

.sidebar-logo img:hover {
    transform: scale(1.02);
}

.sidebar-logo .caption {
    text-align: center;
    margin-top: 0.5rem;
    color: var(--auchan-red);
    font-weight: 500;
}

/* Header */
.dashboard-header {
    background-color:#E4080A;
    color: white;
    padding: 1.5rem;
    border-radius: var(--border-radius);
    margin-bottom: 2rem;
    box-shadow: var(--shadow-md);
}

.dashboard-header h1 {
    text-align: center;
    font-size: 3rem;
    color: white;
    font-weight: 600;
    margin: 0;
    text-transform: uppercase;
}

.dashboard-header h2 {
    text-align: center;
    font-size: 2rem;
    color: white;
    font-weight: 600;
    margin: 0;
    text-transform: uppercase;
}

.dashboard-header h3 {
    text-align: center;
    font-size: 1.5rem;
    color: white;
    font-weight: 600;
    margin: 0;
    text-transform: uppercase;
}

/* Menu de navigation */
#MainMenu {
    background-color: white;
    border-radius: var(--border-radius);
    padding: 0.5rem;
    margin-bottom: 2rem;
    box-shadow: var(--shadow-sm);
}

.nav-link {
    color: var(--auchan-red) !important;
    transition: all 0.3s ease;
    border-radius: var(--border-radius);
    margin: 0.2rem;
}

.nav-link:hover {
    background-color: var(--auchan-red-light) !important;
    transform: translateY(-1px);
}

.nav-link.active {
    background-color:#e63946;
    color: white !important;
    box-shadow: var(--shadow-sm);
}

.nav-link .icon {
    margin-right: 0.5rem;
}

/* Cards */
.custom-card {
    background: white;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow-sm);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    transition: transform 0.3s ease;
}

.custom-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.card-title {
    color: var(--auchan-red);
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 1rem;
}

/* Boutons */
.stButton > button {
    background-color: var(--auchan-red);
    color: white;
    border: none;
    padding: 0.5rem 1.5rem;
    border-radius: var(--border-radius);
    font-weight: 500;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background-color: var(--auchan-red-dark);
    transform: translateY(-1px);
    box-shadow: var(--shadow-sm);
}

/* Widgets Streamlit */
.stSelectbox, .stTextInput, .stDateInput {
    background-color: white;
    border-radius: var(--border-radius);
    padding: 0.5rem;
    margin-bottom: 1rem;
}

/* Tables */
.dataframe {
    border: none !important;
    box-shadow: var(--shadow-sm);
    border-radius: var(--border-radius);
}

.dataframe th {
    background-color: var(--auchan-red) !important;
    color: white !important;
}

.dataframe tr:hover {
    background-color: var(--auchan-red-light) !important;
}

/* Footer */
.footer {
    background-color: white;
    padding: 1.5rem;
    margin-top: 2rem;
    border-radius: var(--border-radius) var(--border-radius) 0 0;
    box-shadow: var(--shadow-sm);
    text-align: center;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in {
    animation: fadeIn 0.5s ease forwards;
}
/* marche pas ! */
.nav-item{
    background-color:#e63946;


}
.stSidebar{
    background-color:#F0D076;
}

            


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

/* Pied de page */
.footer {
    background-color: white;
    padding: 1.5rem;
    margin-top: 2rem;
    border-radius: var(--border-radius) var(--border-radius) 0 0;
    box-shadow: var(--shadow-sm);
    text-align: center;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
    animation: fadeIn 0.5s ease forwards;
}
</style>
""", unsafe_allow_html=True)


#-------------------------------------------- Le sliderbar commun


with st.sidebar:
    st.markdown('<div class="sidebar-logo">', unsafe_allow_html=True)
    st.image(
        "https://logos-world.net/wp-content/uploads/2021/02/Auchan-Logo.png",
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
        "icon": {"font-size": "1.3rem"},
        "nav-link": {"font-size": "1.2em", "text-align": "center", "margin": "0px"},
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
    st.image("https://blog.lengow.com/wp-content/uploads/2016/02/logo-auchan-2015-1050x276-700x184.png", width=800)
with col3:
    st.markdown("""
        <div class="dashboard-header animate-fade-in">
        </div>
    """, unsafe_allow_html=True)

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
            Fama
            -Maty
            -Famara
            -Larry
            -Moussa
            </p>
            <img src="https://ensai.fr/wp-content/uploads/2019/07/ENSAE-Dakar-logo.png" alt="Image du produit" style="width:5%; height:auto; border-radius: 8px;">
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)