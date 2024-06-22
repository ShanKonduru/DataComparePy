import pandas as pd
 
class ExcelFile:
    def __init__(self, file_path, sheet_name=0):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.data = pd.read_excel(file_path, sheet_name=sheet_name)
