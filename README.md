# 📨 Cold Emailer

---
The following application uses Ollama as the interface to communicate with a local llm and help's the user generate email as MindInventory's sales representative.

### Set-up

**1. Set-up Ollama:**

You can download and install Ollama from [here](https://ollama.com/download). Once you have installed Ollama, run the following command:
```commandline
ollama run llama3
```
This will download the Llama3 model and spin up an inference server for it.

**2. Application Set-up:**

This application uses poetry for dependency management. To install `poetry` run the following command:
```commandline
pip install poetry
```

Now `cd` into the `mail_generator/mail_generator` and run the following command:
```commandline
poetry shell
```
```commandline
poetry install
```

**3. Start The Application:**

Run the following command to start the application:
```commandline
streamlit run main.py
```