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

import logging

def forward_eval(root, rhs, facts, new_facts):
  ''' Takes a syntax tree representing the rule and a set of facts 
      return bool tuple (fired, new_fact)'''
  res = post_order_eval(root, facts)
  if res and rhs not in facts:
    new_facts[rhs] = True
    facts[rhs] = True
    return (True, True)
  elif res:
    return (True, False)
  else:
    # return false if the thing we got 
    return (False, False)

def post_order_eval(node, facts):
  if node is None:
    return True
  l = post_order_eval(node.left, facts)
  r = post_order_eval(node.right, facts)
  logging.debug(node)
  if node.value == '&':
    if l and r:
      return True
    else:
      return False
  elif node.value == '|':
    if l or r:
      return True
    else:
      return False
  elif node.value == '!':
    return not l
  else: # gotta be an ID
    if node.value in facts:
      return True
    else:
      return False
