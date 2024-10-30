

# AuchanScraping

**AuchanScraping** est un projet réalisé en groupe dans le cadre de notre formation en Big Data et Cloud Computing à l'**ENSAE de Dakar** au premier semestre d'ISE2. L'objectif du projet est de scraper les données du site Auchan Sénégal puis de les visualiser dans un tableau de bord interactif construit avec Streamlit. 

## Structure du Projet

Le projet est organisé en deux parties :

1. **ScrapyWorkspace** : Ce dossier contient le code pour scraper le site Auchan Sénégal à l'aide de Scrapy. 
2. **AppStreamlit** : Ce dossier contient l'application Streamlit, qui génère le tableau de bord à partir des données scrappées.
3. A la base nous avons travailler deux repertoire github distinc une pour le scraping et une le dashbord.
4. La version finale est contenu dans la branche main.

## Prérequis

1. **Python** : Assurez-vous que Python 3.x est installé sur votre machine.A l'heure actuelle la version 3.13 qui vient recement de sortir est incompatible avec Streamlit
2. **Environnement Virtuel** :  utilisez un environnement virtuel.

### Installation et Configuration

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/Mafieuu/AuchanScraping
   cd AuchanScraping
   ```

2. Créez un environnement virtuel et activez-le :
   ```bash
   python -m venv venv
   source venv/bin/activate    # Sur MacOS/Linux
   venv\Scripts\activate       # Sur Windows
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration des accès à la base de données**  
   Se munir du fichier `secret.txt` contenant le mot de passe pour la connexion à la base de données AWS. Ce fichier **n'est pas inclus dans le dépôt** pour des raisons de sécurité.

   - Placez une copie du fichier `secret.txt` dans les dossiers suivants :
     - `ScrapyWorkspace`
     - `AppStreamlit/my_pages`

## Exécution du Projet

### Étape 1 : Exécution du Scraping

Depuis le dossier `ScrapyWorkspace`, lancez le scraping en exécutant la commande suivante :
```bash
scrapy crawl auchan
```
Le scraping récupérera les données d'Auchan Sénégal et les enregistrera dans notre base de données AWS .

### Étape 2 : Lancement du Tableau de Bord Streamlit

Pour démarrer l'application Streamlit, accédez au dossier `AppStreamlit` et lancez :
```bash
streamlit run app.py
```
Cela ouvrira l'interface Streamlit dans votre navigateur, permettant d'explorer les données scrappées via un tableau de bord interactif.


## Auteurs

Ce projet a été réalisé en *deux semaine*  par :
- Ndeye Fama Diop
- Maty Dione
- Famara Sadio
- Larry Sandjo
- Moussa Dieme

