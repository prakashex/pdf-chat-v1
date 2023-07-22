import os
import pickle
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback

with st.sidebar:
    st.title("Pdf Chat 1.0")
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM model
 
    ''')
    add_vertical_space(5)
    st.write('Only for educational purposes')




load_dotenv()    


def main():

    pdf = st.file_uploader("Upload your PDF file", type='pdf')
    
    if pdf is not None:
            readPdf = PdfReader(pdf)
            # st.write(readPdf)
            # reading data from pdf 
            text = ""
            for page in readPdf.pages:
                 text += page.extract_text()

            text_splitter = RecursiveCharacterTextSplitter(
                 chunk_size=1000,
                 chunk_overlap=200,
                 length_function=len
            )

            text_chunks = text_splitter.split_text(text = text)
            # st.write(text_chunks)

            # creating embeddings of the text chunks
            embeddings = OpenAIEmbeddings()
            VectorStore = FAISS.from_texts(text_chunks, embedding=embeddings)
            pdf_name = pdf.name[:-4]
            # if the file the same name already exits then read it from the 
            # buffer
            if os.path.exists(f"{pdf_name}.pkl"):
                 with open(f"{pdf_name}.pkl","rb") as f:
                      VectorStore = pickle.load(f)
                #  st.write("embeddings loaded from the disk")
            # else compute the embeddings and write it to the buffer    
            else:
                 with open(f"{pdf_name}.pkl","wb") as f:
                     pickle.dump(VectorStore , f)
            # Accept user questions / Query

            query = st.text_input("Ask Questions about your PDF Document:")

            if query:
                 docs = VectorStore.similarity_search(query=query , k=3)
                 llm = OpenAI(model_name='gpt-3.5-turbo')
                 chain = load_qa_chain(llm = llm , chain_type="stuff")
                 with get_openai_callback() as cb:
                      response = chain.run(input_documents=docs , question=query)
                 st.write(response)
                 st.write(cb)


                 

            

                 
            
            



if __name__ == '__main__':
    main()
