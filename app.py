import streamlit as st
import pandas as pd 
import altair as alt
from PIL import Image 

st.set_page_config(layout="wide")

@st.cache_data
def generate_df(data_path):
    
    df = pd.read_excel(
        io = data_path,
        engine = "openpyxl",
        sheet_name="Plan1",
        usecols="A:Q",
        nrows=21044
    )

    return df

if '__main__'==__name__:

    data_path = 'fuel_dataset_anp.xlsx'

    df = generate_df(data_path)

    colunas_uteis = ['MÊS', 'PRODUTO', 'REGIÃO', 'ESTADO', 'PREÇO MÉDIO REVENDA']

    df = df[colunas_uteis]

    with st.sidebar:
        st.subheader('Fuel Prices in Brazil')
        logo_teste = Image.open('fuel_prices.jpg')
        st.image(logo_teste, use_column_width=True)
        st.subheader('Filter selection')
        fProduct = st.selectbox(
            "Seclect fuel tipe: ",
            options=df['PRODUTO'].unique()
        )

        fState = st.selectbox(
            "Select the State: ",
            options=df["ESTADO"].unique()
        )

        filtered_df = df.loc[
            (df['PRODUTO'] == fProduct) &
            (df['ESTADO'] == fState)
        ]

    updateDate = filtered_df["MÊS"].dt.strftime('%Y/%b')
    filtered_df['MÊS'] = updateDate
    
    st.header('Fuel Price in Brazil - 2013 to 2023')
    st.markdown('**Selected Fuel**: ' + fProduct)
    st.markdown('**Selected State**: ' + fState)

    graph_fuel_state = alt.Chart(filtered_df).mark_line(
        point=alt.OverlayMarkDef(color='red', size=20)
    ).encode(
        x = 'MÊS:T',
        y = 'PREÇO MÉDIO REVENDA',
        strokeWidth = alt.value(3)
    ).properties(
        height = 700,
        width = 1200
    )

    st.altair_chart(graph_fuel_state)