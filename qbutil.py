from distro_maker import cat_dict
from numpy.random import random as rand

def powermark(tossup_q):
    if '(*)' in tossup_q:
        return tossup_q
    #else, add in a random powermark
    markspot = .4*rand() + .3
    mark_ind = int(len(tossup_q) * markspot)
    next_space = tossup_q.find(' ', mark_ind)
    tossup_q = tossup_q[:next_space] + ' (*) ' +  tossup_q[next_space+1:]
    return tossup_q

def clean(violin):
    if '&'in violin:
            violin = violin[:violin.index('&')]
    violin = ''.join([i if ord(i) < 128 else ' ' for i in violin])
    return violin

def cat_postscript(cat):
    return f' |({cat_dict[cat]})|' if cat is not None else ' |()|'

class tossup:
    def __init__(self, n, q, a, cat):
        self.n = n
        self.q = powermark(clean(q))
        self.a = clean(a) + cat_postscript(cat)
    
    def to_json_dict(self):
        return {'number' : self.n,
                'question' : self.q,
                'answer' : self.a,
                'question_sanitized' : self.q,
                'answers_sanitized' : self.a}
        
class bonus:
    def __init__(self, li, p1, p2, p3, a1, a2, a3, cat):
        self.leadin = clean(li)
        self.part1 = clean(p1)
        self.part2 = clean(p2)
        self.part3 = clean(p3)
        self.ans1 = clean(a1)
        self.ans2 = clean(a2)
        self.ans3 = clean(a3) + cat_postscript(cat)
    
    def to_json_dict(self):
        return {'leadin' : self.leadin,
                'leadin_sanitized' : self.leadin,
                'answers' : [self.ans1, self.ans2, self.ans3],
                'answers_sanitized' : [self.ans1, self.ans2, self.ans3],
                'parts' : [self.part1, self.part2, self.part3],
                'parts_sanitized' : [self.part1, self.part2, self.part3],
                'values' : [10, 10, 10],
                'difficultyModifiers' : ['m', 'm', 'm']}    
    
class game:
    def __init__(self, tossups, bonuses):
        self.tossups = tossups
        self.bonuses = bonuses
    
    def to_json_dict(self):
        return {'tossups' : [tu.to_json_dict() for tu in self.tossups],
                'bonuses' : [bq.to_json_dict() for bq in self.bonuses]}