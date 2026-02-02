# AFDKO Unified Command Binary
#
# This builds the unified 'afdko' command dispatcher that routes
# subcommands to their appropriate implementations.
#
# Requires Python Development.Embed for embedding Python interpreter.
# If not available (e.g., manylinux wheel builds), this target is skipped.

# Check for Python embedding support before defining any targets
# We need the actual Python library (libpython) for embedding.
# In manylinux, only Development.Module is available (headers but no library).
# CMake caching can give false positives, so check Python_LIBRARY directly.
find_package(Python COMPONENTS Interpreter Development.Embed QUIET)
message(STATUS "Python_FOUND: ${Python_FOUND}")
message(STATUS "Python_Development.Embed_FOUND: ${Python_Development.Embed_FOUND}")
message(STATUS "Python_LIBRARY: ${Python_LIBRARY}")
message(STATUS "Python_LIBRARIES: ${Python_LIBRARIES}")
if(NOT Python_LIBRARY AND NOT Python_LIBRARIES)
    message(STATUS "Python library not available (no Development.Embed) - skipping afdko binary")
    return()
endif()
message(STATUS "Python embedding available - building afdko binary")

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
