1 asynchio et aioshttp pour gerer la synchronisation
2 un script scraper.py :
- scrap_categ_("auchan.sn") qui recup :
{"lien":[name_categorie,name_subcategorie]}
si une categorie n'a pas de sub categorie alors name_subcategorie=False
et lien= lien categorie
sinon lien = lien sub categorie
- scrap_produit_infos(url,class_id,multi_page=True):
    scrape tous les articles de ce lien.retourn un
    dict {id:[name,price_before,price_real,categorie,sub_categorie,img,...]}
- asynch scrap_multipage():appel scrap_produit_info 
de mainiere asynchrone pour scraper tous les produit d'une categorie donnne (page 1,2,...)
scrap_new_produ():appel scrap_produit_infos () avec le bon id
==========
Trouver un moyen de sauvegarder le resultat de scrap_produit_infos chaque fois qu'une page est completement scrape
un script main.py l'orchestre eventuelement un script pour tout ce qui est mysql
- il semble que aiomysql permet de faire des connexion asynchrone sur la base de donne
- Trouver un moyen de maj la base de donnee tous les 24 heures
- suivre les recommandation du fichier robot.txt