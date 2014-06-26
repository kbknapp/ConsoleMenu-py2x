#!/usr/bin/env python2
from __future__ import print_function
import os
from collections import deque
import sys
import subprocess


class ConsoleMenu(object):
    def __init__(self, menu_path):
        self.__options = dict()
        self.__history = deque()
        self.__basedir = os.path.dirname(os.path.realpath(__file__))
        self.__mod_prefix = [os.path.basename(menu_path)]
        self.__menu_bar = ['Home']

        self.build_options(menu_path)

    def build_options(self, m_path):
        if os.path.isdir(m_path):
            i = 1
            for _, _, files in os.walk(m_path):
                added = []
                for f in files:
                    if f.startswith('__'):
                        continue
                    if f[-1] == 'c' and f[:-1] in added:
                        for k in self.__options:
                            if self.__options[k][4] == f[:-1]:
                                i = int(k)
                                break
                    elif f in added:
                        continue
                    pkg_list = self.__mod_prefix[:]
                    fm_list = '.'.join(self.__mod_prefix)
                    pkg_list.append(os.path.splitext(os.path.basename(f))[0])
                    pkg = '.'.join(pkg_list)
                    mod = __import__(pkg, fromlist=['.'.join(self.__mod_prefix)])
                    #print('p {}'.format(pkg))
                    #print('m {}'.format(mod))
                    #print('mp {}'.format(self.__mod_prefix))
                    if mod.otype.lower() == 'menu':
                        self.__options[str(i)] = [mod.short_name, mod.disp_name, 'menu', mod.sub_menu, f]
                    else:
                        self.__options[str(i)] = [mod.short_name, mod.disp_name, 'routine', mod.run, f]
                    if f[-1] == 'c':
                        added.append(f[:-1])
                    else:
                        added.append(f)
                    trim = False
                    while str(i) in self.__options:
                        i += 1
                if len(self.__history) > 0:
                    self.__options[str(i)] = ['Back', 'Back', 'Routine', self.back, None]
                else:
                    self.__options[str(i)] = ['Quit', 'Quit', 'Routine', self.exit, None]
                return


    def update_display(self):
        subprocess.call('clear')
        print(' > '.join(self.__menu_bar))
        print('')
        keys = self.__options.keys()
        keys.sort()
        for opt in keys:
            print('{} - {}'.format(opt, self.__options[opt][1]))
        print('')

    def exit(self):
        self.enter_on()
        sys.exit(0)

    def back(self):
        if len(self.__history) < 1:
            return
        self.__options = self.__history.popleft()
        self.__mod_prefix = self.__mod_prefix[:-1]
        self.__menu_bar = self.__menu_bar[:-1]

    def enter_on(self):
        pass

    def enter_off(self):
        pass

    def do_option(self, key):
        if key not in self.__options:
            return
        mod = self.__options[key]
        otype = mod[2].lower()
        if otype == 'menu':
            self.__history.appendleft(self.__options)
            self.__options = dict()
            self.__mod_prefix.append(mod[3])
            self.__menu_bar.append(mod[0])
            d = self.__mod_prefix[:]
            d.insert(0,self.__basedir)
            self.build_options('/'.join(d))
        elif otype == 'routine':
            self.enter_on()
            self.__options[key][3]()
            self.enter_off()
        else:
            return



    def start(self):
        while True:
            self.update_display()

            ans = raw_input('> ')
            if ans:
                if ans.lower() == 'b':
                    self.back()
                elif ans.lower() == 'q':
                    self.exit()
                else:
                    self.do_option(ans)

if __name__ == '__main__':
    m_dir = os.path.join(os.path.dirname(__file__),'menu')
    cm = ConsoleMenu(m_dir)
    try:
        cm.enter_off()
        cm.start()
    except:
        cm.enter_on()
