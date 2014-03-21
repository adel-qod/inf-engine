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

import sys # argv, exit
import os # path
import logging

import parser # our parser and lexer module
import forward # Using forward chaining
def main():
  ''' exit 0 success, 1 args error, 2 parsing error '''
  log_format = "%(filename)s:%(funcName)s(): %(message)s"
  logging.basicConfig(strea=sys.stderr, level=logging.INFO,format=log_format)
  rules, facts = parse_argv(sys.argv[1:])
  rules, facts = read_rules(rules), read_facts(facts)
  new_facts = {}
  print("Facts: ")
  for fact in facts.keys():
    print(fact)
  print('----------------')
  print("Rules")
  for rule in rules:
    print(rule)
  print('----------------')
  new_fact = True
  while new_fact:
    for rule in rules:
      lhs, rhs = parser.split_rule(rule)
      tokens = parser.lex_lhs(lhs)
      tree = parser.parse(tokens)
      fired, new_fact = forward.forward_eval(tree, rhs, facts, new_facts)
      if fired:
        print("rule fired: ", rule)
      if new_fact:
        print("Fact added: ", rhs)
  print('-------------------')
  if len(new_facts) != 0:
    print("New facts: ")
    for fact in new_facts.keys():
      print(fact)
    print('----------------')
  else:
    print("No new facts were generated")


def parse_argv(argv):
  ''' Checks if the arguments are filenames, returns them if yes and fails if
  not'''
  print("Usage: ./main rules facts")
  if len(argv) < 2:
    print("Need two arguments: rules-file and facts-file")
    sys.exit(1)
  (rules, facts) = argv[:2]
  (rules, facts) = os.path.abspath(rules), os.path.abspath(facts)
  if not os.path.isfile(rules):
    print("The path you specified for rules path is not a file")
    sys.exit(1)
  if not os.path.isfile(facts):
    print("Tha path you sepcified for facts path is not a file")
    sys.exit(1)
  return rules, facts

def read_rules(rules):
  ''' Reads the rules files line by line and returns an array of lines '''
  with open(rules, "r") as f:
    lines = [line for line in f if line != '\n']
  return [line.strip() for line in lines]

def read_facts(facts):
  ''' Reads the facts file line by line and returns a dict of lines '''
  with open(facts, "r") as f:
    lines = [line for line in f if line != '\n']
  l = [line.strip() for line in lines]
  return dict((el, True) for el in l)

if __name__ == "__main__":
  main()
