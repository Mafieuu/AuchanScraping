import streamlit as st

#
# Certains fonction sont commun a plusieurs pages, elles seront definit ici
#

#-------------------------------------------- Fonction pour afficher les images une par une
@st.cache_data
def display_image(image_url):
    # TODO: avec les 3.000 images dispo en local,si l'image est en local alors le recupeere
    # TODO: sinon le telecharger depuis les serveurs de auchan

    """
        retourne l'image si elle est disponible.
        sinon retourne l'image <no image >
    """
    if not image_url or image_url == "NaN":
        st.image("https://github.com/Mafieuu/img_depot/blob/main/missing.jpeg", width=200) 
    else:
        st.image(image_url, width=200)

#--------------------------------------------   afficher un produit [ligne du df]

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
            <img src="{product_image}" alt="Image du produit" style="width:50%; height:auto; border-radius: 8px;">
            <h4>{product_name}</h4>
            <p style = "font-weight: bold;font-size: 24px;">Prix : {product_price} CFA</p>
            <p>Statut : {product_status}</p>
        </div>
        """, unsafe_allow_html=True)



# Affiche une métrique personnalisée [les gris pour total produit,max,...]

def display_custom_metric(label, value, color):
    """
    return st.markdown
    """
    st.markdown(
        f"""
        <div style="background-color: {color}; padding: 20px; border-radius: 10px; margin: 5px 0;">
            <p style="font-size: 9px; margin: 0; color: white;">{label}</p>
            <h2 style="margin: 0; color: white; font-weight: bold">{value}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
