import json

def creerjson(cmd, time_start, time_end, list_args):
    json_dico =  {}
    if cmd == 'get_at':
        json_dico['cmd_type'] = 'get_at'
        json_dico['time_start'] = time_start
    elif cmd == 'get_cur':
        json_dico['cmd_type'] = 'get_cur'
    elif cmd == 'get_from_to':
        json_dico['cmd_type'] = 'get_from_to'
        json_dico['time_start'] = time_start
        json_dico['time_end'] = time_end
    json_dico['objs'] = list_args
    
    retour = json.dumps(json_dico)
    print(json_dico)
    return retour

list_args = []
list_args.append('argument1')
list_args.append('argument2')
creerjson('get_from_to',0,10, list_args)
