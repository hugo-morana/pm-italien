import json,sys,re
L=sys.argv[1]; k=int(sys.argv[2])
B=json.load(open(f'/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/slots/aud_{L}/lots.json'))
def f(t):
    t=re.sub(r'\s*,\s*(\.?)$', r'\1', t).strip()
    return t if t[-1] in '.!?' else t+'.'
print('[slowly] '+' [pause] '.join(f(t) for t in B[k]))
