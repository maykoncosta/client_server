import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Inicializando o Firebase
cred = credentials.Certificate("client-server-52528-cdc8390cfb95.json")
try:
    firebase_admin.initialize_app(cred)
except ValueError:
    firebase_admin.get_app()

db = firestore.client()

def add_post(username, message):
    doc_ref = db.collection('posts').document()
    doc_ref.set({
        'username': username,
        'message': message,
        'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })

# Função para obter posts do Firestore
def get_posts():
    posts = db.collection('posts').stream()
    for post in posts:
        with st.chat_message("user"):
            st.write(f"{post.to_dict()['username']} ({post.to_dict()['timestamp']}): :green[{post.to_dict()['message']}]")

def clear_posts():
    docs = db.collection('posts').stream()
    for doc in docs:
        doc.reference.delete()

# Interface do Streamlit
st.title(':violet[Fórum]')
st.header('Divirta-se no forum', divider='rainbow')
st.subheader('Projeto válido para :blue[Sistemas Distribuidos] :sunglasses:')
username = st.text_input('Nome de usuário')
message = st.text_input('O que você está pensando?')

col1, col2, col3 = st.columns(3)

with col1:
    if st.button('Postar'):
        add_post(username, message)
        st.balloons()

with col2:        
    if st.button('Atualizar'):
        get_posts()

with col3:
    if st.button('Limpar todas as mensagens'):
        clear_posts()
    
    
get_posts()
