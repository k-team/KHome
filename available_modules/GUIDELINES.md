Guidelines
==========

Modules that are available should be put under this directory as zip files.

## Directory structure for module zip

    some_module.zip    an available module
    |
    +--some_module/    the module's sub-directory
       |
       +--module.json  specific module description/configuration (how to start
       |               it, filename overrides, etc...)
       +--public/      the module's public directory, all files here can be
                       directly accessed by the web client (provided that the
                       extension corresponds to a file that can be served)

## Module configuration options

These entries are read in the module's __module.json__.

    start: how to start the module (shell command)
    public_directory: the public directory's name
    partial_name: specific view's filename, relative to public directory
    icon_name: specific icon's filename, relative to public directory
    has_view: specify if the module has a specific view or not (deprecated)
