# encoding: utf-8

"""
"""

from . import __version__
from .commands import KerminalCommands
from .containers import EscapeForwardingSmartContainer, EscapeForwardingGridContainer, KerminalMultiLineText
from .widgets import TextCommandBox, KerminalStatusText
from .utils import launch_text

import npyscreen2

#import curses
from functools import partial
from time import strftime


def header_feed(thread):
    status = ' Kerminal v {0} - Sys. Time: {1} '.format(__version__,
                                                        strftime("%Y-%m-%d %H:%M:%S"))
    if thread.connected:
        status += '- Connected: {0} '.format(thread.data.get('v.name'))
    return status


class KerminalForm(npyscreen2.Form):
    def __init__(self, *args, **kwargs):
        super(KerminalForm, self).__init__(*args, **kwargs)

        self.action_controller = KerminalCommands(self, self)

        self.text = self.add(KerminalMultiLineText,
                             widget_id='text',
                             editable=True,
                             margin=0,
                             auto_manage=False)
        self.text.build_contained_from_text(launch_text)

        self.smart = self.add(EscapeForwardingSmartContainer,
                              widget_id='smart',
                              editable=True,
                              auto_manage=False,)

        self.top_bar = self.add(npyscreen2.BorderBox,
                                widget_id='top_bar',
                                auto_manage=False,
                                top=True,
                                bottom=False,
                                left=False,
                                right=False)

        self.bot_bar = self.add(npyscreen2.BorderBox,
                                widget_id='bottom_bar',
                                auto_manage=False,
                                top=True,
                                bottom=False,
                                left=False,
                                right=False)

        self.header = self.add(npyscreen2.TextField,
                               widget_id='header',
                               auto_manage=False,
                               editable=False,
                               value=' Kerminal Header ',
                               color='LABEL',
                               bold=True,
                               feed=partial(header_feed,
                                            self.form.parent_app.stream))

        self.cl_header = self.add(npyscreen2.TextField,
                                  widget_id='cl_header',
                                  auto_manage=False,
                                  editable=False,
                                  value=' Kerminal Command Line ',
                                  color='LABEL',
                                  bold=True)

        self.command_line = self.add(TextCommandBox,
                                     widget_id='command_line',
                                     auto_manage=False,
                                     editable=True,
                                     value='Press ESC to enter commands')

        self.status_prefix = self.add(KerminalStatusText,
                                      widget_id='status_prefix',
                                      auto_manage=False,
                                      editable=False,
                                      value='STATUS:',
                                      height=1,
                                      bold=True)

        self.status = self.add(npyscreen2.TextField,
                               widget_id='status',
                               auto_manage=False,
                               editable=False,
                               value='',
                               feed_reset=True)
        self.show_text()

    #At this time, main can only be "text" or "smart"
    def show_text(self, msg=None):
        self.smart.hidden = True
        self.text.hidden = False
        if msg is not None:
            self.text.build_contained_from_text(msg)
            self.text._resize()

    def show_smart(self):
        self.smart.hidden = False
        self.text.hidden = True

    def set_up_exit_condition_handlers(self):
        super(KerminalForm, self).set_up_exit_condition_handlers()
        self.how_exited_handlers.update({'escape': self.toggle_commands})

    def toggle_commands(self, inpt=None):
        command_line_index = self.contained.index(self.command_line)
        if self.edit_index == command_line_index:
            if not self.text.hidden:
                self.edit_index = self.contained.index(self.text)
            elif not self.smart.hidden:
                self.edit_index = self.contained.index(self.smart)
            self.command_line.value = 'Press ESC to enter commands'
        else:
            self.edit_index = command_line_index
            self.command_line.value = ''

    def while_waiting(self):
        self.call_feed()
        self.display()

    def info(self, msg):
        self.status_prefix.value = 'INFO:'
        self.status_prefix.color = 'LABEL'
        self.status.feed = lambda: msg
        self.resize_status_line()

    def warning(self, msg):
        self.status_prefix.value = 'WARNING:'
        self.status_prefix.color = 'CAUTION'
        self.status.feed = lambda: msg
        self.resize_status_line()

    def error(self, msg):
        self.status_prefix.value = 'ERROR:'
        self.status_prefix.color = 'DANGER'
        self.status.feed = lambda: msg
        self.resize_status_line()

    def critical(self, msg):
        self.status_prefix.value = 'CRITICAL:'
        self.status_prefix.color = 'CRITICAL'
        self.status.feed = lambda: msg
        self.resize_status_line()

    def resize(self):
        self.text.multi_set(rely=self.rely + 1,
                            relx=self.relx,
                            max_height=self.max_height - 4,
                            max_width=self.max_width)
        self.smart.multi_set(rely=self.rely + 1,
                             relx=self.relx,
                             max_height=self.max_height - 4,
                             max_width=self.max_width)
        self.top_bar.multi_set(rely=self.rely,
                               relx=self.relx,
                               max_height=self.max_height,
                               max_width=self.max_width)
        self.bot_bar.multi_set(rely=self.rely + self.height - 2,
                               relx=self.relx,
                               max_height=self.max_height,
                               max_width=self.max_width)
        self.header.multi_set(rely=self.rely,
                              relx=self.relx + 1,
                              max_width=self.max_width,
                              max_height=1)
        self.cl_header.multi_set(rely=self.rely + self.height - 2,
                                 relx=self.relx + 1,
                                 max_width=self.max_width,
                                 max_height=1)
        self.command_line.multi_set(rely=self.rely + self.height - 1,
                                    relx=self.relx,
                                    max_height=1,
                                    max_width=self.max_width)
        self.resize_status_line()

    def resize_status_line(self):
        self.status_prefix.multi_set(rely=self.rely + self.height - 3,
                                     relx=self.relx,
                                     max_width=self.max_width,
                                     max_height=1)

        status_offset = len(self.status_prefix.value) + 1
        self.status.multi_set(rely=self.rely + self.height - 3,
                              relx=self.relx + status_offset,
                              max_width=self.max_width - status_offset,
                              max_height=1)
