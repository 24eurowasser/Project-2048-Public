"""This file implements the construction of the objects required for 2048"""

import argparse as ap
import curses
import pathlib
import os
from .model import Model
from .controller.controller_remote import ControllerRemote
from .controller.controller_local import ControllerLocal
from .controller.controller_client import ControllerClient
from .view.view_gui import ViewGUI
from .view.view_shell import ViewShell
from .event_manager import EventManager, StartEvent


def main() -> None:
    """Starts the _game 2048"""
    parser = ap.ArgumentParser()      # Flags for starting the game
    parser.add_argument("--bci", help="play game with BCI (default: keyboard)",
                        action="store_true")
    parser.add_argument("--shell", help="show game in window (default: gui)",
                        action="store_true")
    parser.add_argument("--_width", help="choose own width (default=4)",
                        type=int, default=4)
    parser.add_argument("--_height", help="choose own height (default=4)",
                        type=int, default=4)
    parser.add_argument("--logging", help="Choose to log the game activity (default: no logging)",
                        action="store_true")
    parser.add_argument('--client', type=str)
    args = parser.parse_args()

    if args.client:
        ControllerClient(args.client)
        return

    # Create a config file, so that database knows if we should log actions or not
    file_name = "Config - Logging.txt"
    current_path = pathlib.Path(__file__).parent.resolve()
    root_path = current_path.parent
    file_path = os.path.join(root_path, file_name)

    if args.logging:
        file_content = "True"
        with open(file_path, "w") as file:
            file.write(file_content)
    else:
        file_content = "False"
        with open(file_path, "w") as file:
            file.write(file_content)

    ev_manager = EventManager()
    
    # Instantiate the model object
    game = Model(ev_manager)

    # Instantiate a view object
    stdscr = None
    if args.shell:
        stdscr = curses.initscr()
        ViewShell(ev_manager, game, stdscr)
    else:
        ViewGUI(ev_manager, game, args.bci)

    ControllerLocal(ev_manager, stdscr)
    if args.bci:                            # Instantiate a controller object
        ControllerRemote(ev_manager)

    # Start the game
    ev_manager.post(StartEvent())


if __name__ == "__main__":
    main()
