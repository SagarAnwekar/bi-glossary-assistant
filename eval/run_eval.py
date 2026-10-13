import json, sys, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from rag import build_index, answer
cs = int(sys.argv[1]) if len(sys.argv) > 1 else 400
store, n = build_index(chunk_size=cs, chunk_overlap=cs // 8)
Q = json.load(open(pathlib.Path(__file__).with_name("questions.json")))
hit = ans = ref = 0; ansq = unq = 0; rows = []
for i, it in enumerate(Q):
    time.sleep(1)
    for attempt in range(4):
        try: a, src = answer(store, it["q"]); break
        except Exception as e: time.sleep(10 * (attempt + 1)); a, src = f"ERROR {e}", []
    if it["src"]:
        ansq += 1; h = it["src"] in src; k = all(w.lower() in a.lower() for w in it["kw"])
        hit += h; ans += k; rows.append((it["q"], h, k, a))
    else:
        unq += 1; r = "don't know" in a.lower(); ref += r; rows.append((it["q"], None, r, a))
res = {"chunk_size": cs, "chunks": n, "retrieval_hit@3": f"{hit}/{ansq}", "answer_keyword_match": f"{ans}/{ansq}", "correct_refusals": f"{ref}/{unq}"}
print(json.dumps(res))
out = pathlib.Path(__file__).resolve().parent.parent / "results"
json.dump({"summary": res, "rows": rows}, open(out / f"run_chunk{cs}.json", "w"), indent=1)
