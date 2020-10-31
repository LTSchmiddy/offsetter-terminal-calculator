add_subdirectory("./UI")
add_subdirectory("./python_sys")

target_sources(${GUI_TARGET_NAME}
    PUBLIC
    "./gui-main.h"
    "./gui-main.cpp" 
)
