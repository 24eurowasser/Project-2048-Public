"""This file implements the Observer Pattern for 2048"""

from abc import ABC, abstractmethod
from queue import Queue
from threading import Thread
from .arguments import Command, Screen


class Event(ABC):
    """Superclass for events that can be sent to the EventManager"""
    @abstractmethod
    def __init__(self, data):
        """
        Constructs Event

        Parameters
        ----------
        data : object
            arguments passed with an event
        """
        self._data = data

    @property
    def data(self):
        """Returns event argument"""
        if self._data is None:
            raise Exception("This event doesn't carry any data!")
        return self._data


class QuitEvent(Event):
    """Announces to stop the game."""
    def __init__(self):
        self._data = None


class StartEvent(Event):
    """Announces to start the game."""
    def __init__(self):
        self._data = None


class InputRequest(Event):
    """Announces event Input Request."""
    def __init__(self):
        self._data = None


class StateEvent(Event):
    """Announces window switch."""
    def __init__(self, state: Screen):
        self._data = state


class SlideEvent(Event):
    """Announces slide command."""
    def __init__(self, cmd: Command):
        self._data = cmd


class EventManager:
    """Coordinates broadcast to Observers

    Attributes
    ----------
    _observers: list
    """
    def __init__(self):
        """Construct Event Manager and start event loop"""
        self._observers: list = []
        self._event_queue = Queue()


    def register_observer(self, observer) -> None:
        """Add object to broadcast list"""
        self._observers.append(observer)


    def post(self, event: Event) -> None:
        """Broadcast events to the observers"""
        # InputRequest should not enter the Thread – yields errors with pygame/curses
        if isinstance(event, InputRequest):
            self._announce(event)
        # StartEvent starts the event loop
        elif isinstance(event, StartEvent):
            t = Thread(target=self._next_event, daemon=True)
            t.start()
            self._announce(event)
        else:
            self._event_queue.put(event)


    def _announce(self, event) -> None:
        """Broadcast event to all observers"""
        for observer in self._observers:
            observer.notify(event)


    def _next_event(self) -> None:
        """Event loop, that announces next event to the observers"""
        while True:
            event = self._event_queue.get(block=True)
            self._announce(event)
            self._event_queue.task_done()
 