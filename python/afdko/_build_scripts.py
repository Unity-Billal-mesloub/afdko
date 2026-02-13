"""
Dynamic script generation for AFDKO build system.

This module provides dynamic metadata for the [project.scripts] section,
conditionally including the 'afdko' command based on whether the C++ binary
or Python wrapper should be used.

Environment Variables:
    AFDKO_COMMAND_USE_WRAPPER: When set to 'ON', installs Python wrapper for
                                the afdko command instead of the C++ binary.
                                Default: 'OFF' (use C++ binary)
"""

import os


def dynamic_metadata(field, settings, metadata):
    """
    Generate dynamic script metadata based on build configuration.

    Args:
        field: The metadata field being requested (should be "scripts")
        settings: Configuration settings from pyproject.toml
        metadata: Project metadata dictionary

    Returns:
        Dictionary mapping script names to entry points
    """
    assert field == "scripts", f"Expected 'scripts' field, got '{field}'"

    # All deprecated wrapper scripts - always included
    scripts = {
        # C++ commands
        "addfeatures": "afdko._deprecated:addfeatures_wrapper",
        "detype1": "afdko._deprecated:detype1_wrapper",
        "mergefonts": "afdko._deprecated:mergefonts_wrapper",
        "rotatefont": "afdko._deprecated:rotatefont_wrapper",
        "sfntdiff": "afdko._deprecated:sfntdiff_wrapper",
        "sfntedit": "afdko._deprecated:sfntedit_wrapper",
        "spot": "afdko._deprecated:spot_wrapper",
        "tx": "afdko._deprecated:tx_wrapper",
        "type1": "afdko._deprecated:type1_wrapper",
        # Python commands - build & processing
        "buildcff2vf": "afdko._deprecated:buildcff2vf_wrapper",
        "buildmasterotfs": "afdko._deprecated:buildmasterotfs_wrapper",
        "checkoutlinesufo": "afdko._deprecated:checkoutlinesufo_wrapper",
        "comparefamily": "afdko._deprecated:comparefamily_wrapper",
        "makeinstancesufo": "afdko._deprecated:makeinstancesufo_wrapper",
        "makeotf": "afdko._deprecated:makeotf_wrapper",
        "makeotfexe": "afdko._deprecated:makeotfexe_wrapper",
        "otc2otf": "afdko._deprecated:otc2otf_wrapper",
        "otf2otc": "afdko._deprecated:otf2otc_wrapper",
        "otf2ttf": "afdko._deprecated:otf2ttf_wrapper",
        "ttfcomponentizer": "afdko._deprecated:ttfcomponentizer_wrapper",
        "ttfdecomponentizer": "afdko._deprecated:ttfdecomponentizer_wrapper",
        "ttxn": "afdko._deprecated:ttxn_wrapper",
        # Python commands - proofing
        "charplot": "afdko._deprecated:charplot_wrapper",
        "digiplot": "afdko._deprecated:digiplot_wrapper",
        "fontplot": "afdko._deprecated:fontplot_wrapper",
        "fontplot2": "afdko._deprecated:fontplot2_wrapper",
        "fontsetplot": "afdko._deprecated:fontsetplot_wrapper",
        "hintplot": "afdko._deprecated:hintplot_wrapper",
        "waterfallplot": "afdko._deprecated:waterfallplot_wrapper",
        # Python commands - hinting
        "otfautohint": "afdko._deprecated:otfautohint_wrapper",
        "otfstemhist": "afdko._deprecated:otfstemhist_wrapper",
    }

    # Conditionally include afdko command
    use_wrapper = os.environ.get("AFDKO_COMMAND_USE_WRAPPER", "OFF")
    if use_wrapper == "ON":
        # Install Python wrapper for afdko command
        scripts["afdko"] = "afdko.invoker:main"
        # Note: If use_wrapper == "OFF", the C++ binary is installed
        # by CMake

    return scripts
