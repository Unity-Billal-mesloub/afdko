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

# Include directories for spot's sfnt_includes (shared provides ../shared/include and version.h)
target_include_directories(afdko PRIVATE
    ../spot/sfnt_includes
)

# Install to bin directory
# scikit-build-core will handle placing this in the right location in the wheel
install(TARGETS afdko
    RUNTIME DESTINATION ${SKBUILD_SCRIPTS_DIR}
)
