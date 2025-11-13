import streamlit as st
import requests
import os

# URL du backend FastAPI
API_BASE_URL = os.getenv("API_BASE_URL", "http://backend-api-service:8000")

st.title("Clients Management Dashboard")

# --- Afficher tous les clients ---
st.header("Liste des clients")

try:
    response = requests.get(f"{API_BASE_URL}/clients")
    response.raise_for_status()
    clients = response.json()
except requests.exceptions.RequestException as e:
    st.error(f"Erreur lors de la récupération des clients: {e}")
    clients = []

if clients:
    for client in clients:
        full_name = f"{client['first_name']} {client['last_name']}"
        st.write(f"ID: {client['id']} | Nom: {full_name} | Email: {client['email']}")
        if st.button(f"Supprimer {full_name}", key=f"delete-{client['id']}"):
            try:
                delete_resp = requests.delete(f"{API_BASE_URL}/clients/{client['id']}")
                if delete_resp.status_code == 204:
                    st.success(f"Client {full_name} supprimé !")
                    st.rerun()
                else:
                    st.error(f"Erreur lors de la suppression: {delete_resp.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur lors de la suppression: {e}")
else:
    st.info("Aucun client trouvé.")

# --- Ajouter un nouveau client ---
st.header("Ajouter un nouveau client")

with st.form("add_client_form"):
    name = st.text_input("Nom complet")
    email = st.text_input("Email")
    submitted = st.form_submit_button("Ajouter")

    if submitted:
        if not name or not email:
            st.error("Veuillez remplir tous les champs")
        else:
            # Séparer le prénom et le nom
            first_name, *last_name_parts = name.strip().split()
            last_name = " ".join(last_name_parts) if last_name_parts else ""
            payload = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email
            }

            try:
                post_resp = requests.post(f"{API_BASE_URL}/clients", json=payload)
                if post_resp.status_code == 201:
                    st.success(f"Client {name} ajouté !")
                    st.rerun()
                else:
                    detail = post_resp.json().get("detail", post_resp.text)
                    st.error(f"Erreur: {detail}")
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur lors de l'ajout: {e}")

