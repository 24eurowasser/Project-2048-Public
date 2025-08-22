"""This file implements the database for the game"""

import pathlib
import os
import datetime as dt
import numpy as np
import json
from .arguments import Logging


class Database:
    """This class implements a database for the game 2048 for logging and restoring data."""

    def __init__(self):
        """
        Constructor of class Database.

        Parameters
        ----------
        _started : bool
            Indicates if the logging process started
        _path_folder : pathlib.Path
            The path for the "database_content" folder
        _path_log_system : pathlib.Path
            The path for the "temp_Log - System.md" file
        _path_log_game : pathlib.Path
            The path for the "temp_Log - Game.md" file
        _path_save_game : pathlib.Path
            The path for the "Save - Game.json" file
        _path_save_record : pathlib.Path
            The path for the "Save - Record.json" file
        """
        self._started = False
        self._path_folder = None
        self._path_log_system = None
        self._path_log_game = None
        self._path_save_game = None
        self._path_save_record = None


    def _logging_option(self) -> bool:
        """
        Reads the config file and determines whether we should log something or not.

        Returns
        -------
        bool
            If True, then we will log content, otherwise not
        """

        # Get config file path:
        file_name = "Config - Logging.txt"
        current_path = pathlib.Path(__file__).parent.resolve()
        root_path = current_path.parent
        file_path = os.path.join(root_path, file_name)

        if not os.path.exists(file_path):
            return True
        else:
            with open(file_path, "r") as file:
                file_content = file.read()
                if file_content == "True":
                    return True
                else:
                    return False


    def _create_folder(self) -> pathlib.Path:
        """
        Creates a folder for the database files.

        Returns
        -------
        pathlib.Path
            Returns the path of the created folder.
        """
        # Get the current path, in which this file is stored
        current_path = pathlib.Path(__file__).parent.resolve()
        current_path = current_path.parent
        # The folder, in which the database content should be stored
        folder_name = "database_content"
        # Create a path for the desired folder
        self._path_folder = os.path.join(current_path, folder_name)

        # Only create the folder for database, when it doesn't exit yet
        if not os.path.exists(self._path_folder):
            os.makedirs(self._path_folder)
        return self._path_folder

    def _create_temp_logs(self) -> (pathlib.Path, pathlib.Path):
        """
        Creates a temporary log file.

        Returns
        -------
        tuple
            Returns a tuple for the path of the two log files.
        """
        # Skip the logging if necessary
        if not self._logging_option():
            return (None, None)

        # Create a folder for the content
        self._create_folder()
        file_system = "temp_Log - System.md"
        file_game = "temp_Log - Game.md"
        self._path_log_system = os.path.join(self._path_folder, file_system)
        self._path_log_game = os.path.join(self._path_folder, file_game)

        current_time = dt.datetime.now().strftime("%Y_%m_%d %H-%M-%S")
        alignment_spaces = " " * 32

        # Create the files
        with open(self._path_log_system, "w") as system_file:
            system_file.write("### LOG CREATION" + alignment_spaces + "at :clock8: " + current_time + "\n\n")

        with open(self._path_log_game, "w") as game_file:
            game_file.write("### LOG CREATION" + alignment_spaces + "at :clock8: " + current_time + "\n\n")

        return (self._path_log_system, self._path_log_game)


    def _finalize_log_files(self) -> (pathlib.Path, pathlib.Path):
        """
        Changes the names of the temporary log files to a final name.

        Returns
        -------
        tuple
            Returns the paths of the adjusted files.
        """
        # Skip the logging if necessary
        if not self._logging_option():
            return (None, None)

        # Get the current time
        current_time = dt.datetime.now().strftime("%Y_%m_%d %H-%M-%S")

        # Create an unique name for the log files
        file_system = current_time + "   Log - System.md"
        file_game = current_time + "    Log - Game.md"

        final_system_path = os.path.join(self._path_folder, file_system)
        final_game_path = os.path.join(self._path_folder, file_game)

        # Rename the files
        os.rename(self._path_log_system, final_system_path)
        os.rename(self._path_log_game, final_game_path)

        return (final_system_path, final_game_path)


    def _is_file_too_big(self, file: pathlib.Path, added_content: str) -> bool:
        """
        Checks if a file is bigger than 10 MB, when the added_content would be inserted to it.

        Parameters
        ----------
        file : object from pathlib
            Contains the path of the file we want to check.
        added_content : str
            The string that should be inserted to the file.

        Returns
        -------
        bool
            Indicates if a file is too big when content is inserted.
        """
        size_limit = (1024 ** 2) * 10  # <- Change the 10 to adjust the MB size
        file_size = os.path.getsize(file)
        content_size = len(added_content.encode('utf-8'))
        combined_size = file_size + content_size
        comparison = combined_size > size_limit

        if comparison:
            print("Logging not possible, the file is too big!")
            return comparison
        else:
            return comparison

    def _matrix_to_markdown(self, matrix: np.ndarray) -> str:
        """
        Create a formatted markdown string output, based on an input matrix.

        Parameters
        ----------
        matrix : np.ndarray
            The matrix we want to convert to a string.

        Returns
        -------
        str
            A string representation for a matrix.
        """
        result = ""

        # First we need to have 2 rows for the header and alignment
        header = " - |"
        alignment = " :---: |"
        column_length = len(matrix[0])

        # Add header string "| - | - | - | ..."
        result = result + "| - |"
        if column_length > 1:
            for i in range(column_length - 1):
                result = result + header

        # Add alignment string "| :---: | :---: | :---: | ..." below
        result = result + "\n| :---: |"
        if column_length > 1:
            for i in range(column_length - 1):
                result = result + alignment

        # We need to add the matrix elements to the table now
        # The very first element in each row needs a special format
        # We access these elements by using the flag first_row_element
        for row in matrix:
            result = result + "\n"
            first_row_element = True
            for column in row:
                if first_row_element:
                    result = result + "| " + str(int(column)) + " | "
                    first_row_element = False
                    continue
                result = result + str(int(column)) + " | "

        return result


    def _update_highscore_record(self, highscore: int) -> pathlib.Path:
        """
        Updates the save file for the current record of the achieved high score.

        Parameters
        ----------
        highscore
            The highscore value that will may cause an update of the current record.

        Returns
        -------
        pathlib.Path
            The file path of the save file.
        """
        # First check if there is already a highscore save file.
        self._create_folder()
        file_name = "Save - Highscore.json"
        self._path_save_record = os.path.join(self._path_folder, file_name)
        record_file_exists = os.path.exists(self._path_save_record)

        last_record = 0
        new_record = highscore

        # Read the last record, if a save file does exit
        if record_file_exists:
            with open(self._path_save_record, "r") as file:
                last_record = int(float(file.read()))

        # Update new record, if the loaded record is bigger
        if last_record > highscore:
            new_record = last_record

        # Create the record save file
        with open(self._path_save_record, "w") as file:
            file.write(str(new_record))

        return self._path_save_record

    def log(self, content, option=Logging.COMMENT, final_log=False) -> (pathlib.Path, pathlib.Path):
        """
        Logs content into two logs files, which have different level of detail.

        Parameters
        ----------
        content
            Either a numpy matrix or a string.
        option
            Choosing the content type, like a matrix or a comment.
        final_log
            Indicates if the current entry, will be the final log.

        Returns
        -------
        pathlib.Path
            Returns the path of the adjusted file.
        """
        # Skip the logging if necessary
        if not self._logging_option():
            return (None, None)

        # Check if this is the first log
        if not self._started:
            # Set the flag for starting the log process to True and create the file
            self._started = True
            self._create_temp_logs()

        # Get the current time
        current_time = dt.datetime.now().strftime("%Y.%m.%d - %H:%M:%S")
        # This will be the logged content
        log = ""

        ## Create the log string based on the chosen option
        if option == Logging.GAMEFIELD:
            # Check if the content is actually a matrix
            if not isinstance(content, np.ndarray):
                print("ERROR in the log() function from database.py")
                print("Content is not an instance of numpy.ndarray, yet option was set to 'Logging.GAMEFIELD'")
                # End the function
                return
            # Convert the matrix to markdown
            matrix_content = self._matrix_to_markdown(content)
            # Create the final log string
            alignment_spaces = " " * 12
            log = ":large_orange_diamond: **GAMEFIELD**" + alignment_spaces + "at _" + current_time + "_:\n" + matrix_content + "\n\n"

        elif option == Logging.COMMAND:
            alignment_spaces = " " * 24
            log = ":red_circle: **COMMAND**" + alignment_spaces + "at _" + current_time + "_:\\\n**" + str(
                content) + "**\n\n"

        elif option == Logging.USER_INPUT:
            alignment_spaces = " " * 14
            log = ":large_blue_circle: **USER INPUT**" + alignment_spaces + "at _" + current_time + "_:\\\n**" + str(
                content) + "**\n\n"

        elif option == Logging.COMMENT:
            alignment_spaces = " " * 3
            log = ":diamond_shape_with_a_dot_inside: **COMMENT**" + alignment_spaces + "at _" + current_time + "_:\\\n**" + str(
                content) + "**\n\n"

        # No valid option was entered
        else:
            print("ERROR IN THE LOG FUNCTION.\n")
            print("Enter an option string with the following options: 'matrix', 'command', 'user_input', 'comment'.\n")
            print("Upper and lower case is irrelevant for the option-string!\n")
            return

        # Log the content, if the file and the content itself is small enough
        # Comment-Logs will only be displayed in the "Log - System.md" files
        if not option == Logging.COMMENT:
            if not self._is_file_too_big(self._path_log_system, log):
                # Add content to "Log - System.md"
                with open(self._path_log_system, "a") as system_file:
                    system_file.write(log)

            if not self._is_file_too_big(self._path_log_game, log):
                # Add content to "Log - Game.md"
                with open(self._path_log_game, "a") as game_file:
                    game_file.write(log)
        else:
            if not self._is_file_too_big(self._path_log_system, log):
                # Add content to "Log - System.md"
                with open(self._path_log_system, "a") as system_file:
                    system_file.write(log)

        # End the writing process for the files completely when final_log is True
        if final_log:
            names = self._finalize_log_files()
            return names

        return (self._path_log_system, self._path_log_game)

    def create_save(self, matrix: np.ndarray, current_highscore: int) -> (pathlib.Path, pathlib.Path):
        """
        Creates a JSON file, in which the content of a numpy matrix is stored.

        Parameters
        ----------
        matrix
            The matrix we want to store in a JSON file.
        current_highscore
            The highscore of the current gaming session.

        Returns
        -------
        tuple
            Returns the paths of the created files.
        """
        # Create the file path for "Save - Game.json".
        folder_path = self._create_folder()
        file_name = "Save - Game.json"
        self._path_save_game = os.path.join(folder_path, file_name)

        # If the input is currupted, then return basic values
        if matrix is None:
            matrix = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        if current_highscore is None:
            current_highscore = 0

        # JSON can't handle numpy arrays, so we need to convert them first
        matrix_to_list = matrix.tolist()

        # The highscore and gamefield will be stored in a python dictionary
        python_save = {
            "highscore": current_highscore,
            "gamefield": matrix_to_list
        }

        # Convert python_save to the JSON format
        save_converted = json.dumps(python_save)

        # Write the save state content within the file of savestate_path
        with open(self._path_save_game, "w") as file:
            file.write(save_converted)

        # Also create or update the highscore record
        self._update_highscore_record(current_highscore)

        return (self._path_save_game, self._path_save_record)


    def read_save(self, file: pathlib.Path) -> tuple:
        """
        Creates a tuple containing the last highscore and gamefield, based on an input JSON file.

        Parameters
        ----------
        file
            The path to a JSON file that should be read.

        Returns
        -------
        tuple
            A tuple containing the last highscore, gamefield or the highscore record.
        """
        # If the save file doesn't exit, return a warning message in the returned load
        if not os.path.exists(file):
            return (False, "Save file doesn't exit!")

        # /.../.../file -> "file"
        file_name = os.path.basename(file)

        # If the file is the highscore record file, then return the record
        if file_name == "Save - Highscore.json":
            with open(file, "r") as record_file:
                record_file_content = record_file.read()
                load_record = int(float(record_file_content))
            return (load_record,)

        # If the file is the game save file, then return the last gamefield and highscore
        if file_name == "Save - Game.json":
            with open(file, "r") as game_file:
                game_file_content = game_file.read()
                # Get the last gamefield and highscore
                converted_content = json.loads(game_file_content)
                load_highscore = converted_content['highscore']
                temporary_gamefield = converted_content['gamefield']

                # Convert the list in temporary_gamefield to a numpy matrix
                load_gamefield = np.asarray(temporary_gamefield)

                # Make sure that the numbers in the matrix are permitted!
                permitted_num = (0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1042, 2048)
                # Make sure that the numbers are only integers and not float!
                load_highscore = int(float(load_highscore))

                for i, row in enumerate(load_gamefield):
                    for j, column in enumerate(row):
                        # Integer conversion
                        load_gamefield[i][j] = int(float(column))
                        # Replace invalid numbers with 0
                        if column not in permitted_num:
                            load_gamefield[i][j] = 0

                return (load_highscore, load_gamefield)

        return (False, "Invalid file!")
