#teste de macro para inserir simbologia


import importSVG, os
import FreeCAD, FreeCADGui, Part, math, os
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
		self.form.rb_biblioteca3d.clicked.connect(self.get_arquivos)

		self.vista = FreeCADGui.ActiveDocument.ActiveView
		self.callback = self.vista.addEventCallbackPivy(SoMouseButtonEvent.getClassTypeId(), self.getpoint)

		self.get_arquivos()
		

	def get_arquivos(self): #insere a lista de arquivo no listbox
		self.form.lista.clear() # limpa a lista
		self.listaarquiivos = []
		if self.form.rb_simbologia.isChecked() == True:
			for (dirpath, dirnames, filenames) in os.walk(path_arq+'/biblioteca/symbology'):
				listaarquiivos = filenames

			for item in listaarquiivos:
				self.form.lista.insertItem(-1,item)

		elif self.form.rb_biblioteca2d.isChecked() == True:
			for (dirpath, dirnames, filenames) in os.walk(path_arq+'/biblioteca/library2d'):
				listaarquiivos = filenames

			for item in listaarquiivos:
				self.form.lista.insertItem(-1,item)



		elif self.form.rb_biblioteca3d.isChecked() == True:
			for (dirpath, dirnames, filenames) in os.walk(path_arq+'/biblioteca/library3d'):
				listaarquiivos = filenames

			for item in listaarquiivos:
				self.form.lista.insertItem(-1,item)


	def accept(self):
		if self.form.rb_simbologia.isChecked() == True:
			self.get_simbologia()

		if self.form.rb_biblioteca2d.isChecked() == True:
			self.get_biblioteca2d()
		

		FreeCAD.ActiveDocument.recompute()

	def reject(self):
		self.vista.removeEventCallbackPivy(SoMouseButtonEvent.getClassTypeId(), self.callback) #finaliza o evento do mouse


	def getpoint(self,event_cb):
		event = event_cb.getEvent()
		if event.getState() == SoMouseButtonEvent.DOWN and self.form.rb_simbologia.isChecked() == True :
			pos = event.getPosition() # pega o ponto clocado
			point = self.vista.getPoint(pos[0], pos[1])

			obj = self.get_simbologia()
			obj.Placement.Base = point
			

		elif event.getState() == SoMouseButtonEvent.DOWN and self.form.rb_biblioteca2d.isChecked() == True :
			pos = event.getPosition() # pega o ponto clocado
			point = self.vista.getPoint(pos[0], pos[1])

			obj = self.get_biblioteca2d()
			obj.Placement.Base = point
		

		FreeCAD.ActiveDocument.recompute()
		

	def get_simbologia(self):

		lista = importSVG.insert(path_arq+'/biblioteca/symbology/'+str(self.form.lista.currentText()),FreeCAD.ActiveDocument.Name)

		lista = []
		for i in FreeCAD.ActiveDocument.Objects:
			if 'path' in i.Label :

				lista.append(i)

		obj = App.activeDocument().addObject("Part::Compound","Compound") 
		obj.Links = lista

		return obj


	def get_biblioteca2d(self):
		lista = importSVG.insert(path_arq+'/biblioteca/library2d/'+str(self.form.lista.currentText()),FreeCAD.ActiveDocument.Name)

		lista = []
		for i in FreeCAD.ActiveDocument.Objects:
			if 'path' in i.Label :

				lista.append(i)

		obj = App.activeDocument().addObject("Part::Compound","Compound") 
		obj.Links = lista

		return obj



painel = BibliotecaPainel()
FreeCADGui.Control.showDialog(painel) 