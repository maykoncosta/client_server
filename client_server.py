import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializando o Firebase
cred = credentials.Certificate("client-server-52528-cdc8390cfb95.json")
try:
    firebase_admin.initialize_app(cred)
except ValueError:
    firebase_admin.get_app()

db = firestore.client()

# Função para adicionar post ao Firestore
def add_post(username, message):
    doc_ref = db.collection('posts').document()
    doc_ref.set({
        'username': username,
        'message': message
    })

# Função para obter posts do Firestore
def get_posts():
    posts = db.collection('posts').stream()
    for post in posts:
        st.write(f"{post.to_dict()['username']}: {post.to_dict()['message']}")

# Interface do Streamlit
st.title('Fórum')
username = st.text_input('Nome de usuário')
message = st.text_input('O que você está pensando?')
if st.button('Postar'):
    add_post(username, message)
get_posts()
