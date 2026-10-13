# BI Glossary Assistant (RAG + LangChain)

Small retrieval-augmented Q&A over 10 own-written KPI definitions (gross margin, NRR, churn, DSO, EBITDA, CAC, LTV, YoY, working capital, SCD Type 2). No employer or client data. Built as a learning project.

**Stack:** LangChain, FAISS (local), Gemini embeddings (`gemini-embedding-001`) and chat (`gemini-3.1-flash-lite`), free tier. Key from env var `GOOGLE_API_KEY`.

## Run
```
pip install -r requirements.txt
export GOOGLE_API_KEY=...
python src/cli.py "How is CAC computed?"
python eval/run_eval.py 400      # chunk size 400
pytest -q tests                  # mocked, no API calls
```

## Eval (15 questions: 12 answerable, 3 unanswerable)
Metrics: retrieval hit@3 (expected doc in top 3), answer keyword match (expected terms present), correct refusal on unanswerable questions.

| Chunk size | Chunks | Retrieval hit@3 | Answer keyword match | Correct refusals |
|---|---|---|---|---|
| 400 | 10 | 12/12 | 12/12 | 3/3 |
| 150 | 39 | 12/12 | 12/12 | 3/3 |

## Honest limits
- Tiny corpus and short docs, so both settings score full marks. The eval cannot separate them. It is a smoke test, not a benchmark.
- Keyword match is a crude correctness proxy, with no human or LLM grading.
- Next step: more and longer docs, harder multi-doc questions, and a judged answer score.
