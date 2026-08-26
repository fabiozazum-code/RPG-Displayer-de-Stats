import streamlit as st
import plotly.express as px
import pandas as pd

global stat_names 
stat_names = ["Vida","Defesa","Força","Velocidade","Destreza","Carisma","Energia","Inteligência"]

global stat_ranges
stat_ranges = {
    "Vida": (0, 200, 50),
    "Defesa": (0, 75, 10),
    "Força": (0, 20, 10),
    "Velocidade": (0, 20, 10),
    "Destreza": (0, 20, 10),
    "Carisma": (0, 20, 10),
    "Energia": (0, 20, 10),
    "Inteligência": (0, 20, 10),
}



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
                        min_value=stat_ranges[stat_name][0],
                        max_value=stat_ranges[stat_name][1],
                        value=stat_ranges[stat_name][2],
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
        "r": [
            (stats[stat_name] - stat_ranges[stat_name][0])
            / (stat_ranges[stat_name][1] - stat_ranges[stat_name][0])
            * 100
            for stat_name in stat_names
        ],
        "theta": stat_names,
    })

    stat_plot_fig = px.line_polar(
        Stat_df,
        r="r",
        theta="theta",
        range_r=[0,100],
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
    return pd.DataFrame([df]).to_csv(index=False).encode("utf-8")

def save_data():
    data = {"name": name, **stats}
    st.download_button(label="Salvar stats",
                        data=convert_to_csv(data),
                        file_name=f"Stats_{name.strip()}.csv",
                        disabled= not name.strip()
                       )

def load_data():
    with st.sidebar:
        uploaded_file = st.file_uploader("Importar personagem", type="csv")

    if uploaded_file is None:
        return

    file_id = (uploaded_file.name, uploaded_file.size)
    if st.session_state.get("loaded_file_id") == file_id:
        return

    try:
        loaded_data = pd.read_csv(uploaded_file)
        if loaded_data.empty:
            raise ValueError("O arquivo CSV está vazio")

        row = loaded_data.iloc[0]
        if "name" in loaded_data.columns:
            st.session_state["character_name"] = str(row["name"])

        for stat_name in stat_names:
            if stat_name in loaded_data.columns:
                value = int(row[stat_name])
                minimum, maximum, _ = stat_ranges[stat_name]
                st.session_state[f"stat_{stat_name}"] = max(minimum, min(value, maximum))

        st.session_state["loaded_file_id"] = file_id
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
