.. KHome documentation master file, created by
   sphinx-quickstart2 on Fri Feb 28 21:37:45 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to KHome's documentation!
=================================

::

                  n__n_
                 /  = =\
                /   ._Y_)
    ___________/      "\________________________KStore__
              (_/  (_,  \
                \      ( \_,--""""--.
          __..-,-`.___,-` )-.______.' 
        <'     `-,'   `-, )-'    >
         `----._/      ( /"`>.--"
                "--..___,--"

Contents:

.. toctree::
   :maxdepth: 2

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Module writing guidelines
=========================

Modules that are available should be put under the *available_modules* directory as zip files.

Directory structure for module zip::

    some_module.zip    an available module
    |
    +--some_module/    the module's sub-directory
       |
       +--module.json  specific module description/configuration (how to start
       |               it, filename overrides, etc...)
       +--public/      the module's public directory, all files here can be
                       directly accessed by the web client (provided that the
                       extension corresponds to a file that can be served)

Module configuration options
++++++++++++++++++++++++++++

These entries are read in the module's **module.json**::

    name                unique name (used as modules'uid)
    start               how to start the module (shell command)
    public_directory    the public directory's name (default: ./public)
    partial_name        specific view's filename, relative to public directory
    icon_name           specific icon's filename, relative to public directory (default: ./icon.png)
    has_view            specify if the module has a specific view or not (deprecated)

Launching modules
=================
There is two way to launch modules. The first is to do it manually with the
*manager* script file. Try ``./manager --help`` or see the manual below to know
how to use it.

Manual of the *manager* script file::

    Module Manager

    Start or stop a module.

    Usage:
      module start <module_name> [--daemon]
      module stop <module_name>
      module start-all
      module stop-all
      module status
      module (-h | --help)

    Options:
      -h --help     Show this screen.
      --daemon      Start the module as a new daemon.

    Output:
      When the manager is used with the *status* command, the list of the status of
      the modules is written into stdin. The format of output is : PREFIX
      MODULE_NAME where PREFIX is one of those described below and MODULE_NAME is
      the name of the directory of the module (it may be different of the public
      name and the id of the module).

      R - the module is running
      S - the module is stopped

      When the manager is used with the *start* command, the output of the module is shown. It is usefull during debugging phase.

      With other command, there is no output.

The other way is to launch both application and store web servers. The
application web server can be execute without the store web server but it will
be impossible to install new modules.

To launch both servers::

    python2 ./webclient/app.py > ./webclient/app.log &
    python2 ./webclient/store.py > ./webclient/store.log &

The public website is accessible at **127.0.0.1:8888**. Installing modules
start it automaticaly if all required dependancies are installed. Else, you can
click on the modules'icon in the page *Module*. It's start it (if not started)
and go on the module's view.
