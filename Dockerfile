# Utiliser l'image officielle de Python
FROM python:3.12

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt depuis le répertoire parent
COPY ../requirements.txt 

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de votre application depuis le dossier AppStreamlit
COPY . .

# Exposer le port utilisé par Streamlit
EXPOSE 8501

# Commande pour exécuter l'application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.host=0.0.0.0"]
