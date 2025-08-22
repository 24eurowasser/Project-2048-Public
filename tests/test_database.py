from game2048.database import Database
import numpy as np
import pathlib
import os
from game2048.arguments import Logging

# Set logging to true
file_name = "Config - Logging.txt"
current_path = pathlib.Path(__file__).parent.resolve()
root_path = current_path.parent
file_path = os.path.join(root_path, file_name)

file_content = "True"
with open(file_path, "w") as file:
    file.write(file_content)

# Get the current path of the running code
# .../project2048/tests/
current_path = pathlib.Path(__file__).parent.resolve()

class Helpers(Database):

    def class_test_create_folder(self):
        # Create an object of the class DatabaseText
        db = Database()
        # Use the function we want to test
        folder_path = db._create_folder()
        return os.path.exists(folder_path)

    def class_test_create_temp_logs(self):
        # Create an object of the class DatabaseText
        db = Database()
        # Use the function we want to test
        file_paths = db._create_temp_logs()
        path_system = file_paths[0]
        path_game = file_paths[1]
        result = os.path.exists(path_system) and os.path.exists(path_game)
        # Delete the just created files
        os.remove(path_system)
        os.remove(path_game)
        return result

    def class_test_finalize_temp_logs(self):
        # Create an object of the class DatabaseText
        db = Database()
        # Use the functions we want to test
        # Enter either 'log' or 'savestate'
        db._create_temp_logs()
        file_paths = db._finalize_log_files()
        path_system = file_paths[0]
        path_game = file_paths[1]

        with open(path_system, "w") as file:
            file.write("This is a test file.")

        with open(path_game, "w") as file:
            file.write("This is another test file.")

        result = os.path.exists(path_system) and os.path.exists(path_game)
        # Delete the just created files
        os.remove(path_system)
        os.remove(path_game)
        return result

    def class_test_is_file_too_big(self):
        # Create an object of the class DatabaseText
        db = Database()
        # Create a path for 2 test files
        big_path = os.path.join(current_path, "prop_big_file.txt")
        small_path = os.path.join(current_path, "prop_small_file.txt")

        with open(big_path, "a") as big_file:
            with open(small_path, "a") as small_file:
                file_size = 1024 ** 2 * 11
                for i in range(file_size):
                    # Create a big file that is around 11 MB big
                    big_file.write("0")
                    if i < 1000000:
                        # Create a small file that is around 1 MB big
                        small_file.write("1")

        print("A warning message is expected.")
        result = db._is_file_too_big(big_path, "0") and not db._is_file_too_big(small_path, "1")
        # Delete the just created files
        os.remove(big_path)
        os.remove(small_path)
        return result

    def class_test_matrix_to_markdown(self):
        # Create an object of the class DatabaseText
        class_obj = Database()
        # Create a test matrix
        test_matrix = np.array([[2, 4, 8, 16], [4, 8, 16, 32], [8, 16, 32, 64], [16, 32, 64, 128]])
        # Use the function we want to test
        result_string = class_obj._matrix_to_markdown(test_matrix)

        # The result string should look like this:
        line1 = "| - | - | - | - |"
        line2 = "| :---: | :---: | :---: | :---: |"
        line3 = "| 2 | 4 | 8 | 16 | "
        line4 = "| 4 | 8 | 16 | 32 | "
        line5 = "| 8 | 16 | 32 | 64 | "
        line6 = "| 16 | 32 | 64 | 128 | "

        comparison_string = line1 + "\n" + line2 + "\n" + line3 + "\n" + line4 + "\n" + line5 + "\n" + line6
        return result_string == comparison_string

    def class_test_savestate_functions(self):
        # Create a object of the class DatabaseText
        db = Database()
        # Create a test matrix
        source_matrix = np.array([[2, 4, 8, 16], [4, 8, 16, 32], [8, 16, 32, 64], [16, 32, 64, 128]])
        # Create a test highscore
        source_highscore = 12
        # Create a save file and store the path
        file_paths = db.create_save(matrix=source_matrix, current_highscore=source_highscore)

        # Read the save file content
        save_game_path = file_paths[0]
        save_record_path = file_paths[1]

        read_save = db.read_save(save_game_path)
        loaded_highscore = read_save[0]
        loaded_gamefield = read_save[1]
        read_record = db.read_save(save_record_path)
        loaded_record = read_record[0]

        # Now compare the source and the loaded content
        equal_highscore = source_highscore == loaded_highscore
        equal_gamefield = (source_matrix == loaded_gamefield).all()
        equal_record = loaded_record == source_highscore
        result = equal_highscore and equal_gamefield and equal_record

        # Delete the just created files
        os.remove(save_game_path)
        os.remove(save_record_path)
        return result


# Get the protected functions
t = Helpers()


def test_create_folder():
    assert t.class_test_create_folder()


def test_create_temp_file():
    assert t.class_test_create_temp_logs()


def test_finalize_temp_file():
    assert t.class_test_finalize_temp_logs()


def test_is_file_too_big():
    assert t.class_test_is_file_too_big()


def test_matrix_to_markdown():
    assert t.class_test_matrix_to_markdown()


def test_savestate_functions():
    assert t.class_test_savestate_functions()
