from __future__ import absolute_import

import sys
import os

import pygame
import OpenGL.GL as gl

from imgui.integrations.pygame import PygameRenderer
import imgui

import json


version = "0.0.1"

class RapidApp:
    clock: pygame.time.Clock
    refresh_rate_hz: int
    window_size: tuple
    window_flags: int

    impl: PygameRenderer
    io: imgui.core._IO
    context: imgui.core._ImGuiContext
    context: imgui.core.GuiStyle

    def __init__(self, p_refresh_rate_hz=60, p_size=(800, 600)):

        self.refresh_rate_hz = p_refresh_rate_hz
        self.window_size = p_size
        self.window_flags = pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE

        self.quit_on_close = True
        self.use_base_window = True
        self.use_menu_bar = True
        self.use_gl_clear = True
        self.use_style_file = False

        self.show_style_window = False
        self.show_demo_window = False

        self.base_window_flags = imgui.core.WINDOW_MENU_BAR
        self.base_window_flags += imgui.core.WINDOW_NO_MOVE
        self.base_window_flags += imgui.core.WINDOW_NO_RESIZE
        self.base_window_flags += imgui.core.WINDOW_NO_COLLAPSE
        self.base_window_flags += imgui.core.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS
        self.base_window_flags += imgui.core.WINDOW_NO_FOCUS_ON_APPEARING
        self.base_window_flags += imgui.core.WINDOW_NO_TITLE_BAR

        self.clock = None
        self.context = None
        self.impl = None
        self.io = None
        self.style = None

        self.running = False
       
        self.on_init()
       
    def on_init(self):
        pass

    def start(self):
        if not pygame.get_init():
            pygame.init()

        pygame.display.set_caption("RapidApp Window")
        pygame.display.set_mode(self.window_size, self.window_flags)

        gl.glClearColor(1, 1, 1, 1)

        self.context = imgui.create_context()
        self.impl = PygameRenderer()
        self.io = imgui.get_io()
        self.io.display_size = self.window_size

        self.style = imgui.get_style()
        self.style.window_rounding = 0

        self.on_window_created()

        if self.use_style_file:
            load_style_json_file()

        self.clock = pygame.time.Clock()
        self.main_loop()

    def on_window_created(self):
        pass

    def main_loop(self):
        self.running = True

        while self.running:
            # Event Handling:
            for event in pygame.event.get():
                if event.type == pygame.QUIT and self.quit_on_close:
                    self.running = False

                self.impl.process_event(event)
                self.handle_event(event)

            # Drawing:
            imgui.new_frame()

            self.update()

            self.render()

            pygame.display.flip()
            self.clock.tick(self.refresh_rate_hz)

        if self.use_style_file:
            save_style_json_file()

        self.end()

    def handle_event(self, event: pygame.event.Event):
        pass

    def update(self):
        self.window_size = pygame.display.get_surface().get_size()

        if self.use_base_window:
            imgui.set_next_window_position(0, 0)
            imgui.set_next_window_size(self.window_size[0], self.window_size[1])
            imgui.begin("main", False, self.base_window_flags)
            if self.use_menu_bar and imgui.begin_menu_bar():
                self.draw_menu()
                imgui.end_menu_bar()

            self.draw_base_window()

            imgui.end()
        else:
            if self.use_menu_bar and imgui.begin_main_menu_bar():
                self.draw_menu()
                imgui.end_main_menu_bar()

        self.draw_windows()

        if self.show_style_window:
            self.show_style_window = imgui.begin("Style Editor", True)[1]
            imgui.show_style_editor()
            imgui.end()

        if self.show_demo_window:
            self.show_demo_window = imgui.show_demo_window(True)

    def draw_menu(self):
        pass

    def draw_base_window(self):
        pass

    def draw_windows(self):
        pass

    def render(self):
        # gl.glClearColor(1, 1, 1, 1)
        if self.use_gl_clear:
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        self.impl.render(imgui.get_draw_data())

    def end(self):
        pass



def set_style_dict(s_dict: dict):
    my_style = imgui.get_style()

    my_style.alpha = s_dict["alpha"]
    my_style.anti_aliased_fill = s_dict["anti_aliased_fill"]
    my_style.anti_aliased_lines = s_dict["anti_aliased_lines"]
    my_style.button_text_align = s_dict["button_text_align"]
    my_style.child_border_size = s_dict["child_border_size"]
    my_style.child_rounding = s_dict["child_rounding"]
    my_style.curve_tessellation_tolerance = s_dict["curve_tessellation_tolerance"]
    my_style.display_safe_area_padding = s_dict["display_safe_area_padding"]
    my_style.display_window_padding = s_dict["display_window_padding"]
    my_style.frame_border_size = s_dict["frame_border_size"]
    my_style.frame_padding = s_dict["frame_padding"]
    my_style.frame_rounding = s_dict["frame_rounding"]
    my_style.grab_min_size = s_dict["grab_min_size"]
    my_style.grab_rounding = s_dict["grab_rounding"]
    my_style.indent_spacing = s_dict["indent_spacing"]
    my_style.item_inner_spacing = s_dict["item_inner_spacing"]
    my_style.item_spacing = s_dict["item_spacing"]
    my_style.mouse_cursor_scale = s_dict["mouse_cursor_scale"]
    my_style.popup_border_size = s_dict["popup_border_size"]
    my_style.popup_rounding = s_dict["popup_rounding"]
    my_style.scrollbar_rounding = s_dict["scrollbar_rounding"]
    my_style.scrollbar_size = s_dict["scrollbar_size"]
    my_style.touch_extra_padding = s_dict["touch_extra_padding"]
    my_style.window_border_size = s_dict["window_border_size"]
    my_style.window_min_size = s_dict["window_min_size"]
    my_style.window_padding = s_dict["window_padding"]
    my_style.window_rounding = s_dict["window_rounding"]
    my_style.window_title_align = s_dict["window_title_align"]

    for color in range(0, imgui.COLOR_COUNT):
        my_style.colors[color] = s_dict["colors"][color]


def load_style_json_file(fname: str = "style.json"):
    if os.path.exists(fname) and os.path.isfile(fname):
        s_dict = json.load(open(fname, "r"))
        set_style_dict(s_dict)


def load_style_json_string(json_string: str):
    s_dict = json.loads(json_string)
    set_style_dict(s_dict)


def get_style_dict() -> dict:
    my_style = imgui.get_style()

    s_dict = {
        "alpha": my_style.alpha,
        "anti_aliased_fill": my_style.anti_aliased_fill,
        "anti_aliased_lines": my_style.anti_aliased_lines,
        "button_text_align": my_style.button_text_align,
        "child_border_size": my_style.child_border_size,
        "child_rounding": my_style.child_rounding,
        "curve_tessellation_tolerance": my_style.curve_tessellation_tolerance,
        "display_safe_area_padding": my_style.display_safe_area_padding,
        "display_window_padding": my_style.display_window_padding,
        "frame_border_size": my_style.frame_border_size,
        "frame_padding": my_style.frame_padding,
        "frame_rounding": my_style.frame_rounding,
        "grab_min_size": my_style.grab_min_size,
        "grab_rounding": my_style.grab_rounding,
        "indent_spacing": my_style.indent_spacing,
        "item_inner_spacing": my_style.item_inner_spacing,
        "item_spacing": my_style.item_spacing,
        "mouse_cursor_scale": my_style.mouse_cursor_scale,
        "popup_border_size": my_style.popup_border_size,
        "popup_rounding": my_style.popup_rounding,
        "scrollbar_rounding": my_style.scrollbar_rounding,
        "scrollbar_size": my_style.scrollbar_size,
        "touch_extra_padding": my_style.touch_extra_padding,
        "window_border_size": my_style.window_border_size,
        "window_min_size": my_style.window_min_size,
        "window_padding": my_style.window_padding,
        "window_rounding": my_style.window_rounding,
        "window_title_align": my_style.window_title_align,
    }

    save_colors = []
    for color in range(0, imgui.COLOR_COUNT):
        save_colors.append(my_style.colors[color])

    s_dict["colors"] = save_colors

    return s_dict


def save_style_json_file(fname: str = "style.json"):
    s_dict = get_style_dict()
    json.dump(s_dict, open(fname, "w"), indent=4, sort_keys=True)


def save_style_json_string() -> str:
    s_dict = get_style_dict()
    return json.dumps(s_dict, indent=4, sort_keys=True)
