import streamlit as st
import pandas as pd
st.title('Análise de Dados de Combustíveis')

if 'df' not in st.session_state:
    st.session_state['df'] = pd.read_parquet

st.session_state['df'] = pd.read_parquet ('combustivel_dataset_Optimized.parquet')

st.write(st.session_state['df'])

st.data_editor(st.session_state['df'], num_rows="dynamic", use_container_width=True)

pg = st.navigation([
    st.Page ("pages/pag1.py", title = "Dashboard", icon="📊"),
    st.Page ("pages/pag2.py", title = "Sobre", icon="ℹ️"),

])
pg.run()