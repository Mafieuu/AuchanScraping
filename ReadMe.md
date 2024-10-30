

# AuchanScraping
Lien vers l'application [lien](https://dashboardauchanscraping.streamlit.app/)
**AuchanScraping** est un projet réalisé en groupe dans le cadre de notre formation en Big Data et Cloud Computing à l'**ENSAE de Dakar** au premier semestre d'ISE2. L'objectif du projet est de scraper les données du site Auchan Sénégal puis de les visualiser dans un tableau de bord interactif construit avec Streamlit. 

## Structure du Projet

Le projet est organisé en deux parties :

1. **ScrapyWorkspace** : Ce dossier contient le code pour scraper le site Auchan Sénégal à l'aide de Scrapy. 
2. **AppStreamlit** : Ce dossier contient l'application Streamlit, qui génère le tableau de bord à partir des données scrappées.
3. A la base nous avons travailler deux repertoire github distinc une pour le scraping et une le dashbord.
4. La version finale est contenu dans la branche main.

### Installation et Configuration

1. Clonez le dépôt et placez vous dans le dossier AuchanScraping avec un terminal  :
   ```bash
   git clone https://github.com/Mafieuu/AuchanScraping
   cd AuchanScraping
   ```

2. Créez un environnement virtuel et activez-le :
   ```bash
   python -m venv venv
   source venv\bin\activate    # Sur MacOS/Linux
   source venv/Scripts/activate       # Sur Windows
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Exécution du Projet

###  Exécution du Tableau de Bord Streamlit

Pour démarrer l'application Streamlit, accédez au dossier `AppStreamlit` et lancez :
```bash
streamlit run app.py
```
Cela ouvrira l'interface Streamlit dans votre navigateur.
###  Exécution du Scraping

Depuis le dossier `ScrapyWorkspace`, lancez le scraping en exécutant la commande suivante :
```bash
scrapy crawl auchan
```
Le scraping récupérera les données d'Auchan Sénégal et les enregistrera dans notre base de données AWS .

## Guide d'utulisation de l'application
   Une video Youtube sera mis a disposition dans les heures qui suivent.
   Elle fera office de guide d'utulisation de l'application pour un utulisateur lambda.
## Auteurs

Ce projet a été réalisé en *deux semaine*  par :
- Ndeye Fama Diop
- Maty Dione
- Famara Sadio
- Larry Sandjo
- Moussa Dieme

