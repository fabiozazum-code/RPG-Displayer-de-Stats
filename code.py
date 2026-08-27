import streamlit as st
import plotly.express as px
import pandas as pd
import json

global stat_names 
stat_names = ["Ataque", "Velocidade", "Defesa", "Cura", "Inteligência", "Polimata"]

def configure_page():
    st.set_page_config(
        page_title="Organizador de stats",
        page_icon="🏳️‍🌈",
        layout="wide"
    )

def configure_sidebar():
    with st.sidebar:
        with st.form("character_form"):

            global name
            name = st.text_input("Nome do personagem", key="character_name")

            global stats
            stats = {
                    stat_name: st.slider(
                        stat_name,
                        min_value=0,
                        max_value=350,
                        step=50,
                        value=50,
                        key=f"stat_{stat_name}",
                    )
                    for stat_name in stat_names
                }

            submit = st.form_submit_button("Entregar")

            if submit:
                if name.strip():
                    st.success(f"Stats de {name} enviados")
                else:
                    st.error("Preencha o nome do personagem")

            
def configure_spider_plot():

    st.title(name, text_alignment="center")

    Stat_df = pd.DataFrame({
        "r": [stats[stat_name] for stat_name in stat_names],
        "theta": stat_names,
    })

    stat_plot_fig = px.line_polar(
        Stat_df,
        r="r",
        theta="theta",
        range_r=[0,350],
        line_close=True,
        template="plotly_dark",
    )

    stat_plot_fig.update_traces(fill="toself")
    stat_plot_fig.update_layout(hovermode=False, clickmode="none")

    st.plotly_chart(
       stat_plot_fig,
        use_container_width=True,
        config={
            "scrollZoom": False,
            "staticPlot": True,
        }
    )

def convert_to_csv(df):
    return pd.DataFrame([df]).to_json(index=False).encode("utf-8")

def save_data():
    data = {"name": name, **stats}
    st.download_button(label="Salvar stats",
                       data=json.dumps(data),
                        file_name=f"Stats_{name.strip()}.json"
                       )

def load_data():
    with st.sidebar:
        uploaded_file = st.file_uploader("Importar personagem", type="json")

    if uploaded_file is None:
        return
    
    try:
        Jason_f = pd.read_json(uploaded_file, typ="series")

        if Jason_f.empty:
            raise ValueError("O arquivo json está vazio")

        st.session_state["character_name"] = str(Jason_f["name"])

        for stat_name in stat_names:
            st.session_state[f"stat_{stat_name}"] = int(Jason_f[stat_name])
        
        
        st.success("Stats importados com sucesso")

    except (ValueError, TypeError, KeyError) as error:
        st.error(f"Não foi possível enviar o arquivo devido a {error}")
                                
def main():
    configure_page()
    load_data()
    configure_sidebar()
    configure_spider_plot()
    save_data()

if __name__ == "__main__":
    main()
