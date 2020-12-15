
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


	def getAllSheet(self):
		return self.sheet.get_all_records()

	def getValue(self,fila,columna):
		return self.sheet.cell(fila, columna).value

	def setValue(self,fila,columna,valor):
		self.sheet.update_cell(fila, columna, valor)
	
	def setRow(self,fila,numFila):
		self.sheet.insert_row(fila, numFila)
	
	def getFirstRowEmpty(self):
		i=1;
		while(True):
			if(self.getValue(i,1)==""):
				return i;
			i+=1
	def insertRow(self,fila):
		self.setRow(fila,self.getFirstRowEmpty())
	

#scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
#creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
#client = gspread.authorize(creds)

#sheet = client.open("ProyectoHuertos").sheet1


