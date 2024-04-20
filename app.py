import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_doc(pdf_doc):
  """Loads the text content from the uploaded PDF file."""
  try:
    pdf_reader = PdfReader(pdf_doc)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
      page = pdf_reader.pages[page_num]
      text += page.extract_text()
    return text
  except Exception as e:
    st.error(f"Error loading PDF: {e}")
    return None

def answer_query(query, text):
  """Performs a basic text search within the document."""
  sentences = RecursiveCharacterTextSplitter().split(text)
  for sentence in sentences:
    if query.lower() in sentence.lower():
      return sentence  # Return the first matching sentence
  return "Sorry, I couldn't find an answer in the document."

st.title("ChatPDF (Lite)")
st.write("Upload a PDF File and then click on Load PDF File")
st.write("Once the document has been loaded you can begin chatting with the PDF =)")

uploaded_pdf = st.file_uploader("Load a pdf", type=['.pdf', '.docx'])

if uploaded_pdf is not None:
  if uploaded_pdf.type not in ['.pdf', '.docx']:
    st.error("Please upload a valid PDF file.")
  else:
    status = st.text_input("Status", "", key="status")
    text = load_doc(uploaded_pdf)
    if text is not None:
      status.value = "Document loaded successfully!"
    else:
      status.value = "Error loading document."

    query = st.text_input("type in your question")
    output = st.text_area("output", "", height=100)

    if st.button("submit"):
      if text is not None:
        output.value = answer_query(query, text)
      else:
        st.error("Please load a valid PDF document before asking questions.")
