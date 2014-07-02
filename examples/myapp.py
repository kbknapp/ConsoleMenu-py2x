#!/usr/bin/env python2
from __future__ import print_function
import consolemenu


app_title = '{}\n## My App\n{}'.format('#'*20,'#'*20)
cm = consolemenu.ConsoleMenu('menu',title=app_title)
cm.start() 
