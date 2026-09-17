# Tarynea Aggarwal — OIM 3641 Classwork

This is where I'm keeping my work for **OIM 3641** at Babson College — in-class demos, problem sets, and whatever project work comes out of the semester.

## About Me

Hi, I'm Tarynea! I'm an undergrad at Babson finishing up a B.S. in Business with a concentration in **Tech Entrepreneurship and Data Analytics** (expected Dec 2026). I've spent most of my internships and coursework in analytics and strategy — Power BI dashboards, SQL, SAP, market research — and this class is my first real hands-on dive into building with LLM APIs, so expect this repo to get more interesting (and probably messier) as the term goes on.

## Skills & Tools

**Languages**

1. Python 
2. SQL
3. Markdown

**Libraries & Frameworks**

1. Python Dotenv 
2. Google Gemini API
3. Llama Index
4. Pandas 
5. Jupyter 


**Analytics & Business Tools**

1.Excel 
2. Power BI
3. SAP
4. Minitab

**Dev Tools**

1. Git 
2. GitHub
3. GitHub Desktop 
4. VS Code

## Directory Structure

```
OIM3641_F26/
├── data/                                  # Datasets and reference files used in demos/exercises
├── .gitignore                             # Keeps .env, .venv, and other local files out of the repo
├── 01-llm-call.py                         # Basic LLM API call example (Gemini)
├── 02-python_concepts.ipynb               # Python fundamentals exercises
├── 02-python_concepts_ans.ipynb           # Answer key / worked solutions
├── 03-demo_create_llamaindex.py           # Building a LlamaIndex from parsed documents
├── 03-demo_llama_gemini_retrieval.py      # RAG retrieval using LlamaIndex + Gemini
├── 03-demo_llama_retrieval.py             # RAG retrieval using LlamaIndex
├── loan_pmt.py                            # Loan payment calculator exercise
└── README.md                              # This file
```

Files are numbered by lesson (`01-`, `02-`, `03-`...) so it's easy to tell what week something came from. New problem sets and project milestones will get added the same way as the semester goes on.

## Install Instructions

Want to run any of this yourself? Here's how.

**1. Clone the repository**

```bash
git clone https://github.com/<your-username>/OIM3641_F26.git
cd OIM3641_F26
```

**2. Set up a virtual environment (recommended)**

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

**3. Install dependencies**

```bash
pip install python-dotenv google-genai llama-index llama-cloud-services pandas jupyter
```

**4. Add your API keys**

A few of the scripts hit external LLM APIs, so you'll need your own keys in a `.env` file in the project root (already excluded from tracking via `.gitignore`):

```
GEMINI_API_KEY=your_key_here
LLAMA_CLOUD_API_KEY=your_key_here
```

**5. Run a script or notebook**

```bash
python 01-llm-call.py
jupyter notebook 02-python_concepts.ipynb
```

## Let's Connect

Feel free to reach out — always happy to chat about class projects, internships, or anything analytics/AI related.

- **LinkedIn:** [linkedin.com/in/tarynea-aggarwal]
- **Email:** taggarwal2@babson.edu