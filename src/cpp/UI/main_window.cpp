#include <stdio.h>
#include <iostream>
#include <string>
#include <algorithm>
#include <math.h>

#include <boost/foreach.hpp>

#include <imgui.h>
#include <imgui_impl_sdl.h>
#include <imgui_impl_opengl3.h>

// #include "app_window.h"
#include "python_sys/py_loader.h"

#include "main_window.h"
#include "gui-main.h"

using namespace ImGui;

// char input_buffer[MAIN_WINDOW_INPUT_BUFFER_SIZE];

MainWindow::MainWindow() {}

MainWindow::~MainWindow() {}

void MainWindow::update() {
    SDL_GetWindowSize(sdl_window, &win_x, &win_y);

    SetNextWindowPos(ImVec2(0, 0));
    SetNextWindowSize(ImVec2((float)win_x, (float)win_y));    
    Begin(window_name.c_str(), &open, window_flags);
    draw();
    End();
}


void MainWindow::draw() {
    draw_menu_bar();
    draw_log();
    draw_input();
}

void MainWindow::focus_input(){
    _focus_input = true;
}

std::string MainWindow::get_input_string() {
    return input_string;
}
void MainWindow::set_input_string(std::string value, bool use_override = true) {
    temp_input_string = value;
    override_string_set = use_override;
    
}

int MainWindow::get_history_pos(){
    return history_pos;
}
void MainWindow::set_history_pos(int value){
    if (0 == (int)cmd_history.size()) {
        history_pos = 0;
        return;
    }
    history_pos = std::clamp(value, 0, (int)cmd_history.size() - 1);
    set_input_string(cmd_history[history_pos]);
}

// Private:
void MainWindow::draw_menu_bar() {
    if (BeginMenuBar()) {
        if (BeginMenu("File", &menubar_file_open)) {
            Checkbox("Show Demo Window", &show_demo_window);
            Checkbox("Show Style Window", &show_style_window);
            
            if (Button("Exit")) {
                quit_app = true;
            }
            
            EndMenu();   
        }
        EndMenuBar();
    }
}

void MainWindow::draw_log() {
    BeginChild(
        "child_log", 
        ImVec2(-1.0f, -30.0f), 
        true,
        ImGuiWindowFlags_AlwaysVerticalScrollbar
    );

    PushItemWidth(-1.0f);
    for (int i = 0; i < log.size(); i++) {
        std::string* cmd_str = &log[i];
        char* cbuf = (char*)cmd_str->c_str();

        InputText(
            (std::string(" ##history_item_") + std::to_string(i)).c_str(),
            cbuf,
            cmd_str->size(),
            0
            | ImGuiInputTextFlags_ReadOnly
            | ImGuiInputTextFlags_AutoSelectAll
            | ImGuiInputTextFlags_NoUndoRedo

        );
    }
    PopItemWidth();
    // Text(std::to_string(history_pos).c_str());
    // Text(temp_input_string.c_str());
    EndChild();
}


// Child window for the input area:
static int _input_callback(ImGuiInputTextCallbackData* data);
void MainWindow::draw_input() {
        
    BeginChild(
        "child_input",
        ImVec2(-1.0f, -5.0f), 
        false, 
        ImGuiWindowFlags_NoScrollbar | ImGuiWindowFlags_NoScrollWithMouse
    );
    
    PushItemWidth(-80.0f);
    if (_focus_input) {
        // enters++;
        _focus_input = false;
        ImGui::SetKeyboardFocusHere();
    }

    char* local_input_buffer;

    if (override_string_set) {
        override_string_set = false;
        std::cout << "override ";
        std::cout << history_pos;
        std::cout << " ";
        std::cout << temp_input_string;
        std::cout << "\n";
        input_string = temp_input_string.c_str();
        // local_input_buffer = (char*)temp_input_string.c_str();
    }
    // else {
        local_input_buffer = (char*)input_string.c_str();
    // }
    
    bool run_text = InputText(
        (window_name + input_label + std::to_string(history_pos)).c_str(),
        local_input_buffer,
        MAIN_WINDOW_INPUT_BUFFER_SIZE,
        input_text_flags,
        _input_callback,
        this
    );

    input_string = std::string(local_input_buffer);

    SameLine();
    PopItemWidth();
    bool run_btn = Button("Run", ImVec2(-1 , 0));

    EndChild();

    if (run_text ||run_btn) {
        on_run();
    }
}

static int _input_callback(ImGuiInputTextCallbackData* data) {
    MainWindow* mwin = (MainWindow*) data->UserData;
    // mwin->input_string = "HELLO";

    if (data->EventFlag == ImGuiInputTextFlags_CallbackHistory){
        // 3 is up, 4 is down:

        if (data->EventKey == 3){ mwin->set_history_pos(mwin->get_history_pos()-1);} // Prev
        else if (data->EventKey == 4){ mwin->set_history_pos(mwin->get_history_pos()+1);} // Next
        mwin->focus_input();

    }
    return 0;
}

void MainWindow::on_run() {
    // Refocus the text input once we're done:
    _focus_input = true;
    cmd_history.emplace_back(input_string.c_str());
    history_pos = (int)cmd_history.size();

    std::string py_result = py_eval_calc_simple(input_string);
    log.emplace_back(input_string.c_str());
    log.emplace_back(py_result.c_str());
    
    input_string = "";
}