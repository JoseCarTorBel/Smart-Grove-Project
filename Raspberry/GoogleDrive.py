<<<<<<< HEAD
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


def getAllSheet(hoja):
	return hoja.get_all_records()

def getValue(hoja,fila,columna):
	return hoja.cell(fila, columna).value

def setValue(hoja,fila,columna,valor):
	hoja.update_cell(fila, columna, valor)
	
def setRow(hoja,fila,numFila):
	hoja.insert_row(fila, numFila)
	
def getFirstRowEmpty(hoja):
	i=1;
	while(True):
		if(getValue(hoja,i,1)==""):
			return i;
		i+=1
def insert_row(hoja,fila):
	setRow(hoja,fila,getFirstRowEmpty(hoja))
	

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open("ProyectoHuertos").sheet1
setValue(sheet,10,1,"Hola")

=======
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


def getAllSheet(hoja):
	return hoja.get_all_records()

def getValue(hoja,fila,columna):
	return hoja.cell(fila, columna).value

def setValue(hoja,fila,columna,valor):
	hoja.update_cell(fila, columna, valor)
	
def setRow(hoja,fila,numFila):
	hoja.insert_row(fila, numFila)
	
def getFirstRowEmpty(hoja):
	i=1;
	while(True):
		if(getValue(hoja,i,1)==""):
			return i;
		i+=1
def insert_row(hoja,fila):
	setRow(hoja,fila,getFirstRowEmpty(hoja))
	

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open("ProyectoHuertos").sheet1


>>>>>>> 9231b11556a6e2b58fd13a0d6bb47327fe104324
