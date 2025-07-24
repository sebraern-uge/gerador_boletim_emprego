import streamlit as st
from streamlit_option_menu import option_menu
import papermill as pm
import nbformat
import os
import re
import unicodedata

def normalizar_string(texto):
    return unicodedata.normalize("NFC", texto)

# ─── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Gerador de Boletim de Emprego - SEBRAE/RN",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="auto"
)

# ─── Cabeçalho com logo e nome ────────────────────────────────────────────────
st.markdown(
    """
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
        <h3 style="margin: 0; color: #4169E1;">SEBRAE/RN</h3>
    </div>
    """,
    unsafe_allow_html=True
)



# ─── Navbar horizontal ─────────────────────────────────────────────────────────
selecionado = option_menu(
    menu_title=None,
    options=["Por Setor", "Por Município", "Sobre"],
    icons=["bar-chart", "map", "info-circle"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "0!important",
            "background-color": "#4169E1",
            "width": "100%"
        },
        "nav-link": {
            "font-size": "16px",
            "text-align": "center",
            "margin": "0px 20px",
            "color": "white",
        },
        "nav-link-selected": {
            "background-color": "#365BB5"
        },
    }
)

# ─── Função de extração de competência do notebook ─────────────────────────────
def extrair_competencia(notebook_path):
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        for output in cell.get("outputs", []):
            text = ""
            if output.get("output_type") == "stream" and output.get("name") == "stdout":
                text = output.get("text", "")
            elif output.get("output_type") == "execute_result":
                data = output.get("data", {})
                text = data.get("text/plain", "")
            match = re.search(r"[Cc]ompet[êe]ncia:\s*['\"]?(\d{6})['\"]?", text)
            if match:
                return match.group(1)
    return None

# 🎯 Setores disponíveis
setores = ['Comércio', 'Serviços', 'Agropecuária', 'Construção', 'Indústria']

# 🎯 Municípios disponíveis
municipios = [
    'Acari', 'Açu', 'Afonso Bezerra', 'Água Nova', 'Alexandria', 'Almino Afonso',
    'Alto Do Rodrigues', 'Antônio Martins', 'Apodi', 'Arês', 'Areia Branca',
    'Augusto Severo', 'Baía Formosa', 'Barcelona', 'Baraúna', 'Bento Fernandes',
    'Bodó', 'Bom Jesus', 'Brejinho', 'Caiçara Do Norte', 'Caiçara Do Rio Do Vento',
    'Caicó', 'Campo Redondo', 'Carnaubais', 'Carnaúba Dos Dantas', 'Ceará-Mirim',
    'Cerro Corá', 'Coronel Ezequiel', 'Coronel João Pessoa', 'Cruzeta',
    'Canguaretama', 'Doutor Severiano', 'Encanto', 'Equador', 'Espírito Santo',
    'Extremoz', 'Felipe Guerra', 'Fernando Pedroza', 'Florânia', 'Francisco Dantas',
    'Frutuoso Gomes', 'Galinhos', 'Goianinha', 'Governador Dix-Sept Rosado',
    'Grossos', 'Guamaré', 'Ielmo Marinho', 'Ipanguaçu', 'Ipueira', 'Itaú',
    'Itajá', 'Jaçanã', 'Jandaíra', 'Janduís', 'Japi', 'Jardim De Angicos',
    'Jardim De Piranhas', 'Jardim Do Seridó', 'João Câmara', 'João Dias',
    'José Da Penha', 'Jucurutu', 'Jundiá', "Lagoa D'anta", 'Lagoa De Pedras',
    'Lagoa De Velhos', 'Lagoa Nova', 'Lagoa Salgada', 'Lajes', 'Lajes Pintadas',
    'Lucrécia', 'Luís Gomes', 'Macau', 'Macaíba', 'Major Sales', 'Marcelino Vieira',
    'Martins', 'Maxaranguape', 'Messias Targino', 'Monte Alegre',
    'Monte Das Gameleiras', 'Montanhas', 'Mossoró', 'Natal', 'Nova Cruz',
    'Nísia Floresta', "Olho-D'água Do Borges", 'Ouro Branco', 'Paraná', 'Paraú',
    'Parazinho', 'Parnamirim', 'Passa E Fica', 'Passagem', 'Patu', 'Parelhas',
    'Pedro Avelino', 'Pedro Velho', 'Pendências', 'Pilões', 'Poço Branco',
    'Portalegre', 'Porto Do Mangue', 'Pureza', 'Rafael Fernandes', 'Rafael Godeiro',
    'Riacho Da Cruz', 'Riacho De Santana', 'Riachuelo', 'Rio Do Fogo',
    'Rodolfo Fernandes', 'Ruy Barbosa', 'Santana Do Matos', 'Santana Do Seridó',
    'Santa Cruz', 'Santa Maria', 'São Bento Do Norte', 'São Bento Do Trairí',
    'São Fernando', 'São Francisco Do Oeste', 'São Gonçalo Do Amarante',
    'São João Do Sabugi', 'São José De Mipibu', 'São José Do Campestre',
    'São José Do Seridó', 'São Miguel', 'São Miguel Do Gostoso',
    'São Paulo Do Potengi', 'São Pedro', 'São Rafael', 'São Tomé', 'São Vicente',
    'Senador Elói De Souza', 'Senador Georgino Avelino', 'Serra De São Bento',
    'Serra Do Mel', 'Serra Negra Do Norte', 'Serrinha', 'Serrinha Dos Pintos',
    'Severiano Melo', 'Sítio Novo', 'Taboleiro Grande', 'Taipu', 'Tangará',
    'Tenente Ananias', 'Tenente Laurentino Cruz', 'Tibau', 'Tibau Do Sul',
    'Timbaúba Dos Batistas', 'Touros', 'Triunfo Potiguar', 'Umarizal', 'Upanema',
    'Várzea', 'Vera Cruz', 'Venha-Ver', 'Viçosa', 'Vila Flor'
]

# ─── Página “Por Setor” ────────────────────────────────────────────────────────
if selecionado == "Por Setor":
    st.title("Gerador de Boletim de Emprego")
    st.subheader("Rio Grande do Norte")

    setor = st.radio("Escolha o setor:", setores)

    NOTEBOOK_PATH = "Generate_Boletim_Emprego-SETOR.ipynb"
    OUTPUT_NOTEBOOK = NOTEBOOK_PATH

    if st.button("Gerar PDF"):
        with st.spinner(f'Gerando boletim para o setor {setor}...'):
            os.makedirs("output", exist_ok=True)
            pm.execute_notebook(
                NOTEBOOK_PATH,
                OUTPUT_NOTEBOOK,
                parameters = {"setor": normalizar_string(setor)}
            )
        st.success("Boletim por setor gerado com sucesso!")

        competencia = extrair_competencia(OUTPUT_NOTEBOOK)
        if competencia:
            PDF_PATH = f"pdfs/boletim_emprego_{competencia}-{setor}.pdf"
            if os.path.exists(PDF_PATH):
                with open(PDF_PATH, "rb") as file:
                    st.download_button(
                        label="Baixar PDF - Setor",
                        data=file,
                        file_name=os.path.basename(PDF_PATH),
                        mime="application/pdf"
                    )
            else:
                st.error(f"PDF '{PDF_PATH}' não encontrado.")
        else:
            st.error("Não foi possível extrair a competência do notebook.")

# ─── Página “Por Município” ────────────────────────────────────────────────────
elif selecionado == "Por Município":
    st.title("Gerador de Boletim de Emprego")
    st.subheader("Rio Grande do Norte")

    municipio = st.selectbox("Escolha o município:", municipios)

    NOTEBOOK_PATH_MUN = "Generate_Boletim_Emprego-MUN.ipynb"
    OUTPUT_NOTEBOOK_MUN = NOTEBOOK_PATH_MUN

    if st.button("Gerar PDF"):
        with st.spinner(f'Gerando boletim para o município {municipio}...'):
            os.makedirs("output", exist_ok=True)
            pm.execute_notebook(
                NOTEBOOK_PATH_MUN,
                OUTPUT_NOTEBOOK_MUN,
                parameters=dict(municipio=municipio)
            )
        st.success("Boletim por município gerado com sucesso!")

        competencia = extrair_competencia(OUTPUT_NOTEBOOK_MUN)
        if competencia:
            safe_mun = municipio.replace(" ", "_").replace("'", "")
            PDF_PATH = f"pdfs/boletim_emprego_{competencia}-{safe_mun}.pdf"
            if os.path.exists(PDF_PATH):
                with open(PDF_PATH, "rb") as file:
                    st.download_button(
                        label="Baixar PDF - Município",
                        data=file,
                        file_name=os.path.basename(PDF_PATH),
                        mime="application/pdf"
                    )
            else:
                st.error(f"PDF '{PDF_PATH}' não encontrado.")
        else:
            st.error("Não foi possível extrair a competência do notebook.")

# ─── Página “Sobre” ────────────────────────────────────────────────────────────
else:
    st.title("Sobre")
    st.markdown(
        """
        Os dados são referentes ao estado do **Rio Grande do Norte**, 
        com base no **Novo CAGED** (Ministério do Trabalho e Emprego).
        """
    )
