#teste de macro para inserir simbologia


import importSVG, os, random
import FreeCAD, FreeCADGui,Draft , Part, math, os
from pivy.coin import *


path_arq = str(os.path.dirname(__file__))
path_ui = str(os.path.dirname(__file__))+'/bibliotecagui.ui'




class BibliotecaPainel:
	def __init__(self):
		# Carrega a GUI
		self.form = FreeCADGui.PySideUic.loadUi(path_ui)

		self.listaarquiivos = []

		self.form.rb_simbologia.clicked.connect(self.get_arquivos)
		self.form.rb_biblioteca2d.clicked.connect(self.get_arquivos)
		#self.form.rb_biblioteca3d.clicked.connect(self.get_arquivos)

		self.form.bt_insert.clicked.connect(self.insert)

		self.vista = FreeCADGui.ActiveDocument.ActiveView
		

		self.get_arquivos()

	def accept(self):
		if self.form.rb_simbologia.isChecked() == True:
			self.get_simbologia()

		if self.form.rb_biblioteca2d.isChecked() == True:
			self.get_biblioteca2d()

	def insert(self):
		self.callback = self.vista.addEventCallbackPivy(SoMouseButtonEvent.getClassTypeId(), self.getpoint)
		

	def get_arquivos(self): #insere a lista de arquivo no listbox
		self.form.lista.clear() # limpa a lista
		self.listaarquiivos = []
		if self.form.rb_simbologia.isChecked() == True:
			for (dirpath, dirnames, filenames) in os.walk(path_arq+'/library/symbology'):
				listaarquiivos = filenames

			for item in listaarquiivos:
				self.form.lista.insertItem(-1,item)

		elif self.form.rb_biblioteca2d.isChecked() == True:
			for (dirpath, dirnames, filenames) in os.walk(path_arq+'/library/library2d'):
				listaarquiivos = filenames

			for item in listaarquiivos:
				self.form.lista.insertItem(-1,item)
		
		FreeCAD.ActiveDocument.recompute()


	def getpoint(self,event_cb): #pega o ponto clicado e posiciona o objeto n posição clicada
		event = event_cb.getEvent()
		if event.getState() == SoMouseButtonEvent.DOWN and self.form.rb_simbologia.isChecked() == True :
			print('simbologia')
			pos = event.getPosition() # pega o ponto clicado
			point = self.vista.getPoint(pos[0], pos[1])

			lista = self.get_simbologia()
			Draft.move(lista, point, copy=False) # move os elementos para a posução clicada

			#Cria um grupo para a simbologia  e a move para a posição clicada
			grupo = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","Simb.")
			#add a lista no grupo
			for i in lista:
				i.adjustRelativeLinks(grupo)
				grupo.addObject(i)


			

		elif event.getState() == SoMouseButtonEvent.DOWN and self.form.rb_biblioteca2d.isChecked() == True :
			print('biblioteca 2d')
			pos = event.getPosition() # pega o ponto clocado
			point = self.vista.getPoint(pos[0], pos[1])

			lista = self.get_biblioteca2d()
			Draft.move(lista, point, copy=False) # move os elementos para a posução clicada

			#Cria um grupo para a simbologia  e a move para a posição clicada
			grupo = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","block2d")
			#add a lista no grupo
			for i in lista:
				i.adjustRelativeLinks(grupo)
				grupo.addObject(i)
		

		FreeCAD.ActiveDocument.recompute()
		self.vista.removeEventCallbackPivy(SoMouseButtonEvent.getClassTypeId(), self.callback) #finaliza o evento do mouse
		

	def get_simbologia(self): #pega a simbologia e retorna o objeto

		lista = importSVG.insert(path_arq+'/library/symbology/'+str(self.form.lista.currentText()),FreeCAD.ActiveDocument.Name)

		lista = []
		for i in FreeCAD.ActiveDocument.Objects:
			if 'path' in i.Label:
				i.Label = 'Fig'
				lista.append(i)

		return lista


	def get_biblioteca2d(self): #pega a o bloco 2d e retorna o objeto
		lista = importSVG.insert(path_arq+'/library/library2d/'+str(self.form.lista.currentText()),FreeCAD.ActiveDocument.Name)

		lista = []
		for i in FreeCAD.ActiveDocument.Objects:
			if 'path' in i.Label :
				i.Label = 'Fig'

				lista.append(i)

		return lista



painel = BibliotecaPainel()
FreeCADGui.Control.showDialog(painel) 