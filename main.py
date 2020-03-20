#!/usr/bin/python3
# coding : utf-8

from game.engine import GameEngine


def main(zoom, u_size, nb_elements):
    game = GameEngine(zoom, u_size, nb_elements)
    game.run()


if __name__ == "__main__":
    zoom = 3
    u_size = 20*zoom  # unit size (nb pixel*zoom)
    nb_elements = (15, 15)  # nb elements (nb_lines, nb_columns)
    main(zoom, u_size, nb_elements)
