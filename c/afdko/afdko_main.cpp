/*
 * AFDKO Unified Command Invoker
 *
 * This is a git-style unified command dispatcher that routes subcommands
 * to their appropriate implementations (C++ or Python).
 *
 * Usage: afdko <command> [options]
 *
 * Phase 1: Minimal implementation with just tx command for proof of concept
 */

#include <cstdio>
#include <cstring>

// FDK_VERSION is referenced by tx_shared.cpp and other tools
// In the _internal extension, this is defined by Cython and initialized from Python
// For the standalone binary, we define it here and will set it properly later
extern "C" char *FDK_VERSION = (char *)"unknown";

// External C++ tool entry points
extern "C" {
    int main__tx(int argc, char* argv[]);
    int main__sfntedit(int argc, char* argv[]);
}

// Command structure
struct Command {
    const char* name;
    const char* abbrev;  // Can be nullptr
    int (*cpp_main)(int, char**);
};

// Command registry - Phase 1: Just tx and sfntedit for proof of concept
static const Command commands[] = {
    {"tx", nullptr, main__tx},
    {"sfntedit", "se", main__sfntedit},
    {nullptr, nullptr, nullptr}  // Sentinel
};

const Command* find_command(const char* name) {
    for (int i = 0; commands[i].name != nullptr; i++) {
        if (strcmp(commands[i].name, name) == 0) {
            return &commands[i];
        }
        if (commands[i].abbrev && strcmp(commands[i].abbrev, name) == 0) {
            return &commands[i];
        }
    }
    return nullptr;
}

void print_help() {
    printf("Usage: afdko <command> [options]\n\n");
    printf("AFDKO Unified Command Interface\n\n");
    printf("Available Commands (Phase 1 - Proof of Concept):\n");

    for (int i = 0; commands[i].name != nullptr; i++) {
        if (commands[i].abbrev) {
            printf("  %-20s (abbrev: %s)\n", commands[i].name, commands[i].abbrev);
        } else {
            printf("  %s\n", commands[i].name);
        }
    }

    printf("\nRun 'afdko <command> -h' for command-specific help.\n");
    printf("\nNote: This is Phase 1 - more commands will be added in subsequent phases.\n");
}

int main(int argc, char* argv[]) {
    // No subcommand provided
    if (argc < 2) {
        print_help();
        return 1;
    }

    const char* subcmd = argv[1];

    // Help requested
    if (strcmp(subcmd, "-h") == 0 ||
        strcmp(subcmd, "--help") == 0 ||
        strcmp(subcmd, "help") == 0) {
        print_help();
        return 0;
    }

    // Find the command
    const Command* cmd = find_command(subcmd);
    if (!cmd) {
        fprintf(stderr, "Error: Unknown command '%s'\n", subcmd);
        fprintf(stderr, "Run 'afdko --help' for usage.\n");
        return 1;
    }

    // Shift arguments: "afdko tx -dump" becomes "tx -dump"
    // The subcommand's main expects argv[0] to be the command name
    argc--;
    argv++;

    // Dispatch to the C++ command
    return cmd->cpp_main(argc, argv);
}
