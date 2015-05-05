import re, random

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto + w > r:
         return {'craft':c, 'pages':w}
      upto += w
   assert False, "Shouldn't get here"
