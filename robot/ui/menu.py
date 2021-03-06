# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2015 Björn Larsson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from robot.ui import button
from robot.utils import iterators

BUTTON_BACK = 0
BUTTON_SELECT = 1
BUTTON_UP = 2
BUTTON_DOWN = 3

class MenuEntry(object):
    def __init__(self, name):
        self._name = name
        self._parent = None
        self._children = list()
        self._current = None
        self._bc = iterators.BiCircular(self._children)

    def __getitem__(self, name):
        """
        Returns the item with the given name
        If missing, a new item with the given name is created
        """
        try:
            return next((x for x in self._children if x.Name == name))
        except StopIteration:
            return self.append(MenuEntry(name))


    def __repr__(self):
        return "MenuEntry ({0})".format( self.Name)

    def __str__(self):
        return self.Name

    @property
    def Current(self):
        if(self._current is None and len(self._children) > 0):
            self._current = self._children[0]

        return self._current

    @property
    def IsLeaf(self):
        return len(self._children) == 0

    @property
    def Parent(self):
        return self._parent

    @Parent.setter
    def Parent(self, value):
        self._parent = value

    @property
    def Name(self):
        return self._name

    @property
    def Display(self):
        return self.Name

    def append(self, child):
        self._children.append(child)
        child.Parent = self

        return child

    def next(self):
        self._current = self._bc.next()
        return self._current

    def previous(self):
        self._current = self._bc.previous()
        return self._current

    def input(self, button):
        # Implement this to add functionality to leaf nodes
        pass



class Menu(object):
    def __init__(self):
        # Create all buttons and register to their respective Pi pins
        self._back = button.UIButtonBehaviour(button.Button(26))
        self._select = button.UIButtonBehaviour(button.Button(21))
        self._up = button.UIButtonBehaviour(button.Button(20))
        self._down = button.UIButtonBehaviour(button.Button(16))

        self._buttons = (self._back, self._select, self._down, self._up)

        #  Setup listeners
        self._back.OnClick += self._onBack
        self._select.OnClick += self._onSelect
        self._up.OnClick += self._onUp
        self._down.OnClick += self._onDown

        self._root = MenuEntry("Root")
        self._current = self._root
        self._display = None
        self._selected = None

    def __del__(self):
        #  Remove listeners
        self._back.OnClick -= self._onBack
        self._select.OnClick -= self._onSelect
        self._up.OnClick -= self._onUp
        self._down.OnClick -= self._onDown

    def add(self, path, entry):
        """
        Adds a menu entry at the given path
        Path should be of the format /a/b/c
        """
        names = path.split("/")
        current = self._root


        for name in names:
            current = current[name]

        current.append(entry)

        if(self._display == None):
            self._display = self._current.Current


    def _onBack(self, sender):
        if self._selected:
            self._selected = None
        elif self._current.Parent:
            self._current = self._current.Parent
            self._display = self._current.Current

    def _onSelect(self, sender):
        if self._selected:
            self._selected.input(BUTTON_SELECT)
        elif self._display.IsLeaf:
            self._selected = self._display
        else:
            self._current = self._display
            self._display = self._current.Current

    def _onUp(self, sender):
        if self._selected:
            self._selected.input(BUTTON_UP)
        else:
            self._display = self._current.previous()

    def _onDown(self, sender):
        if self._selected:
            self._selected.input(BUTTON_DOWN)
        else:
            self._display = self._current.next()

    def update(self):
        for b in self._buttons:
            b.update()

    def render(self):
        if self._selected:
            return "* {0}".format(self._selected.Display)
        elif self._display:
            return self._display.Display
        else:
            return ""

