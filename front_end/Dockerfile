# Utiliser l'image officielle Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers requirements.txt et installer les dépendances
COPY streamlit/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le reste du code
COPY ./streamlit .

# Exposer le port utilisé par Streamlit
EXPOSE 8501

# Commande pour lancer Streamlit
CMD ["streamlit", "run", "app.py"]