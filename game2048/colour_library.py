"""This file implements the colours used for the GUI"""

import pygame
import pygame.color
pygame.init()


class Colours:
    """
    COLOUR PALETTE in (r,g,b) format
    Theme: Beetlejuice - Dark, murky pastels with dominant purple undertones and green pops
    """

    # Main window colour
    LIGHT_LILAC = pygame.Color(239, 231, 255)

    # Numbers coulour
    LIGHT_TEXT     = pygame.Color(228, 214, 255)
    DARK_TEXT      = pygame.Color(52, 17, 63)

    # Tile colour
    DARK_PURPLE    = pygame.Color(43,25,61)
    NEON_PURPLE    = pygame.Color(138, 43, 226)
    TRUE_PURPLE    = pygame.Color(102, 0, 102)
    NEON_LILA      = pygame.Color(213, 128, 255)
    TUSCANY        = pygame.Color(197, 151, 157)
    EVERGREEN      = pygame.Color(76, 155, 99)
    GRAYISH_LILA   = pygame.Color(205, 165, 243)
    LILAC          = pygame.Color(182, 145, 255)
    RUSSIAN_VIOLET = pygame.Color(58, 1, 92)
    CHARCOAL       = pygame.Color(54, 70, 82)
    MINT           = pygame.Color(142, 208, 129)
    TRUE_GREEN     = pygame.Color(0, 179, 0)
    CHINESE_VIOLET = pygame.Color(111, 45, 189)
    MUTE_MAGENTA   = pygame.Color(179, 0, 179)
    DROP_PURPLE    = pygame.Color(83, 31, 232)

    # Dictionary matching value to color for view module
    color = {
        0: GRAYISH_LILA,
        2: LILAC,
        4: NEON_LILA,
        8: MINT,
        16: CHINESE_VIOLET,
        32: TRUE_GREEN,
        64: EVERGREEN,
        128: MUTE_MAGENTA,
        256: RUSSIAN_VIOLET,
        512: TRUE_PURPLE,
        1024: NEON_PURPLE,
        2048: DARK_PURPLE
    }
