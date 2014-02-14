#!/usr/bin/env python2
"""
Test a module with this script

Usage:
    test_module <module_name>
"""
import os
import sys
import docopt

sys.path.append('core')
from module import use_module

if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    module_name = args['<module_name>']
    mod = use_module(module_name)
    print 'Informations :', mod.info
    fields = mod.info['fields']
    for field in fields:
        print 'Test du champ :', field['name']
        field_fn = getattr(mod, field['name'])
        syntax = str
        if 'type' in field:
            if field['type'] == 'numeric':
                syntax = float
            elif field['type'] == 'boolean':
                syntax = bool
            elif fiald['type'] == 'string':
                syntax = str
            else:
                print '**** WARNING **** Pas de type connu pour ce champ. (Il faut faire heriter de fields.syntax.xxx)'
        else:
            print '**** WARNING **** Pas de type pour ce champ. (Il faut faire heriter de fields.syntax.xxx)'

        if 'readable' in field and field['readable']:
            v = field_fn()
            print 'Test en lecture :', v
            if v is None:
                print '**** WARNING **** Pas de valeur pour ce champ. (Il faut heriter de fields.persistant.Volatile)'
        elif 'writable' in field and field['writable']:
            if syntax is float:
                value = 42.0
            elif syntax is bool:
                value = True
            elif syntax is str:
                value = 'Hello'

            field_fn(value)
            if 'readable' in field and field['readable']:
                v = field_fn()
                if v is None:
                    print '**** ERROR **** Pas de valeur pour ce champ apres ecriture.'
                if v != value:
                    print '**** ERROR **** Pas la meme valeur lu apres ecriture.'
            print 'Test en ecriture :'
        else:
            print '**** WARNING **** Champ ni readable ni writable'
        print

    if not fields:
        print '**** ERREUR **** Pas de champ dans le module'
