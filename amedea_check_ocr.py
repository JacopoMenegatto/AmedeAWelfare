
import streamlit as st
import fitz  # PyMuPDF

def estrai_testo_pdf(file):
    with fitz.open(stream= file.read(), filetype="pdf") as doc:
        testo = ""
        for page in doc:
            testo += page.get_text()
    return testo.lower()

st.set_page_config(page_title="Amedea Check – OCR PDF", layout="centered")

st.image("https://i.imgur.com/jg7P3fG.png", width=150)
st.title("Amedea Check – Validazione Pratica con Controllo PDF")
st.write("Il sistema legge il contenuto dei documenti PDF per verificare se i nomi sono presenti.")

st.markdown("## 📋 Dati dipendente (intestatario piano welfare)")
nome_dip = st.text_input("Nome dipendente")
cognome_dip = st.text_input("Cognome dipendente")

st.markdown("## 👤 Dati beneficiario")
nome_ben = st.text_input("Nome beneficiario")
cognome_ben = st.text_input("Cognome beneficiario")

st.markdown("## 📄 Dettagli della pratica")
causale = st.selectbox("Causale", ["Retta scolastica", "Trasporto pubblico", "Baby sitting", "Utenze domestiche"])
pagamento = st.selectbox("Metodo di pagamento", ["Bonifico", "Carta", "POS", "Contanti"])
data_fattura = st.date_input("Data fattura")
data_pagamento = st.date_input("Data pagamento")
anno_portale = st.selectbox("Anno selezionato nel portale", ["2024", "2025"])

st.markdown("## 📎 Carica i documenti PDF")
fattura = st.file_uploader("Fattura (PDF)", type="pdf")
ricevuta = st.file_uploader("Ricevuta di pagamento (PDF)", type="pdf")

if st.button("✅ Valuta pratica"):
    if not fattura or not ricevuta:
        st.warning("⚠️ Carica tutti i documenti richiesti prima di inviare.")
    elif nome_dip.strip() == "" or cognome_dip.strip() == "" or nome_ben.strip() == "" or cognome_ben.strip() == "":
        st.warning("⚠️ Inserisci nome e cognome sia del dipendente che del beneficiario.")
    else:
        testo_fattura = estrai_testo_pdf(fattura)
        testo_ricevuta = estrai_testo_pdf(ricevuta)
        if nome_ben.lower() not in testo_fattura and cognome_ben.lower() not in testo_fattura:
            st.warning("🟡 Da integrare")
            st.write("Motivazione: Il nome del beneficiario non è presente nel contenuto della fattura.")
        elif nome_dip.lower() not in testo_ricevuta and cognome_dip.lower() not in testo_ricevuta:
            st.warning("🟡 Da integrare")
            st.write("Motivazione: Il nome del dipendente non risulta nel contenuto della ricevuta. Verificare che il pagamento sia intestato correttamente.")
        else:
            if data_pagamento.month >= 10 and anno_portale == "2025":
                st.success("✅ Accettata")
                st.write("Motivazione: Tutti i dati e documenti sono coerenti e leggibili.")
            else:
                st.warning("🟡 Da integrare")
                st.write("Motivazione: La data di pagamento non è coerente con l’anno fiscale selezionato.")
