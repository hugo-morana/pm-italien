import json,sys
B=json.load(open('/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/el/lots.json')); k=int(sys.argv[1])
print('[slowly] '+' [pause] '.join(t if t[-1] in '.!?' else t+'.' for t in B[k]))
