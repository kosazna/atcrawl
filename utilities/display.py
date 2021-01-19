# -*- coding: utf-8 -*-

from atcrawl.utilities.singleton import Singleton


class Display(metaclass=Singleton):
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'

    def __init__(self, mode=None):
        self._mode = mode
        self._content = []

    @staticmethod
    def _display(content, kind=None):
        if kind is None:
            return content
        else:
            return f"[{kind}] - {content}"

    def set_mode(self, mode):
        self._mode = mode

    def get_mode(self):
        return self._mode

    def get_content(self):
        to_show = '\n'.join(self._content)
        return to_show

    def erase(self):
        self._content = []

    def __call__(self, content, kind=None):
        if self._mode == 'CMD':
            print(self._display(content, kind))
        else:
            self._content.append(self._display(content, kind))
