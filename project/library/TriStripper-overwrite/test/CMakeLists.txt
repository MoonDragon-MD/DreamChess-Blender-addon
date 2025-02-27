# Trova le librerie OpenGL e GLUT
find_package(OpenGL REQUIRED)
find_package(GLUT REQUIRED)

# Definisci l'eseguibile con i file sorgente
add_executable(TriStripper.Test gl_mesh.cpp gl_model.cpp gl_renderer.cpp high_res_timer.cpp main.cpp varrays_normalizer.cpp)

# Collega le librerie al target
target_link_libraries(TriStripper.Test TriStripper ${OPENGL_LIBRARIES} ${GLUT_LIBRARIES})

set(exe_name TriStripper.Test)

set(src_files
	fileio.h
	gl_mesh.cpp
	gl_mesh.h
	gl_model.cpp
	gl_model.h
	gl_renderer.cpp
	gl_renderer.h
	high_res_timer.cpp
	high_res_timer.h
	main.cpp
	varrays_normalizer.cpp
	varrays_normalizer.h
)

source_group("Source" FILES ${src_files})

include_directories(../include)
include_directories(${OPENGL_INCLUDE_DIRS} ${GLUT_INCLUDE_DIR})


set_target_properties(${exe_name} PROPERTIES DEBUG_POSTFIX ${CMAKE_DEBUG_POSTFIX})

add_definitions(-D FREEGLUT_STATIC)

set_target_properties(${exe_name} PROPERTIES VS_DEBUGGER_WORKING_DIRECTORY "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}")
