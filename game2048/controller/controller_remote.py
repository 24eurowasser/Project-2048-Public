"""This file implements the remote input decoding"""

import curses
import pathlib
import os
from ..event_manager import EventManager
from .interface_controller import InterfaceController
import socket
from threading import Thread
from ..arguments import *
from ..event_manager import EventManager


class ControllerRemote(InterfaceController):
    """This class implements signals from a client computer as input source to play 2048."""
    def __init__(self, ev_manager: EventManager):
        """
        Constructor of the class ControllerRemote.

        Parameters:
        ----------
        _ev_manager: EventManager
            controls communication with other modules
        _screen: curses.window
            the shell screen or None for GUI view
        """
        super().__init__(ev_manager)
        t2 = Thread(target=self._set_up_server, daemon=True)
        t2.start()

    @staticmethod
    def input_parser(inp: str) -> Command:
        """Parse an input string to a command"""
        inp: str = inp.lower()
        if inp in ["d", "right"]:
            return Command.RIGHT
        elif inp in ["a", "left"]:
            return Command.LEFT
        elif inp in ["w", "up"]:
            return Command.UP
        elif inp in ["s", "down"]:
            return Command.DOWN
        elif inp in ["p", "pause"]:
            return Command.PAUSE
        elif inp in ["e", "ex", "exit"]:
            return Command.EXIT
        elif inp in ["r", "re", "restart"]:
            return Command.RESTART
        elif inp in ["start", "continue"]:
            return Command.START
        else:
            return Command.EMPTY

    def _set_up_server(self, port=2048, hostname="", buffer_size=1024) -> None:
        """Set up a server to connect to a client.

        Parameters
        ----------
        port: int
            The own server port. The client has to connect to the same port.
        hostname: str
            Specify the hostname.
        buffer_size: int
            Specify the number of bytes the server should receive in one receive-action
        """
        self._create_ip_config_file(port=port)
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            bind_address = (ip_address, port)
            server_socket.bind(bind_address)
            while True:
                server_socket.listen()
                (conn, address) = server_socket.accept()
                received_bytes = conn.recv(buffer_size)
                inp: str = str(received_bytes, "utf-8")
                received_command: Command = self.input_parser(inp)
                if received_command == Command.EMPTY:
                    continue
                else:
                    self._play_the_game(received_command)

    def _create_ip_config_file(self, port: int) -> pathlib.Path:
        """Creates a text file in the root folder of this project with the server IP & port.

        Parameters
        ----------
        port: int
            The port that is used by the server

        Returns
        -------
        pathlib.Path
            The file path of the created config file.
        """
        file_name = "Config - Server IP & Port.txt"
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        file_content = f"Server Information:\n\nIP-Address : {ip_address}\nPort : {port}"
        current_path = pathlib.Path(__file__).parent.resolve()
        root_path = current_path.parent.parent
        file_path = os.path.join(root_path, file_name)

        with open(file_path, "w") as file:
            file.write(file_content)

        return file_path
