# AFDKO Unified Command Binary
#
# This builds the unified 'afdko' command dispatcher that routes
# subcommands to their appropriate implementations.
#
# Requires Python Development.Embed for embedding Python interpreter.
# On Linux wheel builds, set AFDKO_BUILD_BINARY=OFF to skip this.

# Find Python with embedding support
find_package(Python COMPONENTS Interpreter Development.Embed REQUIRED)

add_executable(afdko
    afdko_main.cpp
)

# Use C++17 like the rest of the project
set_property(TARGET afdko PROPERTY CXX_STANDARD 17)

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
    antlr4_static
    ${CHOSEN_LIBXML2_LIBRARY}
)

# Link against Python for embedding
target_link_libraries(afdko PRIVATE Python::Python)

# Add math library if needed (Linux)
if (HAVE_M_LIB)
    target_link_libraries(afdko PRIVATE m)
endif()

# Include directories from shared and generated files
target_include_directories(afdko PRIVATE
    ../shared/include
    ../spot/sfnt_includes
    ${CMAKE_BINARY_DIR}/c/shared  # For generated version.h
)

# Ensure libxml2 is built first if needed
if (${NEED_LIBXML2_DEPEND})
    add_dependencies(afdko ${LIBXML2_TARGET})
endif()

# Install to bin directory
# scikit-build-core will handle placing this in the right location in the wheel
install(TARGETS afdko
    RUNTIME DESTINATION ${SKBUILD_SCRIPTS_DIR}
)
