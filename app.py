## GEN AI Project : Summarize the Text From Website

## importing libraries
import validators
import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain

## Streamit web interface
st.set_page_config(page_title="LangChain: Summarize Text From Website", page_icon="🦜")
st.title("🦜 LangChain: Summarize Text From Website")
st.subheader('Summarize URL')


## Get groq api key and url
with st.sidebar:
    groq_api_key = st.text_input("Enter the Groq Api Key : ",type="password")

generic_url = st.text_input("URL",label_visibility="collapsed")

if not groq_api_key:
    st.warning("Please Enter Groq API Key")
    st.stop()

llm = ChatGroq(groq_api_key=groq_api_key,model="llama-3.1-8b-instant")

prompt_template = """
    Provide a summary of the following content in 300 words:
    Content:{text}
"""

prompt = PromptTemplate(input_variables=['text'],template=prompt_template)

if st.button("Summarize the Content "):
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please the provide the information to get started")
    elif not validators.url(generic_url):
        st.error("Please provide the correct URL")
    else:
        try:
            with st.spinner("Loading content..."):
                
                loader = UnstructuredURLLoader(
                    urls=[generic_url],
                    ssl_verify = True,
                    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
                )

                docs = loader.load()

                chain = load_summarize_chain(llm=llm,chain_type="stuff",prompt=prompt)

                output_summary = chain.run(docs)

                st.success(output_summary)
        
        except Exception as e:
            import traceback 
            st.error(f"Exception: {e}") 
            st.text(traceback.format_exc())