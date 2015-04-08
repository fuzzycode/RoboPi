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

BUTTON_BACK = 0
BUTTON_SELECT = 1
BUTTON_UP = 2
BUTTON_DOWN = 3

class MenuEntry(object):
    def __init__(self, parent):
        self._parent = parent
        self._children = list()
        self_current = None

    @property
    def Current(self):
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
    def Display(self):
        raise NotImplementedError("Implement this")

    def append(self, child):
        self._children.append(child)
        child.Parent = self

    def next(self):
        pass

    def previous(self):
        pass

    def update(self, buttons):
        pass



class Menu(object):
    def __init__(self, root):
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

        self._current = None

    def _onBack(self, sender):
        if self._current:
            if self._current.Parent:
                self._current = self._current.Parent
                self.update()

    def _onSelect(self, sender):
        if self._current and not self._current.IsLeaf:
            self._current = self._current.Current
        self.update()

    def _onUp(self, sender):
        if self._current and self._current.IsLeaf:
            self._current.update(BUTTON_UP)
        elif self._current:
            self._current = self._current.previous()

    def _onDown(self, sender):
        if self._current and self._current.IsLeaf:
            self._current.update(BUTTON_DOWN)
        elif self._current:
            self._current = self._current.next()

    def update(self):
        for b in self._buttons:
            b.update()


