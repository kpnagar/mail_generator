from langchain_core.exceptions import OutputParserException
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain_core.output_parsers import JsonOutputParser

llm = Ollama(model="llama3")


def extract_jobs(cleaned_text):
    json_prompt = PromptTemplate.from_template(
        """
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data}
        ### INSTRUCTION:
        The scraped text is from the career's page of a website.
        Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `techstack` and `description`.
        Only return the valid JSON.
        ### VALID JSON (NO PREAMBLE):
        """
    )
    json_parser = JsonOutputParser()
    json_chain = json_prompt | llm
    res = json_chain.invoke(input={"page_data": cleaned_text})
    try:
        res = json_parser.parse(res)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")
    return res if isinstance(res, list) else [res]


def write_mail(job, links):
    email_prompt = PromptTemplate.from_template(
        """
        ### JOB DESCRIPTION:
        {job_description}
        
        ### INSTRUCTION:
        You are Sid, a business development executive at MindInventory. MindInventory is a mindful team of tech innovators with over 13 years of experience in bringing world-class tech ideas to reality. We embrace the power of technology to provide cutting-edge digital solutions that propel our clients toward unprecedented success. Your job is to write a cold email to the client regarding the job mentioned above describing the capability of Mindinventory in fulfilling their needs.
        Also add the following links to showcase Mindinventory's portfolio: {link_list}
        Remember you are Sid, BDE at Mindinventory. Do not provide a preamble.
        ### EMAIL (NO PREAMBLE):
        
        """
    )
    email_chain = email_prompt | llm
    res = email_chain.invoke({"job_description": str(job), "link_list": links})
    return res
