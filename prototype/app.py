"""Try one ticket: python prototype/app.py "Como exporto as notas da turma para Excel?" """
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pipeline

text = " ".join(sys.argv[1:]) or "How do I resubmit my assignment?"
o = pipeline.run_one(text)
print(f"language  {o['language']} ({o['lang_conf']:.2f})   category {o['category']} ({o['cat_conf']:.2f})")
print(f"decision  {o['decision']}  {o['reason']}   send: {o['send']}")
print(f"sources   {'; '.join(o['citations']) or '—'}")
print(f"draft     {o['draft']}")
