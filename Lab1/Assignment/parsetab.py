
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'adj article noun verb verbca verbcb\n    calc : SENTENCE\n            | empty\n    \n    SENTENCE : NOUN VERB\n    \n    NOUN : ARTICLE noun\n    \n    NOUN : ADJECTIVE noun\n    \n    NOUN : ARTICLE ADJECTIVE noun\n    \n    NOUN : noun\n    \n    ARTICLE : article\n                \n    \n    VERB : NOUN VERB\n            | VERBC VERB\n    \n    VERB : verb\n            | VERBC\n    \n    VERBC : verbca verbcb\n    \n    ADJECTIVE : adj\n    \n    empty :\n    '
    
_lr_action_items = {'$end':([0,1,2,3,11,12,13,18,19,20,],[-15,0,-1,-2,-3,-12,-11,-9,-10,-13,]),'noun':([0,4,5,6,7,8,9,10,12,15,16,17,20,21,],[6,6,15,-7,17,-8,-14,6,6,-4,21,-5,-13,-6,]),'article':([0,4,6,10,12,15,17,20,21,],[8,8,-7,8,8,-4,-5,-13,-6,]),'adj':([0,4,5,6,8,10,12,15,17,20,21,],[9,9,9,-7,-8,9,9,-4,-5,-13,-6,]),'verb':([4,6,10,12,15,17,20,21,],[13,-7,13,13,-4,-5,-13,-6,]),'verbca':([4,6,10,12,15,17,20,21,],[14,-7,14,14,-4,-5,-13,-6,]),'verbcb':([14,],[20,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'calc':([0,],[1,]),'SENTENCE':([0,],[2,]),'empty':([0,],[3,]),'NOUN':([0,4,10,12,],[4,10,10,10,]),'ARTICLE':([0,4,10,12,],[5,5,5,5,]),'ADJECTIVE':([0,4,5,10,12,],[7,7,16,7,7,]),'VERB':([4,10,12,],[11,18,19,]),'VERBC':([4,10,12,],[12,12,12,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> calc","S'",1,None,None,None),
  ('calc -> SENTENCE','calc',1,'p_calc','23CS60R22_DesLab_T2.py',128),
  ('calc -> empty','calc',1,'p_calc','23CS60R22_DesLab_T2.py',129),
  ('SENTENCE -> NOUN VERB','SENTENCE',2,'p_sentence','23CS60R22_DesLab_T2.py',136),
  ('NOUN -> ARTICLE noun','NOUN',2,'p_article_noun','23CS60R22_DesLab_T2.py',143),
  ('NOUN -> ADJECTIVE noun','NOUN',2,'p_adjective_noun','23CS60R22_DesLab_T2.py',150),
  ('NOUN -> ARTICLE ADJECTIVE noun','NOUN',3,'p_article_adjective_noun','23CS60R22_DesLab_T2.py',157),
  ('NOUN -> noun','NOUN',1,'p_noun','23CS60R22_DesLab_T2.py',164),
  ('ARTICLE -> article','ARTICLE',1,'p_article','23CS60R22_DesLab_T2.py',171),
  ('VERB -> NOUN VERB','VERB',2,'p_verbb_noun','23CS60R22_DesLab_T2.py',179),
  ('VERB -> VERBC VERB','VERB',2,'p_verbb_noun','23CS60R22_DesLab_T2.py',180),
  ('VERB -> verb','VERB',1,'p_verb_one_symbol','23CS60R22_DesLab_T2.py',186),
  ('VERB -> VERBC','VERB',1,'p_verb_one_symbol','23CS60R22_DesLab_T2.py',187),
  ('VERBC -> verbca verbcb','VERBC',2,'p_verbc','23CS60R22_DesLab_T2.py',194),
  ('ADJECTIVE -> adj','ADJECTIVE',1,'p_adjective','23CS60R22_DesLab_T2.py',201),
  ('empty -> <empty>','empty',0,'p_empty','23CS60R22_DesLab_T2.py',207),
]