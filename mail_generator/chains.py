from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain.output_parsers.json import SimpleJsonOutputParser

llm = Ollama(model="llama3")


def extract_jobs(cleaned_text):
    json_prompt = PromptTemplate.from_template(
        """
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data}
        ### INSTRUCTION:
        The scraped text is from the career's page of a website.
        Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, and `description`.
        Only return the valid JSON. No preamble.
        ### RESPONSE:
        """
    )
    json_parser = SimpleJsonOutputParser()
    json_chain = json_prompt | llm | json_parser
    res = json_chain.invoke(input={"page_data": cleaned_text})
    return res if isinstance(res, list) else [res]


def write_mail(job):
    email_prompt = PromptTemplate.from_template(
        """
        ### JOB DESCRIPTION:
        {job_description}
        
        ### INSTRUCTION:
        You are Sid, a business development executive at MindInventory. MindInventory is a mindful team of tech innovators bringing world-class tech ideas to reality. We embrace the power of technology to provide cutting-edge digital solutions that propel our clients toward unprecedented success. Your job is to write a cold email to the client regarding the job mentioned above describing the capability of Mindinventory in fulfilling their needs.
        No preamble.
        """
    )
    email_chain = email_prompt | llm
    res = email_chain.invoke({"job_description": str(job)})
    return res
