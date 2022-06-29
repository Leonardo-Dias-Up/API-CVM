import pandas as pd
import sqlalchemy
import requests
import numpy as np
import sqlite3
import io
import requests, zipfile, io
import os
import csv, sys

###### EXTRAINDO OS ARQUIVOS NO ZIP CARTEIRA CVM #########
def carteiraCVM(ano, mes):
  
    #Extraindo arquivo e criando uma pasta com nome e mês
    url = 'http://dados.cvm.gov.br/dados/FI/DOC/CDA/DADOS/cda_fi_{:02d}{:02d}.zip'.format(ano,mes)
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    files_dir = (r"F:\00. CarteiraCVM\{:02d}{:02d}".format(ano,mes))
    x = z.extractall(files_dir)
    
    count = -1
    listcsv = ['1.tp','2.fic','3.swap','4.assets/debêtures',
                 '5.letras','6.créd.priv','7.inv.ext','8.outros'
                 '9.plfundos']
    listcsv[0]
  
    #listando os arquivos .csv e carregando eles
    arquivos = [f for f in os.listdir(files_dir) if f.endswith(".csv")]
    for filename in arquivos:
      if filename.endswith(".csv"):
          print(filename)
          

          #Carregar os arquivos em nosso db MYSQL
          with open(os.path.join(files_dir,filename), 'rb') as file:
              count = count + 1
              
              #chamando os arquivos extraidos
              reader = pd.read_csv(file, error_bad_lines=False, sep= "," , encoding='ISO-8859-1')
              reader
              
              try:
                  a = listcsv[count]
                  #criando o db
                  conn = sqlite3.connect(r'F:\00. CarteiraCVM\%s.db'%a)
                  c = conn.cursor()
                                   
                  #Convertendo para sql - sqlite3
                  reader.to_sql(a, conn, if_exists='replace', index = False)
        
                  #Enviando o comando
                  conn.commit()
                  print('Dados alterados com sucesso.')
                    
              except sqlite3.OperationalError:
                  pass
                  #Fechando conexão
              finally:
                  conn.close()
                  
carteiraCVM(2021, 10)# -*- coding: utf-8 -*-

