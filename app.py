import streamlit as st
from dotenv import load_dotenv

from streamlit_extras.add_vertical_space import add_vertical_space

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
    st.write("Hello")
    pdf = st.file_uploader("Upload your PDF file", type='pdf')


if __name__ == '__main__':
    main()
