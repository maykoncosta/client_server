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

# Obter posts do Banco
def get_posts():
    posts = db.collection('posts').stream()
    for post in posts:
        with st.chat_message("user"):
            st.write(f"{post.to_dict()['username']} ({post.to_dict()['timestamp']}): :green[{post.to_dict()['message']}]")

# Limpar posts do Banco
def clear_posts():
    docs = db.collection('posts').stream()
    for doc in docs:
        doc.reference.delete()

# Interface do Streamlit
st.title(':violet[Fórum]')
st.header('Divirta-se no forum', divider='rainbow')
st.subheader('Projeto válido para :blue[Sistemas Distribuidos] :sunglasses:')

# Adicionar novo usuario no Banco
def add_user(username, password):
    doc_ref = db.collection('users').document(username)
    doc_ref.set({
        'password': password,
        'logged_in': False
    })

# Verificar se um usuário existe no Banco
def user_exists(username):
    doc_ref = db.collection('users').document(username)
    return doc_ref.get().exists

# Verificar as credenciais do usuário
def check_credentials(username, password):
    if user_exists(username):
        doc_ref = db.collection('users').document(username)
        return doc_ref.get().to_dict()['password'] == password
    return False

# Função para definir o estado de login do usuário
def set_login_state(username, state):
    doc_ref = db.collection('users').document(username)
    doc_ref.update({
        'logged_in': state
    })

# Função para obter o estado de login do usuário
def get_login_state(username):
    if not username:
        return False
    if user_exists(username):
        doc_ref = db.collection('users').document(username)
        return doc_ref.get().to_dict()['logged_in']
    return False

# Se o usuário não estiver logado, mostre a tela de login e cadastro
username = ''
if not get_login_state(username):
    username = st.text_input('Nome de usuário')
    password = st.text_input('Senha', type='password')

    colunaLogin, colunaCadastro = st.columns(2)

    with colunaLogin:   
        if st.button('Login'):
            if check_credentials(username, password):
                set_login_state(username, True)
                st.success('Login bem sucedido!')
            else:
               st.error('Nome de usuário ou senha incorretos.')

    with colunaCadastro:
        if st.button('Cadastrar'):
            if user_exists(username):
                st.error('Nome de usuário já existe.')
            else:
                add_user(username, password)
                st.success('Usuário cadastrado com sucesso!')

# Mostrar se usuario estiver logado
if username and password and get_login_state(username):

        
    message = st.text_input('O que você está pensando??')
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button('Postar'):
            add_post(username, message)
            st.balloons()

    with col3:
        if st.button('Limpar todas as mensagens'):
            clear_posts()
    
    if st.button('Sair'):
        set_login_state(username, False)
        username = ''
        password = ''
    
    st.divider()
    get_posts()

