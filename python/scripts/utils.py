import os
from datetime import datetime
import mysql.connector
from sqlalchemy import create_engine   
from unicodedata import normalize

import pandas as pd

class Sanitation:
    
    def __init__(self, data, configs):
        self.data = data
        self.metadata =  pd.read_excel(configs["meta_path"])
        self.len_cols = max(list(self.metadata["id"]))
        self.columns = list(self.metadata['nome_original'])
        self.new_columns = list(self.metadata['nome'])
        self.path_work = configs["work_path"]        

    def select_rename(self):
        self.data = self.data.loc[:, self.columns]
        for i in range(self.len_cols):
            self.data.rename(columns={self.columns[i]:self.new_columns[i]}, inplace = True)

    def typing(self):
        for col in self.new_columns:
            tipo = self.metadata.loc[self.metadata['nome'] == col]['tipo'].item()
            if tipo == "int":
                self.data[col] = self.data[col].astype(int)
            elif tipo == "float":
                self.data[col].replace(",", ".", regex=True, inplace=True)
                self.data[col] = self.data[col].astype(float)
            elif tipo == "date":
                self.data[col] = pd.to_datetime(self.data[col]).dt.strftime('%Y-%m-%d')

        self.remove_special_chars()
        self.to_lowecase()
    
    def save_work(self):
        self.data['load_date'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        con = mysql.connector.connect(
            user='root', password='root', host='mysql', port="3306", database='db')
        
        print("DB connected")

        engine  = create_engine("mysql+mysqlconnector://root:root@mysql/db")
        self.data.to_sql('cadastro', con=engine, if_exists='append', index=False)
        con.close()

    def remove_special_chars(self):
        func = lambda x: normalize('NFKD', x).encode('ASCII', 'ignore').decode('ASCII')
        self.data['email'] = (self.data['email'].apply(func))

    def to_lowecase(self):
        self.data['nome'] = self.data['nome'].str.lower()
        self.data['sobrenome'] = self.data['sobrenome'].str.lower()

def error_handler(exception_error, stage):
    
    log = [stage, type(exception_error).__name__, exception_error,datetime.now()]
    logdf = pd.DataFrame(log).T
    
    if not os.path.exists("logs_file.txt"):
        logdf.columns = ['stage', 'type', 'error', 'datetime']
        logdf.to_csv("logs_file.txt", index=False,sep = ";")
    else:
        logdf.to_csv("logs_file.txt", index=False, mode='a', header=False, sep = ";")
