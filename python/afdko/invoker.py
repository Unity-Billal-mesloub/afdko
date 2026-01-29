"""
AFDKO Unified Command Invoker (Python Module)

This module provides the command registry, help system, and dispatch logic
for the unified 'afdko' command.

It is used by:
1. The C++ binary (for non-C++ commands, help, errors)
2. The Python wrapper mode (when AFDKO_BUILD_BINARY=OFF)

This keeps all command logic and help text in one maintainable location.
"""

import sys
from typing import NoReturn


# Complete command registry with abbreviations
# Format: name -> (module:function, description)

CPP_COMMANDS = {
    # C++ commands (handled by binary's fast path, or _internal in wrapper mode)
    'tx': ('afdko._internal:tx', 'Font converter and analyzer'),
    'sfntedit': ('afdko._internal:sfntedit', 'SFNT table editor'),
    'se': ('afdko._internal:sfntedit', None),  # abbreviation
    'spot': ('afdko._internal:spot', 'SFNT font inspector'),
    'addfeatures': ('afdko._internal:addfeatures', 'Feature file compiler'),
    'af': ('afdko._internal:addfeatures', None),  # abbreviation
    'detype1': ('afdko._internal:detype1', 'Type 1 font decompiler'),
    'dt1': ('afdko._internal:detype1', None),  # abbreviation
    'type1': ('afdko._internal:type1', 'Type 1 font tool'),
    't1': ('afdko._internal:type1', None),  # abbreviation
    'sfntdiff': ('afdko._internal:sfntdiff', 'Compare SFNT fonts'),
    'mergefonts': ('afdko._internal:mergefonts', 'Merge font files'),
    'mf': ('afdko._internal:mergefonts', None),  # abbreviation
    'rotatefont': ('afdko._internal:rotatefont', 'Rotate font glyphs'),
    'rf': ('afdko._internal:rotatefont', None),  # abbreviation
}

PYTHON_COMMANDS = {
    # Python commands
    'makeotf': ('afdko.makeotf:main', 'Build OpenType font'),
    'mo': ('afdko.makeotf:main', None),  # abbreviation
    'buildcff2vf': ('afdko.buildcff2vf:main', 'Build CFF2 variable font'),
    'bvf': ('afdko.buildcff2vf:main', None),  # abbreviation
    'buildmasterotfs': ('afdko.buildmasterotfs:main', 'Build master OTF fonts'),
    'bmo': ('afdko.buildmasterotfs:main', None),  # abbreviation
    'makeinstancesufo': ('afdko.makeinstancesufo:main', 'Generate UFO instances'),
    'miu': ('afdko.makeinstancesufo:main', None),  # abbreviation
    'checkoutlinesufo': ('afdko.checkoutlinesufo:main', 'Check UFO outlines'),
    'cou': ('afdko.checkoutlinesufo:main', None),  # abbreviation
    'comparefamily': ('afdko.comparefamily:main', 'Compare font family'),
    'cf': ('afdko.comparefamily:main', None),  # abbreviation
    'otc2otf': ('afdko.otc2otf:main', 'Extract OTFs from OTC'),
    'otf2otc': ('afdko.otf2otc:main', 'Combine OTFs into OTC'),
    'otf2ttf': ('afdko.otf2ttf:main', 'Convert OTF to TTF'),
    'ttfcomponentizer': ('afdko.ttfcomponentizer:main', 'Add TTF components'),
    'ttfdecomponentizer': ('afdko.ttfdecomponentizer:main', 'Remove TTF components'),
    'ttxn': ('afdko.ttxn:main', 'TTX wrapper'),
    'otfautohint': ('afdko.otfautohint.__main__:main', 'Auto-hint fonts'),
    'autohint': ('afdko.otfautohint.__main__:main', None),  # abbreviation
    'ah': ('afdko.otfautohint.__main__:main', None),  # abbreviation
    'otfstemhist': ('afdko.otfautohint.__main__:stemhist', 'Generate stem histogram'),
    'stemhist': ('afdko.otfautohint.__main__:stemhist', None),  # abbreviation
    'sh': ('afdko.otfautohint.__main__:stemhist', None),  # abbreviation
    # Proofing tools
    'charplot': ('afdko.proofpdf:charplot', 'Generate character proof'),
    'digiplot': ('afdko.proofpdf:digiplot', 'Generate digitization proof'),
    'fontplot': ('afdko.proofpdf:fontplot', 'Generate font proof'),
    'fontplot2': ('afdko.proofpdf:fontplot2', 'Generate font proof (v2)'),
    'fontsetplot': ('afdko.proofpdf:fontsetplot', 'Generate font set proof'),
    'hintplot': ('afdko.proofpdf:hintplot', 'Generate hint proof'),
    'waterfallplot': ('afdko.proofpdf:waterfallplot', 'Generate waterfall proof'),
}

ALL_COMMANDS = {**CPP_COMMANDS, **PYTHON_COMMANDS}


def print_help() -> None:
    """Print help message with all commands."""
    print("Usage: afdko <command> [options]")
    print()
    print("AFDKO Unified Command Interface")
    print()

    # C++ Commands
    print("C++ Commands (fast, no Python startup):")
    seen = set()
    for name, (target, desc) in CPP_COMMANDS.items():
        if desc is not None:  # Skip abbreviations
            # Find abbreviations for this command
            abbrevs = [k for k, (t, d) in CPP_COMMANDS.items() if t == target and d is None]
            if abbrevs:
                abbrev_str = f" ({', '.join(abbrevs)})"
            else:
                abbrev_str = ""
            print(f"  {name:20} {desc}{abbrev_str}")
            seen.add(target)

    print()
    print("Python Commands:")
    seen = set()
    for name, (target, desc) in PYTHON_COMMANDS.items():
        if desc is not None and target not in seen:  # Skip abbreviations and duplicates
            # Find abbreviations for this command
            abbrevs = [k for k, (t, d) in PYTHON_COMMANDS.items() if t == target and d is None]
            if abbrevs:
                abbrev_str = f" ({', '.join(abbrevs)})"
            else:
                abbrev_str = ""
            print(f"  {name:20} {desc}{abbrev_str}")
            seen.add(target)

    print()
    print("Run 'afdko <command> -h' for command-specific help.")


def dispatch_command(cmd: str) -> NoReturn:
    """Dispatch to the appropriate command implementation."""
    if cmd not in ALL_COMMANDS:
        print(f"Error: Unknown command '{cmd}'", file=sys.stderr)
        print("Run 'afdko --help' for usage.", file=sys.stderr)
        sys.exit(1)

    target, _ = ALL_COMMANDS[cmd]
    module_name, func_name = target.split(':')

    # Import and call the function
    try:
        module = __import__(module_name, fromlist=[func_name])
        func = getattr(module, func_name)
    except (ImportError, AttributeError) as e:
        print(f"Error loading command '{cmd}': {e}", file=sys.stderr)
        sys.exit(1)

    # Adjust sys.argv to look like the command was called directly
    # "afdko makeotf -f font.pfa" becomes "makeotf -f font.pfa"
    sys.argv = sys.argv[1:]

    # Call the function - it will handle sys.exit() internally
    result = func()

    # Handle return value (some commands return exit code)
    if result is None:
        sys.exit(0)
    elif isinstance(result, int):
        sys.exit(result)
    else:
        sys.exit(0)


def main() -> NoReturn:
    """Main entry point for the unified afdko command."""
    # No subcommand provided
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    subcmd = sys.argv[1]

    # Help requested
    if subcmd in ('-h', '--help', 'help'):
        print_help()
        sys.exit(0)

    # Dispatch to command
    dispatch_command(subcmd)


if __name__ == '__main__':
    main()
