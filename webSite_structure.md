## structure de Auchan.sn
### Menu deroulant
<ul id="top-menu">
- chaque children est un <li class=category menu-item menu-depth0-item >
ce sont les seuls <li> de notre div
- chaque li a un children <a class=dropdown-item menu-link menu-depth0-link>
- chaque <a> a un <img class=menu-depth0-icon>  et aussi un children  <span class="link-label">
Ne pas oublier de scraper la page "Promotions"
certains categories ont des sub-categories ce sont des <li id=categorie - xxx> ayant des <div id="top_sub_menu_53316">.Dans ces div si on deroule deroule on tombe sur des <ul class=" top-menu menu-list menu-depth1-list"> dans ce dernier on a des <li id="category-xxx"> 
chaque li a un <a> qui lui meme a un children <span>
===============================================
Pour les categorie et les sous-categorie la structure des pages web sont identique.
si une categorie a des sous-categorie alors ne pas scraper cette categorie
- tous les articles sont dans un div <div class=products row> avec eds children <article class="product-miniature js-product-miniature ">
<!-- - chaque <article> a un seul <div class="thumbnail-container reviews-loaded"> dans lequel:
-- <div class="thumbnail-block"> il a un <a> qui pointe vers les details du produit.ce a possede un <img> ce img a un arg data-full-size-image-url qui lui meme pointe vers une image ???
-- <div class="product-description"> il a un children div
dans ce div on a :
--- <h2 class="h3 product-title"> ce h2 a un <a> qui pointe vers les details du produits
--- <div class= "weight"> ce div a 2 span: class="weight" pour le poids et class=unit_price pour le prix.
---- <div class="price-line"> ???????
---- <div class="consigne-line">????
---- <div class="product-list-reviews"> ??????? -->
Dans un article:
- le titre est dans un <h2 class="h3 product-title"> c'est le texte du <a>
- l'image est dans un <a class="thumbnail product-thumbnail"> lui meme dans un <div class="thumbnail-block">
- Le prix est dans un <span class="price "> lui meme dans un <div class="product-price-and-shipping">
Pour des prix qui ont un changement alors prix est dans un <span class="price has-discount"> et l'ancien prix est dans <span class="regular-price"> et <span class="price "> n'existe plus
ripture ou pas est dans un <span class="rupture"> lui meme dans un <div class="thumbnail-container reviews-loaded">.attention ripture n'exsiste que pour les articles en rupture de sock
- claque article a un identifiant dans "data-id-product" argument de <article>
- pour switcher dans les differents pages on ajoute dans le lien ?page=**
si on atteint une page ou <article> n'existe pas alors on a atteint la page max.
==========================
Pour https://www.auchan.sn/promotions il semble que c'est juste un filtrage des produits ayant un prix en baisse

================
Pour la descriptions des produits on verra ....
Scraper les nouveaux produits de la firme dans la page d'acueil

