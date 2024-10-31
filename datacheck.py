#%%
from sqlalchemy import create_engine,MetaData,Table,Column,Integer,String,DateTime,JSON,ForeignKey
import pandas as pd
engine=create_engine('sqlite:///data.db')

metadata=MetaData()

paciente=Table('paciente',metadata,
    Column('id',Integer,primary_key=True,autoincrement=True),
    Column('firstname',String),
    Column('lastname',String),
    Column('birthdate',DateTime),
    Column('comorbilidades',JSON))

enfermedades=Table('enfermedades',metadata,
    Column('id',Integer,primary_key=True,autoincrement=True),
    Column('enfermedad',String),
    Column('startDate',String),
    Column('endDate',String),
    Column('complications',String),
    Column('paciente_id',Integer,ForeignKey('paciente.id')))

#%%
df=pd.read_sql_table('paciente',con=engine)
df
# %%
dfenfe=pd.read_sql_table('enfermedades',con=engine)
dfenfe