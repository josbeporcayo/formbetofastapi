from typing import Annotated
from pydantic import BaseModel
from fastapi import FastAPI,Request,Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine,Table,MetaData,Column,Integer,String,DateTime,Float,JSON,ForeignKey
from sqlalchemy.dialects.sqlite import insert

import pandas as pd

engine=create_engine('sqlite:///data.db')

metadata=MetaData()

pacientetable=Table('paciente',metadata,
    Column('id',Integer,primary_key=True,autoincrement=True),
    Column('firstName',String),
    Column('lastName',String),
    Column('dateOfBirth',String),)

enfermedadestable=Table('enfermedades',metadata,
    Column('id',Integer,primary_key=True,autoincrement=True),
    Column('enfermedad',String),
    Column('startdate',String),
    Column('enddate',String),
    Column('complications',String),
    Column('paciente_id',Integer,ForeignKey('paciente.id')))

metadata.create_all(engine,checkfirst=True)



app = FastAPI()

class FormData(BaseModel):
    firstName: str
    lastName: str
    model_config={'extra':'allow'}

class EnfermedadesData(BaseModel):
    vaccinationStatus: str
    model_config={'extra':'allow'}

templates=Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root(request:Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submitpaciente")
def submit(data: Annotated[FormData, Form()]):

    datadict=data.model_dump(mode="json")

    #datadf=pd.json_normalize(datadict)
    
    #datadf.to_csv('data.csv',index=False)

    with engine.connect() as conn:
        conn.execute(insert(pacientetable),datadict)
        conn.commit()

    
    return RedirectResponse(url="/comorbilidades", status_code=302)

@app.get("/comorbilidades")
def read_root(request:Request):
    return templates.TemplateResponse("comorbilidades.html", {"request": request})

@app.post("/submitenfermedades")
def submit(data: Annotated[EnfermedadesData, Form()]):

    datadict=data.model_dump(mode="json")

    with engine.connect() as conn:
        findidquery='SELECT MAX(id) AS last_id FROM paciente'
        lastid=pd.read_sql(findidquery,con=conn)
        lastid=int(lastid['last_id'][0])
    
    enfermedades=[]
    i=1
    while True:
        enfermedad = datadict.get(f"enfermedad{i}")
        startdate = datadict.get(f"startdate{i}")
        enddate = datadict.get(f"enddate{i}")
        complications=datadict.get(f"complications{i}")

        # Esto es necesario porque el if con un string "" evalua a False
        if not enddate:
            enddate = "now"

        if enfermedad and startdate and enddate and complications:
            enfermedades.append({
                "enfermedad": enfermedad,
                "startdate": startdate,
                "enddate": enddate,
                "complications": complications,
                "paciente_id":lastid
            })
            i += 1

        else:
            break

    with engine.connect() as conn:
        conn.execute(insert(enfermedadestable),enfermedades)
        conn.commit()

    return enfermedades

@app.get("/enfermedadesasociadas")
def asociadasdata():
    with engine.connect() as conn:
        asocquery='''
                    SELECT * 
                    FROM enfermedades
                    WHERE paciente_id IN (SELECT MAX(id) AS last_id FROM paciente)'''
        asocpd=pd.read_sql(asocquery,con=conn)
    
    return asocpd.to_dict(orient='records')