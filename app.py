from typing import Annotated
from pydantic import BaseModel
from fastapi import FastAPI,Request,Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine,Table,MetaData,Column,Integer,String,DateTime,Float,JSON
from sqlalchemy.dialects.sqlite import insert

import pandas as pd

engine=create_engine('sqlite:///data.db')

metadata=MetaData()

paciente=Table('paciente',metadata,
    Column('id',Integer,primary_key=True,autoincrement=True),
    Column('firstName',String),
    Column('lastName',String),
    Column('dateOfBirth',String),
    Column('comorbilidades',JSON))

metadata.create_all(engine,checkfirst=True)



app = FastAPI()

class FormData(BaseModel):
    firstName: str
    lastName: str
    model_config={'extra':'allow'}

templates=Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root(request:Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit")
def submit(data: Annotated[FormData, Form()]):

    datadict=data.model_dump(mode="json")

    enfermedades=[]
    i=1
    while True:
        enfermedad = datadict.get(f"enfermedad{i}")
        startdate = datadict.get(f"startdate{i}")
        enddate = datadict.get(f"enddate{i}")

        # Esto es necesario porque el if con un string "" evalua a False
        if not enddate:
            enddate = "now"

        if enfermedad and startdate and enddate:
            enfermedades.append({
                "enfermedad": enfermedad,
                "startdate": startdate,
                "enddate": enddate
            })
            i += 1

            print("sigo aqui")
        else:
            break

    datadict['comorbilidades']=enfermedades
    # remove the original enfermedad, startdate, and enddate fields
    for key in list(datadict.keys()):
        if key.startswith("enfermedad") or key.startswith("startdate") or key.startswith("enddate"):
            del datadict[key]

    print(datadict)

    #datadf=pd.json_normalize(datadict)
    
    #datadf.to_csv('data.csv',index=False)

    with engine.connect() as conn:
        conn.execute(insert(paciente),datadict)
        conn.commit()

    
    return datadict

