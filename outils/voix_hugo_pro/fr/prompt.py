import json,sys
B=json.load(open('/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/elfr/lots.json')); k=int(sys.argv[1])
def f(t):
    import re; t=re.sub(r'\s*,\s*(\.?)$', r'\1', t).strip()
    t=re.sub(r'\s*[\u3000-\u9fff\uff00-\uffef]+[\u3000-\u9fff\uff00-\uffef ]*','',t).strip()
    t=re.sub(r'\s*\bfam\.','',t).strip()
    return t if t[-1] in '.!?' else t+'.'
print('[slowly] '+' [pause] '.join(f(t) for t in B[k]))
