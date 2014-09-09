# encoding: utf-8

"""

"""

from npyscreen import NPSAppManaged

from . import forms


class KerminalApp(NPSAppManaged):
    keypress_timeout_default = 1  # this is as short as possible
    #keypress_timeout = 1

    def onStart(self):
        self.addForm('MAIN', forms.ConnectQuery)
        self.addForm('CONNECTION', forms.Connection)