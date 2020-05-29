#!/usr/bin/env python
# encoding: utf-8
import sys


for line in sys.stdin:
  words = line.split()
  for word in words:
      print('{}\t{}'.format(word.strip(), 1))