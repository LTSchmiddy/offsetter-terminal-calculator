cmake_minimum_required(VERSION 3.0.0)
project(offsetter-terminal-calculator VERSION 0.1.0)
cmake_policy(SET CMP0076 NEW)
set (CMAKE_CXX_STANDARD 17)

set(TARGET_NAME offsetter)
set(GUI_TARGET_NAME offsetter-gui)

set(Boost_USE_STATIC_LIBS OFF) 
set(Boost_USE_MULTITHREADED ON)  
set(Boost_USE_STATIC_RUNTIME OFF) 

find_package(Python3 3.8 COMPONENTS Interpreter Development REQUIRED)
find_package(SDL2 CONFIG REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLEW REQUIRED)

find_package(imgui CONFIG REQUIRED)
find_package(Boost 1.45.0 COMPONENTS filesystem REQUIRED) 
# if(Boost_FOUND)

include_directories(${Sdl2_INCLUDE_DIRS}) 
include_directories(${OpenGL_INCLUDE_DIRS}) 
include_directories(${Glew_INCLUDE_DIRS}) 
include_directories(${Imgui_INCLUDE_DIRS}) 

include_directories(${Python3_INCLUDE_DIRS}) 
include_directories(${Boost_INCLUDE_DIRS}) 

add_executable(${TARGET_NAME} ./src/cpp/main.cpp)
add_executable(${GUI_TARGET_NAME} )
include_directories(./src/cpp/)
add_subdirectory(./src/cpp/)

# add_library(${TARGET_NAME} SHARED test.cpp)
# add_library(${TARGET_NAME} test.cpp)
# mcppt_target_triplet(${TARGET_NAME} "static")
# mcppt_target_triplet(${GUI_TARGET_NAME}, "static")

# GUI ONLY:
target_link_libraries(${GUI_TARGET_NAME} SDL2::SDL2main SDL2::SDL2)
target_link_libraries(${GUI_TARGET_NAME} ${OpenGL_LIBRARIES})
target_link_libraries(${GUI_TARGET_NAME} GLEW::GLEW)
target_link_libraries(${GUI_TARGET_NAME} imgui::imgui)

message(STATUS ${OpenGL_LIBRARIES})

# Common:
target_link_libraries(${TARGET_NAME} ${Python3_LIBRARIES})
target_link_libraries(${GUI_TARGET_NAME} ${Python3_LIBRARIES})

message(STATUS ${Python3_INCLUDE_DIRS})
message(STATUS ${Python3_LIBRARIES})

target_link_libraries(${TARGET_NAME} ${Boost_LIBRARIES})
target_link_libraries(${GUI_TARGET_NAME} ${Boost_LIBRARIES})
# message(STATUS ${Python3_INCLUDE_DIRS}) 
# endif()

set_target_properties(${TARGET_NAME}
    PROPERTIES
    ARCHIVE_OUTPUT_DIRECTORY "./arc/cli/"
    LIBRARY_OUTPUT_DIRECTORY "./lib/cli/"
    RUNTIME_OUTPUT_DIRECTORY "./bin/cli/"
)

set_target_properties(${GUI_TARGET_NAME}
    PROPERTIES
    ARCHIVE_OUTPUT_DIRECTORY "./arc/gui/"
    LIBRARY_OUTPUT_DIRECTORY "./lib/gui/"
    RUNTIME_OUTPUT_DIRECTORY "./bin/gui/"
)


set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
