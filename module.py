#!/usr/bin/env python2.7

import sqlite3 as lite
import json
from time import time
from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import UNIXServerEndpoint as ServerEndpoint

class Module(Protocol):
	def __init__(self, db_conn):
		print 'nothing'
		#nothing for now but we should create the attributes ...
		
	def dataReceived(self, data):
		try:
			json_data = json.loads(data)
		except ValueError:
			self.err_decode_data()
			return

		if not 'code' in json_data: 
			self.err_code_not_found()
			return

		
		code = str(json_data['code'])
		if code == 'get_cur':
			self.get_cur(json_data)
		elif code == 'get_at':
			self.get_at(json_data)
		elif code == 'get_from_to':
			self.get_from_to(json_data)
		elif code == 'answer':
			self.load_answer(json_data
		else:
			self.err_code_not_found()
			
	def error(self, msg):
# TODO log errors
		print msg
		re = {'success': False}
		self.transport.write(json.dumps(re))
		
	def err_decode_data(self):
		self.error('Impossible to decode the received data')

	def err_code_not_found(self):
		self.error('Code not found in the query')

	def get_cur(self, data):
		entry_objs = data['objs']
		for attr in list_attr:
			if attr.name in entry_objs:
				self.update_attrs()
				out = {}
				out['code'] = "answer"
				out['asking_attr'] = data['asking_attr']
				out['obj']=attr
				out_json = json.dumps(out)
				self.transport.write(out_json)

	def get_at(self, data):
		#just send it to the db
		self.transport.write(db_data)
		
	def get_from_to(self, data):
		#just send it to the db
		self.transport.write(db_data)

	def update_attrs(self):
		for attr in list_attr:
			if len(attr.list_depend) > 0:
			
				# avant d'envoyer la demeande je vasi faire une liste qui va check si j'ai reçu mes info pr l'appel bloquant
				#rmq il faut que ce tableau soit la list depend ....
				#on la clear à chaque fois que on s'en ert comme sa elle peut servir de global pr traveerser les fonctions
				#a refaire sous al forme d'un tin de dico
				
				
				#envoie de la demande
				out = {}
				out['code'] = "get_cur"
				out['asking_attr']=attr.name
				out['objs'] = attr.list_depend
				out_json = json.dumps(out)
				self.transport.write(out_json)
				
				test=true;
				while test != true:
					
					#I want to wait here but how
					#maybe creating an event (is there away in python ??)
					
					#verif si on a recup toute les valeurs
					test = true
					for cle, value in attr.list_depend:
						if value = 0:
							test = false
							break
							
				#here we need to update the attribute
				#but idk how f_eval works ...
				
				#and now we clear list_depend so we signal that we need to ask for data next time
				for cle in attr.list_depend:
					attr.list_depend[cle] = 0 
	
	def load_answer(self,data):
		for elem in list_attr:
			if elem.name = data['asking_attr']:
				obj=data['obj']
				elem.list_depend[obj.name]=obj
				
		#here we need to launch an event to signal we have gotted some infos
		#to ask the funstions to continu and check if they have all the info they need
		
						
if __name__ == '__main__':
	factory = Factory()
	factory.protocol = Module
	port = reactor.listenUNIX('module.sock', factory)
	reactor.run()
