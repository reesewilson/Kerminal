# encoding: utf-8

from npyscreen.wgwidget import Widget
from npyscreen import TitleText

from functools import wraps


#I see one major drawback with this approach, as opposed to simply using a
#special Form to extend any Widget into a LiveWidget, which is that one must
#explicitly create a new class for each npyscreen widget you want to use in
#order to inherit the LiveWidget functionality
class LiveWidget(Widget):
    """
    The LiveWidget differs from the Widget in only one substantial way: it has
    built-in support for a `feed` method which may be passed in with the "feed"
    keyword argument during instantiation, or modified elsewhere. Whenever
    `LiveWidget.feed` is called, it's return will be assigned to
    `LiveWidget.value` (no need to write this assignment yourself).

    Scheduling the calling of `LiveWidget.feed` is up to the designer. One motif
    of interest is using a special Form class to register LiveWidgets and then
    calling their feeds during `while_waiting`.
    """
    def __init__(self, screen, feed=None, *args, **kwargs):
        super(LiveWidget, self).__init__(screen, *args, **kwargs)
        if feed is not None:
            self.feed = feed

    def _feed(self):
        """
        The internal method for `feed`. This must simply return an appropriate
        value to be assigned to `LiveWidget.value`.
        """
        return ''

    @property
    def feed(self):
        """
        The method for updating the LiveWidget's value. Customize your widget by
        setting this to a function that returns the desired value from a live
        data source.
        """
        def _feed_wrapper(f):
            @wraps(f)
            def wrapper(*args, **kwds):
                self.value = f(*args, **kwds)
            return wrapper
        return _feed_wrapper(self._feed)

    @feed.setter
    def feed(self, func):
        if not callable(func):
            raise ValueError('LiveWidget.feed must be assigned a callable')
        self._feed = func


class LiveTitleText(TitleText, LiveWidget):
    pass