#!/usr/bin/env python
from __future__ import print_function
import subprocess

short_name = 'Opt 3'
disp_name = 'Option 3 Submenu'
otype = 'Routine'
need = ['need 1: ', 'need 2: ', 'need 3: ']
answers = []

def run():
	global answers
	while True:
		subprocess.call('clear')
		i = 0
		while i < len(need):
			ans = raw_input(need[i])

			if validate(ans):
				answers.append(ans)
				i += 1

		final = 'Doing something with '
		for a in answers:
			final = '{}, {}'.format(final, a)
		print(final)
		raw_input()
		return

def validate(char):
	if char:
		return True
	return False