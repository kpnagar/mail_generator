import uuid
from typing import List

import streamlit as st

from chains import extract_jobs, write_mail
from data_loader import DataLoader, ChromaDBClient, PortfolioData


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
    demo_portfolio_file_path = "cleaned_portfolio.csv"
    urls = ["https://www.mindinventory.com/careers.php"]

    demo_loader = DataLoader(urls=urls)
    demo_chroma_client = ChromaDBClient(path='vectorstore')

    demo_portfolio_data = PortfolioData(file_path=demo_portfolio_file_path)

    if not demo_chroma_client.get_collection().count():
        for _, demo_row in demo_portfolio_data.data.iterrows():
            demo_chroma_client.get_collection().add(documents=demo_row["Technology Platform"],
                                                    metadatas={"links": demo_row["Link"]},
                                                    ids=[str(uuid.uuid4())])
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
    st.set_page_config(layout="wide", page_title="Cold Emailer", page_icon="📨")
    portfolio_file_path = "cleaned_portfolio.csv"
    st.title("📨 Cold Emailer")
    st.caption("Generated content may be inaccurate. User's discretion advised.")
    url_input = st.text_input("Enter a URL:", value="https://www.mindinventory.com/careers.php")
    submit_button = st.button("Submit")
    if submit_button:
        try:
            loader = DataLoader(urls=[url_input])
            chroma_client = ChromaDBClient(path='vectorstore')

            portfolio_data = PortfolioData(file_path=portfolio_file_path)

            if not chroma_client.get_collection().count():
                for _, row in portfolio_data.data.iterrows():
                    chroma_client.get_collection().add(documents=row["Technology Platform"],
                                                       metadatas={"links": row["Link"]},
                                                       ids=[str(uuid.uuid4())])

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
