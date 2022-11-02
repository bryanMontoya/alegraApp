from openpyxl import load_workbook
 
#load excel file
workbook = load_workbook(filename = "Libro1 - copia.xlsx")
 
#open workbook
sheet = workbook.active
 
#modify the desired cell
sheet["X3"] = "Cargado"
 
#save the file
workbook.save(filename="Libro2 - copia.xlsx")