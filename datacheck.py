#%%
from sqlalchemy import create_engine,MetaData,Table,Column,Integer,String,DateTime,JSON
import pandas as pd
engine=create_engine('sqlite:///data.db')

metadata=MetaData()

paciente=Table('paciente',metadata,
    Column('id',Integer,primary_key=True,autoincrement=True),
    Column('firstname',String),
    Column('lastname',String),
    Column('birthdate',DateTime),
    Column('comorbilidades',JSON))

#%%
df=pd.read_sql_table('paciente',con=engine)
df
# %%
