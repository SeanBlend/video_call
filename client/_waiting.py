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

import time
import threading
import pygame
from _constants import *
from _elements import Button, Text, TextInput


class Waiting:
    def __init__(self, conn):
        self.conn = conn

        self.text_header = Text(FONT_LARGE.render("Meeting", 1, BLACK))
        self.text_attendees = Text(FONT_MED.render("Attendees", 1, BLACK))
        self.text_info = Text(FONT_MED.render("Info", 1, BLACK))
        self.text_chat = Text(FONT_MED.render("Chat", 1, BLACK))
        self.input_chat_send = TextInput(FONT_SMALL, "Send a message...", on_enter=self.chat_send)

        self.active = True
        self.chat_sending = False
        self.attendees = []
        self.info = {}
        self.chat_msgs = []
        self.is_host = False
        self.get_data_started = False

    def chat_send(self):
        while self.chat_sending:
            time.sleep(0.01)

        self.chat_sending = True
        text = self.input_chat_send.text
        if text.strip() != "":
            self.conn.send({"type": "chat_send", "msg": text})
        self.chat_sending = False

    def get_info(self):
        while self.active:
            try:
                self.conn.send({"type": "get", "data": "attendees"})
                self.attendees = self.conn.recv()["data"]
                self.conn.send({"type": "get", "data": "info"})
                self.info = self.conn.recv()["data"]
                self.conn.send({"type": "get", "data": "chat"})
                self.chat_msgs = self.conn.recv()["data"]
                self.conn.send({"type": "get", "data": "is_host"})
                self.is_host = self.conn.recv()["data"]
                time.sleep(0.1)

            except KeyError:
                return

    def draw(self, window, events, conn):
        if not self.get_data_started:
            threading.Thread(target=self.get_info).start()
            self.get_data_started = True
        width, height = window.get_size()

        window.fill(WHITE)
        self.text_header.draw(window, (width//2, 50))
        self.text_attendees.draw(window, (width//4, 150))
        self.text_info.draw(window, (width//2, 150))
        self.text_chat.draw(window, (width*3/4, 150))

        for i, attend in enumerate(self.attendees):
            Text(FONT_SMALL.render(attend, 1, BLACK)).draw(window, (width//4, 200+i*30))

        for i, key in enumerate(self.info):
            name = {"host": "Host", "key": "Key", "pword": "Password", "num_people": "Number of people"}[key]
            info = self.info[key]

            if name == "Password":
                reg_text = FONT_SMALL.render(f"Password: {info}", 1, BLACK)
                star_text = FONT_SMALL.render("Password: " + "*"*len(info), 1, BLACK)
                star_width = star_text.get_width()

                y_loc = 200 + i * 30 - 8
                x_min = width//2 - star_width//2 - 2
                x_max = width//2 + star_width//2 + 2
                mouse = pygame.mouse.get_pos()
                in_text = x_min <= mouse[0] <= x_max and y_loc-2 <= mouse[1] <= y_loc+18
                text = reg_text if in_text else star_text

                Text(text).draw(window, (width//2, 200+i*30))

            else:
                if name == "Host" and self.is_host:
                    name += " (You)"
                Text(FONT_SMALL.render(f"{name}: {info}", 1, BLACK)).draw(window, (width//2, 200+i*30))

        self.input_chat_send.draw(window, events, (width*3/4, height-75), (width//6, 50))
        for i, msg in enumerate(self.chat_msgs):
            time, person, string = msg
            string = f"{person}: {string}"
            if time != "":
                string = f"({time}) " + string
            Text(FONT_SMALL.render(string, 1, BLACK)).draw(window, (width*3/4, 200+i*30))
