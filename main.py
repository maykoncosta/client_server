import streamlit as st
import firebase_admin

from firebase_admin import credentials, db, auth

cred = credentials.Certificate('client-server-52528-cdc8390cfb95.json')
try:
    default_app = firebase_admin.get_app()
except ValueError:
    default_app = firebase_admin.initialize_app(cred)

st.title("Bem vindo ao APP :violet[Cliente-Servidor]")

choice = st.selectbox('Login/Signup', ['Login', 'Sing Up'])

if choice == 'Login':
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
        
    st.button('Login!!')

else:
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    username = st.text_input('Usuario') 
        
    if st.button('Criar minha conta!!'):
        user = auth.create_user(email = email, password = password, uid=username)
        st.success('Conta criada com sucesso!')
        st.markdown('Por Favor, logue usando seu e-mail e senha.')
        st.balloons()