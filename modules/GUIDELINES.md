Guidelines
==========

# Modules

These should be put under the [modules][] directory, and can be managed using
the [manage.py][] script available in that same directory.

[modules]: ../../blob/modular-system/modules
[manage.py]: ../../blob/modular-system/manage.py

### Directory structure

    modules/
    |
    +--manage.py       the module managing script
    |
    +--some_module/    an added module
       |
       +--module.json    the module's description, how to start or install
       |                 it, its dependencies, etc...
       |
       +--module.sock    UNIX socket created by the module, corresponding to
       |                 its own socket
       |
       +--module.pid     file containing the module's pid, created by the
                         managing script and used by it to terminate modules
                         and their dependencies
