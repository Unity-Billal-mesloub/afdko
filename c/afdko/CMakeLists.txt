# AFDKO Unified Command Binary
#
# This builds the unified 'afdko' command dispatcher that routes
# subcommands to their appropriate implementations.
#
# Requires Python Development.Embed for embedding Python interpreter.
# On Linux wheel builds, set AFDKO_COMMAND_USE_WRAPPER=ON to use the
# Python wrapper instead of building this binary.

# Find Python with embedding support
# Note: Development.Embed is needed for embedding Python interpreter in C++
find_package(Python COMPONENTS Interpreter Development.Embed QUIET)

if(NOT Python_FOUND)
    message(FATAL_ERROR
        "Cannot build afdko C++ binary: Python Development.Embed not found.\n"
        "\n"
        "The afdko binary requires Python development headers with embedding support.\n"
        "This is typically unavailable in manylinux containers and some minimal Python\n"
        "installations.\n"
        "\n"
        "WORKAROUND: Use the Python wrapper instead of the C++ binary:\n"
        "  - Set environment variable: AFDKO_COMMAND_USE_WRAPPER=ON\n"
        "  - Then rebuild/reinstall AFDKO\n"
        "\n"
        "Example:\n"
        "  export AFDKO_COMMAND_USE_WRAPPER=ON\n"
        "  pip install --force-reinstall --no-cache-dir afdko\n"
        "\n"
        "Note: The Python wrapper has slightly slower startup time but identical\n"
        "functionality. Most users won't notice the difference.\n"
        "\n"
        "To install Python development headers on your system:\n"
        "  - Debian/Ubuntu: sudo apt-get install python3-dev\n"
        "  - RHEL/Fedora: sudo dnf install python3-devel\n"
        "  - macOS: Install full Python from python.org (not just Xcode CLI tools)\n"
        "  - Windows: Ensure 'Development' features are checked in Python installer\n"
    )
endif()

add_executable(afdko
    afdko_main.cpp
)

# Link against all C++ tool libraries (same as _internal)
target_link_libraries(afdko PRIVATE
    afdko_version
    detype1
    type1
    addfeatures
    spot
    sfntedit
    sfntdiff
    mergefonts
    rotatefont
    shared
    afdko::antlr4
    LibXml2::LibXml2
)

# Link against Python for embedding
target_link_libraries(afdko PRIVATE Python::Python)

# Add math library if needed (Linux)
if (HAVE_M_LIB)
    target_link_libraries(afdko PRIVATE m)
endif()

# Add pthread if needed (Linux with ANTLR4 static linking)
if (CMAKE_USE_PTHREADS_INIT)
    target_link_libraries(afdko PRIVATE Threads::Threads)
endif()

# Include directories for spot's sfnt_includes (shared provides ../shared/include and version.h)
target_include_directories(afdko PRIVATE
    ../spot/sfnt_includes
)

# Install to bin directory
# scikit-build-core will handle placing this in the right location in the wheel
install(TARGETS afdko
    RUNTIME DESTINATION ${SKBUILD_SCRIPTS_DIR}
)
