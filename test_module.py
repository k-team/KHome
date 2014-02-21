#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Script simplifiant les test d'un module.

Usage:
    test_module <module_name>
    test_module (-a|--all)

Options:
    -a, --all   Tester tous les modules
    -h, --help  Afficher ce message d'aide
"""
import os
import sys
import docopt
import logging

this_dir = os.path.dirname(os.path.realpath(__file__))
core_dir = os.path.join(this_dir, 'core')
sys.path.insert(1, core_dir)
from module import use_module
from module.path import modules_directory

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fmt = '%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s'
formatter = logging.Formatter(fmt)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

def test_module(module_name):
    logger.info('Début du test du module "%s"', module_name)
    mod = use_module(module_name)
    logger.info('Informations (brutes) : %s', mod.info)
    fields = mod.info['fields']

    if 'public_name' in mod.info or not mod.info['public_name']:
        logger.warning('Pas de nom public pour le module (ajouter un public_name = "xxx" dans la description du module')

    if not fields:
        logger.error('Pas de champ défini dans le module')
    for field in fields:
        logger.info('Début du test du champ : "%s"', field['name'].encode('utf8'))
        if 'public_name' in field or not field['public_name']:
            logger.warning('Pas de nom public pour le field (ajouter un public_name = "xxx" dans la description du field')
        field_fn = getattr(mod, field['name'])
        syntax = str
        if 'type' in field:
            if field['type'] == 'numeric':
                syntax = float
            elif field['type'] == 'boolean':
                syntax = bool
            elif field['type'] == 'string':
                syntax = str
            else:
                logger.warning('Pas de type connu pour ce champ. (Il faut faire heriter de fields.syntax.xxx)')
        else:
            logger.warning('Pas de type pour ce champ. (Il faut faire heriter de "fields.syntax.<type>")')

        if 'readable' in field and field['readable']:
            value = field_fn()
            if isinstance(value, str):
                value = value.encode('utf8')
            logger.info('Test en lecture : "%s"', value)
            if value is None:
                logger.warning('Pas de valeur pour ce champ. (Il faut heriter de "fields.persistant.Volatile")')
        if 'writable' in field and field['writable']:
            if syntax is float:
                new_value = 42.0
            elif syntax is bool:
                new_value = True
            elif syntax is str:
                new_value = 'Hello world!'

            logger.info('Test en écriture : écriture de "%s"', new_value)
            field_fn(new_value)
            if 'readable' in field and field['readable']:
                value = field_fn()
                logger.info('Valeur lue après écriture : "%s"', value)
                if value is None:
                    logger.error('Pas de valeur pour ce champ après écriture')
                elif value[1] != new_value:
                    logger.error('Pas la même valeur lue après écriture')
        if not 'writable' in field and not 'readable' in field:
            logger.warning('Champ ni "readable" ni "writable"')
        logger.info('Fin du test du champ : "%s"', field['name'])
    logger.info('Fin du test du module "%s"', module_name)

if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    if args['--all']:
        for module_name in os.listdir(modules_directory()):
            test_module(module_name)
    else:
        test_module(args['<module_name>'])
