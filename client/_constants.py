#  ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import os
import json
import pygame
pygame.init()


if os.path.isfile("settings.json"):
    with open("settings.json", "r") as file:
        settings = json.load(file)
    IP = settings["ip"]
else:
    IP = input("IP address: ")

FPS = 60

BLACK = (0, 0, 0)
GRAY_DARK = (80, 80, 80)
GRAY = (128, 128, 128)
GRAY_LIGHT = (192, 192, 192)
WHITE = (255, 255, 255)

RED = (240, 70, 70)

FONT_SMALL = pygame.font.SysFont("ubuntu", 16)
FONT_MED = pygame.font.SysFont("ubuntu", 22)
FONT_LARGE = pygame.font.SysFont("ubuntu", 34)
