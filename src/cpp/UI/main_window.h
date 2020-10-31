#include <stdio.h>
#include <string>
#include <vector>

#include <imgui.h>
#include <imgui_impl_sdl.h>
#include <imgui_impl_opengl3.h>

#include <SDL2/SDL.h>

#include "app_window.h"

#define MAIN_WINDOW_INPUT_BUFFER_SIZE 64

class MainWindow : public AppWindow {
public:
    MainWindow();
    ~MainWindow();
    
    std::string window_name = "##main";
    ImGuiWindowFlags window_flags = 0
        | ImGuiWindowFlags_MenuBar 
        | ImGuiWindowFlags_NoBringToFrontOnFocus
        | ImGuiWindowFlags_NoCollapse
        | ImGuiWindowFlags_NoMove
        | ImGuiWindowFlags_NoResize
        | ImGuiWindowFlags_NoTitleBar;


    std::vector<std::string> log;
    std::vector<std::string> cmd_history;


    // Methods:
    void update() override;
    void draw() override;

    void focus_input();

    std::string get_input_string();
    void set_input_string(std::string value, bool use_override);

    int get_history_pos();
    void set_history_pos(int value);
private:
    // Variables:
    const std::string input_label = "_input";
    int win_x, win_y;

    bool override_string_set;
    std::string temp_input_string;
    std::string input_string;

    // Menu state variables:
    bool menubar_file_open;
    
    // Navigation control variables;
    bool _focus_input;
    int history_pos = 0;
    ImGuiInputTextFlags input_text_flags = 0
        | ImGuiInputTextFlags_EnterReturnsTrue
        | ImGuiInputTextFlags_CallbackHistory;

    // Methods:
    void draw_menu_bar();
    void draw_log();
    void draw_input();

    void on_run();
    // int input_callback(ImGuiInputTextCallbackData* data);
};

