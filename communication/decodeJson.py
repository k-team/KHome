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
    """print(json_dico)"""
    return retour
  

def creerjsonRetour(cmd):
    json_dico =  {}
    list_args = []
    list_obj1={}
    list_obj2 = {}
    list_obj_data1 = []
    list_obj_data2 = []
    list_obj1['type'] = 'type1'
    list_obj1['name'] = 'arg1'
    list_obj_data1 += [{'time':1, 'value':1},
                       {'time':2, 'value':2},
                       {'time':3, 'value':3},
                       {'time':4, 'value':4},
                       {'time':5, 'value':5}]
    
    list_obj2['type'] = 'type2'
    list_obj2['name'] = 'arg2'
    list_obj_data2 += [{'time':10, 'value':11},
                       {'time':12, 'value':12},
                       {'time':13, 'value':13},
                       {'time':14, 'value':14},
                       {'time':15, 'value':15}]

    
    list_obj1['obj_data'] = list_obj_data1

    list_obj2['obj_data'] = list_obj_data2

    list_args.append(list_obj1)
    list_args.append(list_obj2)

    json_dico['objs'] = list_args
    retour = json.dumps(json_dico,  indent=2)
    print(retour)
    return retour

def decodejson(askedJson):
    decode = json.loads(askedJson)
    obj_data = []
    print(decode)
    if len(decode)!=0: 
        print('Decoder')
        for objdata in decode['objs']:
            list_obj_data =[]
            list_obj_data.append(str(objdata['name']))
            list_obj_data.append(str(objdata['type']))
            list_data =[]
            for data in objdata['obj_data']:
                list_data.append('('+str(data['time'])+','+str(data['value'])+')')
            list_obj_data.append(list_data)
            obj_data.append(list_obj_data)
            '''print(objdata)'''
        '''print(obj_data)'''
    else:
        print('Error')
    return obj_data
  

list_args = []
list_args.append('argument1')
list_args.append('argument2')
jsonTest = creerjson('get_from_to',0,10, list_args)
jsonTest2 = creerjsonRetour('get_from_to')
retour = json.dumps([],  indent=2)
test = decodejson(jsonTest2)
print(test)

