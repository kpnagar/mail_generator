import uuid
from typing import List, Optional
import streamlit as st
import pandas as pd

from data_loader import DataLoader, ChromaDBClient
from chains import extract_jobs, write_mail


class PortfolioData:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self) -> pd.DataFrame:
        return pd.read_csv(self.file_path, index_col=0).dropna()


class EmailGenerator:
    def __init__(self, chroma_client: ChromaDBClient, portfolio_data: PortfolioData):
        self.chroma_client = chroma_client
        self.portfolio_data = portfolio_data

    def generate_email(self, job: dict) -> str:
        skills = job.get('techstack', [])
        links = self.get_relevant_links(skills)
        return write_mail(job, links)

    def get_relevant_links(self, required_skills: List[str]) -> List[dict]:
        query_texts = required_skills if required_skills else ['Software']
        result = self.chroma_client.query(query_texts=query_texts, n_results=3)
        return result.get('metadatas', [])


def demo():
    demo_portfolio_file_path = "/home/mind/Documents/projects/mail_generator/mail_generator/cleaned_portfolio.csv"
    urls = ["https://www.mindinventory.com/careers.php"]

    demo_loader = DataLoader(urls=urls)
    demo_chroma_client = ChromaDBClient(path='vectorstore')

    demo_portfolio_data = PortfolioData(file_path=demo_portfolio_file_path)
    demo_email_generator = EmailGenerator(demo_chroma_client, demo_portfolio_data)

    demo_text_data = demo_loader.load_data()
    print(demo_text_data)
    demo_jobs = extract_jobs(demo_text_data)
    print(demo_jobs)

    demo_emails = []
    for demo_job in demo_jobs:
        demo_email = demo_email_generator.generate_email(demo_job)
        demo_emails.append(demo_email)
        print(demo_email)
    print(demo_emails)


if __name__ == '__main__':
    st.set_page_config(layout="wide", page_title="MailGen", page_icon="📨")
    portfolio_file_path = "cleaned_portfolio.csv"
    st.title("📨 MailGen")
    st.caption("Generated content may be inaccurate. User's discretion advised.")
    url_input = st.text_input("Enter a URL:", value="https://www.mindinventory.com/careers.php")
    submit_button = st.button("Submit")
    if submit_button:
        try:
            loader = DataLoader(urls=[url_input])
            chroma_client = ChromaDBClient(path='vectorstore')

            portfolio_data = PortfolioData(file_path=portfolio_file_path)
            email_generator = EmailGenerator(chroma_client, portfolio_data)

            text_data = loader.load_data()
            print(text_data)
            jobs = extract_jobs(text_data)
            print(jobs)
            emails = []
            for job in jobs:
                email = email_generator.generate_email(job)
                emails.append(email)
                st.code(email, language='markdown')
            print(emails)
        except Exception as e:
            st.error(f"Error: {e}")
