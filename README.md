# LinkedIn Icebreaker Bot

An AI-powered tool that generates personalized icebreakers and conversation starters based on LinkedIn profiles, built with IBM watsonx.ai and LlamaIndex as a hands-on RAG (Retrieval-Augmented Generation) project.

## Project Overview

Imagine you're heading to a networking event and want to open with something better than "So, what do you do?" This bot does the research for you: give it a LinkedIn profile (or use the built-in mock data), and within seconds it generates personalized icebreakers based on that person's career highlights, skills, and background — then lets you ask follow-up questions about the profile.

## Features

- Extract LinkedIn-style profile data via [LinkdAPI](https://linkdapi.com) or built-in mock data (no API key needed for testing)
- Chunk and index profile data using LlamaIndex, embedded with IBM watsonx embeddings
- Generate interesting facts about a person's career or education using a RAG pipeline
- Answer follow-up questions about the profile, grounded in the retrieved context
- Two interfaces: a command-line tool and a Gradio web UI

## Project Structure

```
icebreaker_bot/
├── requirements.txt           # Dependencies
├── config.py                  # Configuration settings
├── modules/
│   ├── __init__.py
│   ├── data_extraction.py     # LinkedIn profile data extraction (LinkdAPI or mock data)
│   ├── data_processing.py     # Chunking and vector indexing
│   ├── llm_interface.py       # watsonx LLM and embedding setup
│   └── query_engine.py        # Query processing and response generation
├── app.py                     # Gradio web interface
└── main.py                    # CLI entry point
```

## Getting Started

### Prerequisites

- Python 3.11+
- An IBM watsonx.ai account and project ID
- A [LinkdAPI](https://linkdapi.com) key (optional — mock data works out of the box without one)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/axer99/ai-icebreaker-bot.git
cd ai-icebreaker-bot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set your credentials as environment variables:
```bash
export WATSONX_PROJECT_ID="your_watsonx_project_id"
export LINKDAPI_API_KEY="your_linkdapi_key"  # optional, only needed for live profile lookups
```

### Usage

#### Command Line Interface

```bash
python main.py --mock  # Use mock data
# OR
python main.py --url "https://www.linkedin.com/in/username/" --api-key "your-linkdapi-key"
```

#### Web Interface

```bash
python app.py
```

Then open your browser to the URL shown in the terminal (typically `http://127.0.0.1:7860`).

## How It Works

This is a small end-to-end RAG pipeline:

1. **Extract** — pull profile data (mock or live via LinkdAPI)
2. **Chunk** — split the profile JSON into smaller nodes with LlamaIndex's `SentenceSplitter`
3. **Embed & store** — embed each chunk with an IBM watsonx embedding model and index it in a `VectorStoreIndex`
4. **Retrieve & generate** — for each question, retrieve the most relevant chunks and pass them to a watsonx LLM (Granite by default) to generate a grounded answer

## Notes

- The mock data option uses a sample LinkedIn-style profile, so you can try the whole pipeline without any API key.
- LinkdAPI is used here as the live data source (LinkedIn's original scraping API this project used, ProxyCurl, was discontinued in 2025). If you swap in a different provider, the only file you need to touch is `modules/data_extraction.py`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- IBM watsonx.ai for the LLM and embedding models
- LlamaIndex for the data indexing and retrieval framework
- LinkdAPI for LinkedIn profile data extraction
