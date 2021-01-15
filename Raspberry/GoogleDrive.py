
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

class GoogleDrive:

	scope=""
	creds=""
	client=""
	sheet=""

	def __init__(self):
		self.scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
		self.creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', self.scope)
		self.client = gspread.authorize(self.creds)
		self.sheet = self.client.open("ProyectoHuertos").sheet1

	# Devuelve toda la hoja de calculo
	def getAllSheet(self): 
		return self.sheet.get_all_records()
	# Devuelve el valor de una fila/columna
	def getValue(self,fila,columna):
		return self.sheet.cell(fila, columna).value
	# Setea el valor de una fila/columna
	def setValue(self,fila,columna,valor):
		self.sheet.update_cell(fila, columna, valor)
	# Inserta una fila 
	def setRow(self,fila,numFila):
		self.sheet.insert_row(fila, numFila)
	# Nos devuelve el numero de la primera fila vacia
	def getFirstRowEmpty(self):
		i=1;
		while(True):
			if(self.getValue(i,1)==""):
				return i;
			i+=1
	# Inserta una fila al final
	def insertRow(self,fila):
		self.setRow(fila,self.getFirstRowEmpty())
	# Inserta varias filas
	def insertRows(self,matriz):
		inicio=self.getFirstRowEmpty()
		fin=inicio+len(matriz)
		up="A"+str(inicio)+":C"+str(fin)
		self.sheet.update(up, matriz)
	

#scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
#creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
#client = gspread.authorize(creds)

#sheet = client.open("ProyectoHuertos").sheet1


