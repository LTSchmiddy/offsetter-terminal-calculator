import rapidui
import pygame
from imgui import *

import main

class MainApp(rapidui.RapidApp):
    eval_scope: dict
    output: str
    input_str: str

    def on_init(self):
        self.window_size = (900, 720)
        self.use_style_file = True

        self.eval_scope = {}
        self.output = open("style.json", 'r').read()
        self.input_str = ""

    def on_window_created(self):
        pygame.display.set_caption("Offsetter: Python Calculator")


    def draw_menu(self):
        if begin_menu("File", True):
            # clicked_quit, selected_quit = menu_item("Quit", "", False, True)
            if menu_item("Quit", "", False, True)[1]:
                self.running = False

            end_menu()

        if begin_menu("Style", True):

            self.show_demo_window = menu_item(
                "Show Demo Window", "", self.show_demo_window, True
            )[1]
            self.show_style_window = menu_item(
                "Show Style Editor", "", self.show_style_window, True
            )[1]

            separator()

            if menu_item("Save Style To File", "", False, True)[0]:
                rapidui.save_style_json_file()

            if menu_item("Load Style From File", "", False, True)[0]:
                rapidui.load_style_json_file()

            end_menu()

    def draw_base_window(self):
        # columns(2, 'main_frame')

        # set_next_window_size(self.window_size[0], self.window_size[1])
        # set_next_window_position(50, 90)
        begin_child('history_view', self.window_size[0] - 20 , self.window_size[1] - 60)

        # for i in range(0, 100): text("hello")
        for i in self.output.split("\n"):
            text(i)

        end_child()
        text_in = input_text(
            'user_input',
            self.input_str,
            1000,
            INPUT_TEXT_ENTER_RETURNS_TRUE
        )

        if text_in[0]:
            print(text_in[1])

        # next_column()
        # columns(1)

    def get_history(self) -> str:
        return "poop"

    def handle_event(self, event: pygame.event.Event):
        pass

    def end(self):
        print("App ended...")





if __name__ == "__main__":
    app = MainApp()
    app.start()
