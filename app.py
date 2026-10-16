import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Analisador de Sentimentos Offline",
    page_icon="🤖",
    layout="centered"
)

def traduzir_para_ingles(texto: str) -> str:
    """
    Traduz o texto de entrada para o inglês usando o deep-translator.
    Caso ocorra algum erro, retorna o texto original.
    """
    try:
        # O deep-translator detecta automaticamente o idioma de origem e traduz para 'en'
        traducao = GoogleTranslator(source='auto', target='en').translate(texto)
        return traducao if traducao else texto
    except Exception as e:
        # Em caso de falha na tradução, segue com o texto original
        return texto

def analisar_sentimento(texto: str):
    """
    Realiza a análise de polaridade utilizando o TextBlob.
    Retorna a polaridade (-1.0 a 1.0) e a subjetividade (0.0 a 1.0).
    """
    # Traduz para o inglês para melhor precisão do TextBlob
    texto_traduzido = traduzir_para_ingles(texto)
    
    # Processa com TextBlob
    blob = TextBlob(texto_traduzido)
    polaridade = blob.sentiment.polarity
    subjetividade = blob.sentiment.subjectivity
    
    return polaridade, subjetividade

def classificar_polaridade(polaridade: float) -> tuple:
    """
    Classifica a polaridade numérica em Positivo, Negativo ou Neutro
    e define a cor/componente visual correspondente do Streamlit.
    """
    if polaridade > 0.05:
        return "Positivo", "success", "O sentimento predominante é positivo! 😊"
    elif polaridade < -0.05:
        return "Negativo", "error", "O sentimento predominante é negativo. 😔"
    else:
        return "Neutro", "warning", "O sentimento é neutro ou inconclusivo. 😐"

def main():
    # Cabeçalho da aplicação
    st.title("📊 Analisador de Sentimentos Offline")
    st.markdown(
        "Esta é uma versão **Offline** desenvolvida com bibliotecas tradicionais de Python "
        "(`TextBlob` e `deep-translator`). Nenhuma API externa (como OpenAI ou Google Cloud) é utilizada."
    )
    st.divider()

    # Área de entrada de texto
    st.subheader("Insira o texto para análise")
    texto_usuario = st.text_area(
        "Digite ou cole sua frase, comentário ou review abaixo:",
        placeholder="Ex: Eu adorei este aplicativo, ele é simplesmente fantástico e muito útil!",
        height=150
    )

    # Botão de análise
    if st.button("Analisar Sentimento", type="primary"):
        if not texto_usuario.strip():
            st.warning("⚠️ Por favor, digite algum texto antes de clicar em analisar.")
            return

        with st.spinner("Analisando sentimento..."):
            # Realiza a análise
            polaridade, subjetividade = analisar_sentimento(texto_usuario)
            classificacao, tipo_alerta, mensagem = classificar_polaridade(polaridade)

        # Exibição dos resultados
        st.subheader("Resultado da Análise")
        
        # Exibe o alerta visual baseado no sentimento
        if tipo_alerta == "success":
            st.success(f"**Classificação: {classificacao}**\n\n{mensagem}")
        elif tipo_alerta == "error":
            st.error(f"**Classificação: {classificacao}**\n\n{mensagem}")
        else:
            st.warning(f"**Classificação: {classificacao}**\n\n{mensagem}")

        # Métricas detalhadas
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Polaridade (-1 a 1)", value=f"{polaridade:.2f}")
            st.caption("Valores próximos de 1 são positivos, e de -1 são negativos.")
        with col2:
            st.metric(label="Subjetividade (0 a 1)", value=f"{subjetividade:.2f}")
            st.caption("0 = Fatos/Objetivo | 1 = Opinião/Subjetivo.")

if __name__ == "__main__":
    main()
