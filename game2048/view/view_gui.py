from .interface_view import InterfaceView
from ..event_manager import EventManager, Screen
from ..model import Model
from ..colour_library import Colours
import numpy as np
import pygame as pg
import time
import math
from ..database import Database


db = Database()


class ViewGUI(InterfaceView):
    """This class implements a graphic output to display the game 2048"""
    def __init__(self, ev_manager: EventManager, game: Model, bci: bool):
        """Constructs the output GUI window

        Parameters
        ----------
        ev_manager: EventManager
            controls communication with other modules
        game: Model
            Reference to the model instance
        bci: bool
            checks if the bci controller is active
        """
        super().__init__(ev_manager, game)

        self._screen_size = (700, 700)
        self._font = pg.font.Font("NotoSans.ttf", 24)
        pg.init()
        self._speed = pg.time.Clock()
        self._screen = pg.display.set_mode(self._screen_size, pg.RESIZABLE)
        pg.display.set_caption('Project2048')
        self._bci = bci
        self._count = 0
        self._shadow_distance = (-2.5, 2.5)

    def _coord(self, x, y) -> (int, int):
        """Transfers generalized coordinates (10x10) to actual screen (pixels)"""
        w, h = self._screen_size
        cell = min(w, h) / 10
        gap = abs(w - h) / 2
        if w >= h:
            return gap + x * cell, y * cell
        else:
            return x * cell, gap + y * cell

    def _dim(self, w, h) -> (int, int):
        """Transfers rectangle size (in 10x10) to screen (pixels)"""
        cell = min(self._screen_size) / 10
        return w * cell, h * cell

    def _quit(self, field: np.ndarray, highscore: int) -> None:
        """Ends the game"""
        self._screen.fill(Colours.DARK_PURPLE)
        db.create_save(matrix=field, current_highscore=highscore)

        text = self._font.render("BYE BYE!", True, Colours.LILAC)
        text2 = self._font.render("See you soon (space cowboy) ;)", True, Colours.LILAC)
        text3 = self._font.render("Your highscore: " + str(highscore), True, Colours.LILAC)
        self._screen.blit(text, self._coord(3, 3))
        self._screen.blit(text2, self._coord(2.5, 4))
        self._screen.blit(text3, self._coord(2.5, 6))

        pg.display.update()
        time.sleep(3)
        pg.quit()


    def _draw(self) -> None:
        """Outputs the current Screen"""
        self._screen.fill(Colours.LIGHT_LILAC)
        self._screen_size = self._screen.get_size()

        super()._draw()

        pg.display.update()


    def _add_drop_shadow(self,
                        text, colour,
                        shadow_distance,
                        shadow_colour=Colours.DROP_PURPLE,
                        shadow_alpha = 0):
        """Renders a given text with a drop shadow"""

        dx = shadow_distance[0]
        dy = shadow_distance[1]

        text_size = self._font.size(text)
        # Create transparent surface
        surface = pg.Surface((text_size[0] + abs(dx), text_size[1] + abs(dy)), pg.SRCALPHA)
        # Render the text with the shadow colour & set transparency
        shadow_surface = self._font.render(text, True, shadow_colour)
        shadow_surface.set_alpha(shadow_alpha)
        text_surface = self._font.render(text, True, colour)
        # Layers: shadow text & text -> transparent surface -> screen
        surface.blit(shadow_surface, (max(0, dx), max(0, dy)))
        surface.blit(text_surface, (max(0, -dx), max(0, -dy)))

        return surface


    def _print_pause(self) -> None:
        """Displays the pause screen"""

        text_surf = self._add_drop_shadow("PAUSE",Colours.DARK_PURPLE, self._shadow_distance)
        self._screen.blit(text_surf, self._coord(4.5, 3))

        text_surf = self._add_drop_shadow(" s ~ continue", Colours.DARK_PURPLE, self._shadow_distance)
        self._screen.blit(text_surf, self._coord(2.5, 4))

        text_surf = self._add_drop_shadow(" r ~ restart", Colours.DARK_PURPLE, self._shadow_distance)
        self._screen.blit(text_surf, self._coord(2.5, 4.5))

        text_surf = self._add_drop_shadow(" q ~ exit", Colours.DARK_PURPLE, self._shadow_distance)
        self._screen.blit(text_surf, self._coord(2.5, 5))


    def _print_instructions(self) -> None:
        """Displays a welcome message for players."""
        text_surf = self._add_drop_shadow("WELCOME TO 2048!", Colours.MUTE_MAGENTA, self._shadow_distance)
        self._screen.blit(text_surf, self._coord(3, 3))

        text_surf = self._add_drop_shadow("Your aim in this game is to reach", Colours.DARK_PURPLE, self._shadow_distance)
        self._screen.blit(text_surf, self._coord(1.5, 4))

        text_surf = self._add_drop_shadow("the number 2048 on one of the tiles.", Colours.DARK_PURPLE, self._shadow_distance)
        self._screen.blit(text_surf, self._coord(1.5, 4.5))

        text_surf = self._add_drop_shadow("You should do so by cleverly sliding", Colours.DARK_PURPLE, self._shadow_distance)
        self._screen.blit(text_surf, self._coord(1.5, 5))

        text_surf = self._add_drop_shadow("the tiles up, down, left or right.", Colours.DARK_PURPLE, self._shadow_distance)
        self._screen.blit(text_surf, self._coord(1.5, 5.5))

        text_surf = self._add_drop_shadow("Good luck and have fun! :)", Colours.CHINESE_VIOLET, self._shadow_distance)
        self._screen.blit(text_surf, self._coord(2.5, 6))

        text_surf = self._add_drop_shadow("PRESS for:", Colours.DARK_TEXT, self._shadow_distance)
        self._screen.blit(text_surf, self._coord(1.5, 7))

        text_surf = self._add_drop_shadow("s ~ continue", Colours.MUTE_MAGENTA, self._shadow_distance)
        self._screen.blit(text_surf, self._coord(4, 7.5))

        text_surf = self._add_drop_shadow("OR", Colours.DARK_TEXT, self._shadow_distance)
        self._screen.blit(text_surf, self._coord(5, 8))

        text_surf = self._add_drop_shadow("q ~ exit", Colours.MUTE_MAGENTA, self._shadow_distance)
        self._screen.blit(text_surf, self._coord(4, 8.5))



    def _print_game(self, matrix: np.ndarray, score: int, record: int) -> None:
        """
        Displays a given matrix, high score, record score and mini tutorial in the window.

        Parameter
        ---------
        matrix: np.ndarray
            The current _game _field.
        score: int
            The current high score.
        """
        def print_score() -> None:
            """Print the score and the record on the screen"""
            score_rect = pg.Rect(self._coord(3, 2), self._dim(4, 1))
            score_text = self._add_drop_shadow('Score: ' + str(int(score)), Colours.DARK_TEXT, self._shadow_distance)
            temp_score_text = "Score: " + str(int(score))
            temp_record_text = "Record: " + str(int(record))
            score_text = self._add_drop_shadow(temp_score_text + "   " + temp_record_text, Colours.DARK_TEXT, self._shadow_distance)

            score_rect = score_text.get_rect(center=score_rect.center)
            self._screen.blit(score_text, score_rect)

        def print_tiles() -> None:
            """Print tiles from gamefield on the screen"""
            for i in range(4):
                for j in range(4):
                    value = matrix[i][j]
                    # draw tiles of appropriate colour
                    tile = pg.Rect(self._coord(3+j, 3+i), self._dim(1, 1))
                    pg.draw.rect(self._screen, Colours.color[value], tile, 0, 20)
                    # put numbers on tiles
                    if value > 0:
                        value_length = len(str(value))
                        tile_font = pg.font.Font("NotoSans.ttf", 50 - (5 * value_length))
                        value_text = tile_font.render(str(int(value)), True,
                                                      Colours.LIGHT_TEXT if value > 32 else Colours.DARK_TEXT)
                        value_rect = value_text.get_rect(center=tile.center)
                        self._screen.blit(value_text, value_rect)

        def print_options() -> None:
            """Print instructions on the possible keys to press"""
            text_rect = pg.Rect(self._coord(3, 8), self._dim(4, 1))
            text_text = self._add_drop_shadow("use arrows to slide  |  press p to pause", Colours.DARK_TEXT, self._shadow_distance)
            text_rect = text_text.get_rect(center=text_rect.center)
            self._screen.blit(text_text, text_rect)


        def print_flicker() -> None:
            """Print a flickering field in current state"""
            up = pg.Rect(self._coord(3, 0), self._dim(4, 2))
            down = pg.Rect(self._coord(3, 8), self._dim(4, 2))
            left = pg.Rect(self._coord(0, 3), self._dim(2, 4))
            right = pg.Rect(self._coord(8, 3), self._dim(2, 4))
            pg.draw.rect(self._screen, self._flicker(6), up)
            pg.draw.rect(self._screen, self._flicker(8), right)
            pg.draw.rect(self._screen, self._flicker(10), down)
            pg.draw.rect(self._screen, self._flicker(15), left)

        print_score()
        print_tiles()

        # test flicker function without bci by replacing the following part by this:
        # print_flicker()
        # self._count += 1

        if self._bci:
            print_flicker()
            self._count += 1
        else:
            print_options()


    def _flicker(self, f: int) -> (int, int, int):
        """Returns the colour value of a flickering field

        Parameters
        ----------
        f: int
            flicker frequency in Hertz"""
        n: int = int(255 * 0.5 * (1 + math.sin((self._count / 60) * f * 2 * math.pi)))
        return (n, n, n)


    def _print_final(self, score: int, record: int) -> None:
        """
        Displays the ending screen & the reason why game has ended.

        Parameters
        ----------
        score: int
            The current high score.
        """
        if self._game_state is Screen.WIN:
            text = self._add_drop_shadow("You reached a 2048 tile and won!", Colours.CHINESE_VIOLET, self._shadow_distance)
            self._screen.blit(text, self._coord(2, 3))
        if self._game_state is Screen.LOSE:
            text = self._add_drop_shadow("You lost!", Colours.DARK_TEXT, self._shadow_distance)
            self._screen.blit(text, self._coord(2, 3))

        text = self._add_drop_shadow("Your Final Score: " + str(int(score)), Colours.DARK_TEXT, self._shadow_distance)
        self._screen.blit(text, self._coord(1, 4))

        text = self._add_drop_shadow("The Current Record: " + str(int(record)), Colours.DARK_TEXT, self._shadow_distance)
        self._screen.blit(text, self._coord(1, 5))

        text = self._add_drop_shadow("Press s to start new game  or  q to quit", Colours.DARK_TEXT, self._shadow_distance)
        self._screen.blit(text, self._coord(1, 6))

