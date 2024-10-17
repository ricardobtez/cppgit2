
project(cppgit2)
cmake_minimum_required(VERSION 3.19)

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# Add libgit2
find_package(libgit2 REQUIRED)
include(CMakePackageConfigHelpers)

# Sources for cppgit2
file(GLOB CPPGIT2_SOURCES "src/*.cpp")

# Version information
set(CPPGIT2_VERSION_MAJOR 0)
set(CPPGIT2_VERSION_MINOR 0)
set(CPPGIT2_VERSION_REV 1)
set(CPPGIT2_VERSION_STRING "${CPPGIT2_VERSION_MAJOR}.${CPPGIT2_VERSION_MINOR}.${CPPGIT2_VERSION_REV}")

# Build option for shared vs. static lib (Same option as for libgit2)
option(BUILD_SHARED_LIBS "Build Shared Library (OFF for Static)" OFF)

# Build shared/static library
if (BUILD_SHARED_LIBS)
    add_library(cppgit2 SHARED $<TARGET_OBJECTS:CPPGIT2_OBJECT_LIBRARY>)
    set_target_properties(cppgit2 PROPERTIES
    VERSION ${CPPGIT2_VERSION_STRING}
    SOVERSION ${CPPGIT2_VERSION_MINOR}
    WINDOWS_EXPORT_ALL_SYMBOLS ON)
else ()
    add_library(cppgit2 STATIC ${CPPGIT2_SOURCES})
endif ()
target_link_libraries(cppgit2 PUBLIC libgit2::libgit2)
target_include_directories(cppgit2 PUBLIC include)


# Build samples
file(GLOB SAMPLES "samples/*.cpp")
foreach(SAMPLE ${SAMPLES})
    get_filename_component(SAMPLE_EXE ${SAMPLE} NAME_WE)
    add_executable(${SAMPLE_EXE} ${SAMPLE})
    target_link_libraries(${SAMPLE_EXE} PUBLIC cppgit2)
endforeach()

# Build tests
enable_testing()
file(GLOB TESTS "test/*.cpp")
set_source_files_properties(test/main.cpp
    PROPERTIES
    COMPILE_DEFINITIONS DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN)
add_executable(cppgit2_test ${TESTS})
target_link_libraries(cppgit2_test PUBLIC cppgit2)
add_test(cppgit2_unittest cppgit2_test)

install(TARGETS cppgit2 DESTINATION lib/)
install(DIRECTORY include/cppgit2 DESTINATION include)
