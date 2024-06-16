
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftPLUSMINUSleftMULTIPLYDIVIDEMODULUSleftPOWERleftDOUBLE_EQUALSDIVIDE DOUBLE_EQUALS EQUALS FLOAT INT LPAREN MINUS MODULUS MULTIPLY NAME PLUS POWER RPAREN\n    calc : expression\n         | var_assign\n         | empty\n    \n    var_assign : NAME EQUALS expression\n    \n    expression : LPAREN expression RPAREN\n    \n    expression : expression MULTIPLY expression\n               | expression DIVIDE expression\n               | expression MODULUS expression\n               | expression POWER expression\n               | expression PLUS expression\n               | expression MINUS expression\n               | expression DOUBLE_EQUALS expression\n    \n    expression : MINUS expression\n    \n    expression : INT\n               | FLOAT\n    \n    expression : NAME\n    \n    empty :\n    '
    
_lr_action_items = {'LPAREN':([0,5,6,10,11,12,13,14,15,16,20,],[5,5,5,5,5,5,5,5,5,5,5,]),'MINUS':([0,2,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,],[6,15,6,6,-14,-15,-16,6,6,6,6,6,6,6,15,-16,-13,6,-6,-7,-8,-9,-10,-11,-12,-5,15,]),'INT':([0,5,6,10,11,12,13,14,15,16,20,],[7,7,7,7,7,7,7,7,7,7,7,]),'FLOAT':([0,5,6,10,11,12,13,14,15,16,20,],[8,8,8,8,8,8,8,8,8,8,8,]),'NAME':([0,5,6,10,11,12,13,14,15,16,20,],[9,18,18,18,18,18,18,18,18,18,18,]),'$end':([0,1,2,3,4,7,8,9,18,19,21,22,23,24,25,26,27,28,29,],[-17,0,-1,-2,-3,-14,-15,-16,-16,-13,-6,-7,-8,-9,-10,-11,-12,-5,-4,]),'MULTIPLY':([2,7,8,9,17,18,19,21,22,23,24,25,26,27,28,29,],[10,-14,-15,-16,10,-16,10,-6,-7,-8,-9,10,10,-12,-5,10,]),'DIVIDE':([2,7,8,9,17,18,19,21,22,23,24,25,26,27,28,29,],[11,-14,-15,-16,11,-16,11,-6,-7,-8,-9,11,11,-12,-5,11,]),'MODULUS':([2,7,8,9,17,18,19,21,22,23,24,25,26,27,28,29,],[12,-14,-15,-16,12,-16,12,-6,-7,-8,-9,12,12,-12,-5,12,]),'POWER':([2,7,8,9,17,18,19,21,22,23,24,25,26,27,28,29,],[13,-14,-15,-16,13,-16,13,13,13,13,-9,13,13,-12,-5,13,]),'PLUS':([2,7,8,9,17,18,19,21,22,23,24,25,26,27,28,29,],[14,-14,-15,-16,14,-16,-13,-6,-7,-8,-9,-10,-11,-12,-5,14,]),'DOUBLE_EQUALS':([2,7,8,9,17,18,19,21,22,23,24,25,26,27,28,29,],[16,-14,-15,-16,16,-16,16,16,16,16,16,16,16,-12,-5,16,]),'RPAREN':([7,8,17,18,19,21,22,23,24,25,26,27,28,],[-14,-15,28,-16,-13,-6,-7,-8,-9,-10,-11,-12,-5,]),'EQUALS':([9,],[20,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'calc':([0,],[1,]),'expression':([0,5,6,10,11,12,13,14,15,16,20,],[2,17,19,21,22,23,24,25,26,27,29,]),'var_assign':([0,],[3,]),'empty':([0,],[4,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> calc","S'",1,None,None,None),
  ('calc -> expression','calc',1,'p_calc','calculator.py',72),
  ('calc -> var_assign','calc',1,'p_calc','calculator.py',73),
  ('calc -> empty','calc',1,'p_calc','calculator.py',74),
  ('var_assign -> NAME EQUALS expression','var_assign',3,'p_var_assign','calculator.py',80),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_lparen_rparen','calculator.py',86),
  ('expression -> expression MULTIPLY expression','expression',3,'p_expression','calculator.py',92),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression','calculator.py',93),
  ('expression -> expression MODULUS expression','expression',3,'p_expression','calculator.py',94),
  ('expression -> expression POWER expression','expression',3,'p_expression','calculator.py',95),
  ('expression -> expression PLUS expression','expression',3,'p_expression','calculator.py',96),
  ('expression -> expression MINUS expression','expression',3,'p_expression','calculator.py',97),
  ('expression -> expression DOUBLE_EQUALS expression','expression',3,'p_expression','calculator.py',98),
  ('expression -> MINUS expression','expression',2,'p_expression_uniaryMinus','calculator.py',104),
  ('expression -> INT','expression',1,'p_expression_int_float','calculator.py',110),
  ('expression -> FLOAT','expression',1,'p_expression_int_float','calculator.py',111),
  ('expression -> NAME','expression',1,'p_expression_name','calculator.py',117),
  ('empty -> <empty>','empty',0,'p_empty','calculator.py',123),
]