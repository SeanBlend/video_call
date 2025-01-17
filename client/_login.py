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

import threading
import pygame
from _constants import *
from _elements import Button, Text, TextInput


class Login:
    def __init__(self):
        self.status = "CHOOSE"
        self.key = None
        self.error_msg = None

        self.text_header = Text(FONT_LARGE.render("Video Call", 1, BLACK))
        self.text_processing = Text(FONT_MED.render("Processing...", 1, BLACK))

        self.button_goto_join = Button(FONT_MED.render("Join a meeting", 1, BLACK))
        self.button_goto_create = Button(FONT_MED.render("Create a meeting", 1, BLACK))
        self.button_back = Button(FONT_MED.render("Back", 1, BLACK))
        self.input_name = TextInput(FONT_MED, "Your name")

        self.input_join_code = TextInput(FONT_MED, "Meeting code")
        self.input_join_pword = TextInput(FONT_MED, "Meeting password", True)
        self.button_join = Button(FONT_MED.render("Join meeting", 1, BLACK))

        self.input_create_pword = TextInput(FONT_MED, "Meeting password", True)
        self.button_create = Button(FONT_MED.render("Create meeting", 1, BLACK))

    def create_meeting(self, conn):
        conn.send({"type": "new_meeting", "name": self.input_name.text, "pword": self.input_create_pword.text})
        result = conn.recv()
        if result["type"] is None:
            self.create_meeting(conn)
            return

        if not result["status"]:
            self.error_msg = result["error"]
        return result["status"]

    def join_meeting(self, conn):
        conn.send({"type": "join_meeting", "name": self.input_name.text,
            "key": self.input_join_code.text, "pword": self.input_join_pword.text})
        result = conn.recv()
        if result["type"] is None:
            self.join_meeting(conn)
            return

        if not result["status"]:
            self.error_msg = result["error"]
        return result["status"]

    def draw(self, window, events, conn):
        width, height = window.get_size()

        window.fill(WHITE)
        self.text_header.draw(window, (width//2, height//5))
        if self.error_msg is not None:
            Text(FONT_MED.render(self.error_msg, 1, RED)).draw(window, (width//2, height//5+50))

        if self.status == "CHOOSE":
            if self.button_goto_join.draw(window, events, (width//2, height//2), (300, 50)):
                self.status = "JOIN"
            if self.button_goto_create.draw(window, events, (width//2, height//2+75), (300, 50)):
                self.status = "CREATE"

        elif self.status == "PROCESSING":
            self.text_processing.draw(window, (width//2, height//2))

        else:
            if self.button_back.draw(window, events, (width//2, height//3), (300, 50)):
                self.status = "CHOOSE"
                return

            self.input_name.draw(window, events, (width//2, height//2), (300, 50))
            if self.status == "JOIN":
                self.input_join_code.draw(window, events, (width//2, height//2+75), (300, 50))
                self.input_join_pword.draw(window, events, (width//2, height//2+150), (300, 50))
                if self.button_join.draw(window, events, (width//2, height//2+255), (300, 50)):
                    status = self.join_meeting(conn)
                    if status:
                        return "waiting"

            elif self.status == "CREATE":
                self.input_create_pword.draw(window, events, (width//2, height//2+75), (300, 50))
                if self.button_create.draw(window, events, (width//2, height//2+150), (300, 50)):
                    status = self.create_meeting(conn)
                    if status:
                        return "waiting"
