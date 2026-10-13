import sys
from rag import build_index, answer
store, n = build_index()
q = " ".join(sys.argv[1:]) or input("Question: ")
a, src = answer(store, q)
print(a, "\nSources:", ", ".join(dict.fromkeys(src)))
