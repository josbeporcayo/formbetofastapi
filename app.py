from typing import Annotated
from pydantic import BaseModel
from fastapi import FastAPI,Request,Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import pandas as pd

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

    listaenfermedades=[]
    listastartdate=[]
    listaenddates=[]

    for key in datadict:

        if 'enfermedad' in key:
            listaenfermedades.append(datadict[key])

        elif 'startdate' in key:
            listastartdate.append(datadict[key])

        elif 'enddate' in key:
            listaenddates.append(datadict[key])

        else:
            continue
    
    datadictfinal={'firsname':datadict['firstName'],
                   'lastname':datadict['lastName'],
                   'enfermedades':listaenfermedades,
                   'startdates':listastartdate,
                   'enddates':listaenddates}

    datadf=pd.json_normalize(datadictfinal)
    
    datadf.to_csv('data.csv',index=False)
    return data

