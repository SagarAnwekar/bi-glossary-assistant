import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from unittest.mock import patch
import rag

def test_docs_load_and_have_sources():
    d = rag.load_docs()
    assert len(d) >= 10 and all(x.metadata["source"] for x in d)

def test_answer_uses_retrieved_sources():
    class H:  # fake retrieval hit
        def __init__(s, n): s.page_content = n; s.metadata = {"source": n}
    class Store:
        def similarity_search(s, q, k=3): return [H("dso"), H("cac")]
    with patch.object(rag, "ask_llm", return_value="stub") as m:
        a, src = rag.answer(Store(), "q")
    assert a == "stub" and src == ["dso", "cac"] and m.called
