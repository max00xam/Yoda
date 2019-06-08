#!/usr/bin/env python3

"""
'voglio andare a mangiare'
[aux] [ROOT] [mark, xcomp] --> [mark, xcomp] [ROOT] [', io '] [aux]
[a mangiare] [andare] [', io '] [voglio]

'oggi non so cosa fare'
[advmod, advmod, ROOT] [obj, ccomp]  --> [obj, ccomp] [', io '] [advmod, advmod, ROOT]
[cosa fare] [', io '] [oggi non so]

'Claudia ha mangiato un gelato alla fragola.')
[nsubj, aux] [ROOT] [det, obj, amod, nmod]  -->  [det, obj, amod, nmod] [', '] [ROOT] [nsubj, aux]
[un gelato alla fragola] [', '] [mangiato] [Claudia ha]

Il vento scuote i rami degli alberi
[det, nsubj, ROOT] [det, obj, det, obj] --> [det, obj, det, obj] [', '] [det, nsubj, ROOT]
[i rami degli alberi] [', '] [il vento scuote]

'Alessandro è uscito di casa con il papà'
[nsubj, aux] [ROOT] [case, obl] [case, det, obl] --> [case, det, obl] [case, obl] [ROOT] [', '] [nsubj, aux]
[con il papà] [di casa] [uscito] [', '] [Alessandro è]

'Marta ha invitato Ludovico alla sua festa di compleanno'
[nsubj, aux] [ROOT, obj] [flat:name, det:poss, nmod, case, nmod] --> [obj, flat:name, det:poss, nmod, case, nmod] [ROOT] [', '] [nsubj, aux]
[Ludovico alla sua festa di compleanno] [invitato] [', '] [Marta ha]

1. spezza la frase nelle sottoliste
2. aggiungere se serve il soggetto e la virgola
3. [::-1]

            [aux]           [ROOT]  [mark, xcomp]
            [advmod, advmod, ROOT]  [obj, ccomp]
            [nsubj, aux]    [ROOT]  [det, obj, amod, nmod]
            [det, nsubj      ROOT]  [det, obj, det, obj]
            [nsubj, aux]    [ROOT]  [case, obl] [case, det, obl]
            [nsubj, aux]    [ROOT]  [obj, flat:name, det:poss, nmod, case, nmod]


      ['aux'],             'ROOT',  ['mark', 'xcomp', 'punct']
      ['advmod', 'advmod', 'ROOT'], ['obj', 'ccomp', 'punct']
      ['nsubj', 'aux'],    'ROOT',  ['det', 'obj', 'amod', 'nmod', 'punct']
          ['det', 'nsubj', 'ROOT'], ['det', 'obj', 'det', 'obj', 'punct']
      ['nsubj', 'aux'],    'ROOT',  ['case', 'obl', 'case', 'det', 'nmod', 'punct']
      ['nsubj', 'aux'],    'ROOT',  ['obj', 'flat:name', 'det:poss', 'nmod', 'case', 'nmod', 'punct']

partire da ROOT
se prima di ROOT ci sono *mod aggiungerli al gruppo di ROOT
se c'é un det prima di *mod aggiungerlo al gruppo di ROOT
se dopo di ROOT c'é un obj che non ha subito dopo un ?comp aggiungerlo al gruppo di ROOT
prendere tutto quello che resta e che precede ROOT e creare un gruppo
di quello che resta dopo ROOT raggruppare case fino al obl successivo
"""

import spacy
import sys

texts = [
    "La capacità di parlare non fa di te un essere intelligente.",
    "Navigare nell'iperspazio non è come spargere fertilizzante da un aeroplano.",
    "imperatore ti stava aspettando...",
    "Lo so, padre.",
    "Allora... hai accettato la verità?!",
    "Ho accettato la verità che tu una volta eri Anakin Skywalker, mio padre!",
    "Quel nome non ha più alcun significato per me!",
    "Quello è il nome del tuo vero io... lo hai solo dimenticato... so che c'è del buono in te, l'imperatore non è riuscito del tutto a privartene!",
    "È così che muore la libertà. Sotto scroscianti applausi.",
    "La paura è la via per il lato oscuro. La paura porta alla rabbia, la rabbia porta all'odio, l'odio alla sofferenza.",
    "Che la forza sia con te!",
    "L'attaccamento è proibito. Il possesso è proibito. La compassione, che io definirei amore assoluto, illimitato, è al centro della vita di un Jedi. E quindi si può dire che noi siamo spronati ad amare.",
    "La vita sembra più facile quando riesci ad aggiustare qualcosa.",
    "Ho sempre odiato vederti partire!",
    "Per questo lo facevo, così ti mancavo un po'!",
    "Senti, altezza serenissima, mettiamo in chiaro una cosa, io gli ordini li prendo da una sola persona: da me!",
]

def _(nlp, text):
    doc = nlp(text)
    res = []
    for sent in doc.sents:
        for clause in sent:
            res.append({
                'text': clause.text,
                'ancestors': [a.text for a in clause.ancestors],
                'children': [a.text for a in clause.children],
                'dep': clause.dep_,
                'left_edge': clause.left_edge.text,
                'lefts': [a.text for a in clause.lefts],
                'n_lefts': clause.n_lefts,
                'right_edge': clause.right_edge.text,
                'rights': [a.text for a in clause.rights],
                'n_rights': clause.n_rights,
                'pos': clause.pos_,
                'subtree': [a.text for a in clause.subtree],
                'tag': clause.tag_
                })
    return res

def __(nlp, text):
    doc = nlp(text)
    res = []
    tmp = []
    for sent in doc.sents:
        idx = 0
        for clause in sent:
            if clause.dep_ == 'ROOT':
                if 'aux' in tmp:
                    res.append(tmp) 
                    tmp.append([clause.dep_, clause.text])
                    res.append([[c.dep_, c.text] for c in sent[idx+1:]])
                else:
                    tmp.append([clause.dep_, clause.text])
                    res.append(tmp)
                    res.append([[c.dep_, c.text] for c in sent[idx+1:]])
                break
            else:
                tmp.append([clause.dep_, clause.text])

            idx += 1
    return res

def yoda_say(text):
    out_text = [[a[1] for a in text] for text in __(nlp, text)][::-1]    
    out_dep_ = [[a[0] for a in text] for text in __(nlp, text)][::-1]
    if out_dep_[-1][-2:] == ['aux', 'ROOT']:
        out_text[-1] = out_text[-1][:-2] + out_text[-1][-2:][::-1]
        out_dep_[-1] = out_dep_[-1][:-2] + out_dep_[-1][-2:][::-1]
    
    if out_dep_[-1] == ['ROOT', 'aux']:
        out_text[0] = [a for a in out_text[0] if a != '.']
        out_text[-1] = out_text[-1][:-2] + [out_text[-1][0], ', io', out_text[-1][1]]        
    
    if out_dep_[-1][-3:] == ['advmod', 'advmod']:
        out_text[0] = [a for a in out_text[0] if a != '.']
        out_text[-1] = out_text[-1][:-2] + [', io', out_text[-1][-3], out_text[-1][-2]]
    
    return ' '.join([' '.join(ot) for ot in out_text]).replace(' ,', ',').replace(' .', ',')

nlp = spacy.load("it")    
sents = []
if len(sys.argv) > 1:
    print(yoda_say(' '.join(sys.argv[1:])))
else:    
    for t in texts:
        # print(t[1])
        print(yoda_say(t))
        print('------------------------------------------------------------------------------------------------------')
        # print ([ot for ot in out_dep_])
        # print()

