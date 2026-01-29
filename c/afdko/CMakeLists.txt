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

# Link against the same libraries as _internal
# Phase 1: Just link what we need for tx and sfntedit
# tx is in shared, sfntedit is separate
target_link_libraries(afdko PRIVATE
    sfntedit
    shared
    antlr4_static
    ${CHOSEN_LIBXML2_LIBRARY}
)

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
