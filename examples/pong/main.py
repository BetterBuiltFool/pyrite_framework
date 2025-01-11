"""
Pong is a very basic game, and thus makes for a good introduction to the basic usage of
Pyrite.

This example makes use of no image assets.
"""

import src.pyrite as pyrite


if __name__ == "__main__":
    with pyrite.Game(resolution=(800, 500)) as pong_game:
        pong_game.game_data.title = "Example Pong"
