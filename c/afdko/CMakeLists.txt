# AFDKO Unified Command Binary
#
# This builds the unified 'afdko' command dispatcher that routes
# subcommands to their appropriate implementations.
#
# Phase 1: C++ commands only (no Python embedding yet)

add_executable(afdko
    afdko_main.cpp
)

# Use C++17 like the rest of the project
set_property(TARGET afdko PROPERTY CXX_STANDARD 17)

# Link against all C++ tool libraries (same as _internal)
target_link_libraries(afdko PRIVATE
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

# Link against Python for embedding (fallback to Python dispatcher)
# Find Python with Development component (not just Development.Module)
find_package(Python COMPONENTS Interpreter Development REQUIRED)
target_link_libraries(afdko PRIVATE Python::Python)

# Add math library if needed (Linux)
if (HAVE_M_LIB)
    target_link_libraries(afdko PRIVATE m)
endif()

# Include directories from shared
target_include_directories(afdko PRIVATE
    ../shared/include
    ../spot/sfnt_includes
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
