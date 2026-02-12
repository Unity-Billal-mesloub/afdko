5.0.0 (unreleased)
------------------
**Major restructuring: Unified command interface, massive C++ modernization, and build system overhaul**

This is a major release with extensive architectural changes including a substantial C→C++ conversion. While we have worked to maintain compatibility, with this much change there are likely to be regressions. Users not in a position to thoroughly verify their output may want to wait for 5.0.1 or 5.0.2 before upgrading.

### Summary of Command and Interface Changes

#### Unified Command Interface
- **New primary interface**: All AFDKO tools are now accessed through `afdko <command>` syntax
  ```bash
  afdko makeotf -r
  afdko tx -dump font.otf
  afdko spot -Proof font.otf
  ```
- **Deprecated wrappers**: Individual command wrappers (e.g., `makeotf`, `tx`, `spot`) are deprecated with gradual rollout:
  - By default, wrappers work silently (opt-in warnings with `AFDKO_WRAPPER_MODE=warn`)
  - Two-tier removal timeline: less-used commands will be present for at least 6 months, commonly-used commands for at least 12 months
  - Wrappers will start to omit warnings in a future release
  - See [docs/Deprecation_System.md](docs/Deprecation_System.md) for details

#### makeotfexe → addfeatures Transition
- **Variable Font Support**: `addfeatures`, which replaces `makeotfexe`, supports more direct building of variable fonts:
  - Accepts CFF2 table as input in addition to CFF
  - Enhanced feature file syntax for direct specification of variable values
    - See [docs/CFF2_Support.md](docs/CFF2_Support.md) for details
- **Workflow changes**: For direct invocation, you may now need to build a CFF table first using `tx`
  - `tx` has been enhanced with features previously exclusive to `makeotfexe`, including GlyphOrderAndAliasDB support

### Other Changes

#### Major C/C++ Port
- **C → C++ conversion**: Overall codebase is now 49% C++ vs 4% C++ in v4.0
  - Major files: tx_shared, uforead, ufowrite, t1read, t1cstr, t2cstr, ttread, and many more
  - Total source files: 177 → 150 (-15%)
  - Better type safety, modern C++ patterns, improved maintainability
  - See [docs/C_CPP_Changes.md](docs/C_CPP_Changes.md) for comprehensive architectural details

#### Build System Modernization
- **scikit-build-core**: Migrated from setuptools to scikit-build-core for better CMake integration
- **Version integration**: All tools use AFDKO package version as tool version
- **Simplified dependencies**: Streamlined build requirements (scikit-build-core, setuptools-scm, cython)

#### Bug fixes

Many issues have been fixed in this update. Because of the large amount of change we are not listing those issues individually. Check the AFDKO issue records for details.

### Important Notes

- **Potential regressions**: Due to the extensive changes, some edge cases may not work as expected initially. Please report any issues.
- **Documentation updated**: All documentation has been updated to use the new `afdko <command>` syntax
- **Backward compatibility**: While deprecated, individual command wrappers continue to work in this release

### Migration Guide

**For most users**: Simply install the new version and start using the unified interface.

**If calling commands directly**:
1. Update scripts to use `afdko <command>` syntax (recommended)
2. Or set environment variable `AFDKO_WRAPPER_MODE` to `off` to silence deprecation warnings (temporary)

**If calling makeotfexe directly**:
1. Replace with `afdko addfeatures`
2. In place of type1 input, first generate CFF using `afdko tx`
