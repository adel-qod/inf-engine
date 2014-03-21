#!/usr/bin/python3.2 -tt

# Copyright (c) 2014, Adel Qodmani
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice, 
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, 
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON 
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF 
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys # sys.exit
import logging

class Node:
  def __init__(self, value=None):
    self.value = value
    self.parent = None
    self.left = None
    self.right = None
  def __str__(self):
    return self.value if self.value else "None"

def split_rule(rule):
  ''' Returns a list of two members: LHS and RHS of a rule '''
  sides = rule.split('>')
  sides = [token.strip() for token in sides]
  logging.debug(sides)
  return (sides[0], sides[1])

def lex_lhs(lhs):
  ''' Given a LHS of a rule, it returns the tokens found '''
  tokens = lhs.split()
  logging.debug(tokens)
  return tokens

# Contains the stream of the tokens currently being parsed
tokens = None

def parse(tokens_):
  ''' Parses the tokens and returns a syntax tree '''
  global tokens
  if len(tokens_) == 0:
    return None
  tokens = tokens_
  return exp()

def look_ahead():
  ''' Returns the next token in the tokens stream '''
  global tokens
  if len(tokens) == 0:
    return ''
  return tokens[0]

def consume():
  global tokens
  if len(tokens) == 0:
    print("Consume: no more tokens")
    sys.exit(2)
  tokens.pop(0)

def syntax_error(err):
  global tokens
  print(err)
  print("tokens: ", tokens)
  sys.exit(2)

# From here on, the code for the recursive descent parsing routines
def exp():
  a = exp1()
  b = or_exp()
  if a != None and b != None:
    node = Node('|')
    node.left = b
    node.right = a
    return node
  elif a != None:
    return a
  else:
    return b

def exp1():
  a = exp2()
  b = and_exp()
  if a != None and b != None:
    node = Node('&')
    node.left = b
    node.right = a
    return node
  elif a != None:
    return a
  else:
    return b
  
def or_exp():
  global tokens
  if look_ahead() == '|':
    consume()
    node = Node('|')
    a = exp1()
    b = or_exp()
    if a != None and b != None:
      node.left = b
      node.right = a
      return node
    else:
      return a
  else:
    return None

def and_exp():
  if look_ahead() == '&':
    consume()
    node = Node('&')
    a = exp2()
    b = and_exp()
    if a != None and b != None:
      node.left = b
      node.right = a
      return node
    else:
      return a
  else:
    return None

def exp2():
  if look_ahead() == '!':
    consume()
    node = Node('!')
    node.left = exp3()
    return node
  else:
    return exp3()

def exp3():
  if look_ahead().isalpha():
    node = Node(look_ahead())
    consume()
    return node
  elif look_ahead() == '(':
    consume()
    exp()
    if look_ahead() != ')':
      syntax_error("syn")
  else:
    syntax_error("syn")
