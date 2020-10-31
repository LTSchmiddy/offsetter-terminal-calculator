#include <stdio.h>

#include <Python.h>
#include <imgui.h>
#include <imgui_impl_sdl.h>
#include <imgui_impl_opengl3.h>

#include "app_window.h"
#include "gui-main.h"


AppWindow::AppWindow() {}
AppWindow::AppWindow(std::string p_window_name) {
    window_name = p_window_name;
}
AppWindow::~AppWindow() {}

void AppWindow::handle_event(SDL_Event* event){}


void AppWindow::update() {
    ImGui::Begin(window_name.c_str(), &open, window_flags);
    draw();
    ImGui::End();
}


void AppWindow::draw() {}
