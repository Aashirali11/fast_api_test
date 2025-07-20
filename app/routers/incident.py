import psycopg
import time
from fastapi import APIRouter, Depends, HTTPException, status,Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
router = APIRouter(
    tags=["Incidents"],
    prefix="/api/v0"
)



class Incident(BaseModel):
    short_description:str
    description:str
    priority:int
    id:Optional[int] = None



my_incidents = [{'id':1,'short_description':'internet issue','desc':'internet not working for user alice'},
                {'id':2,'short_description':'mouse issue','desc':'mouse not working for user john doe'}]


@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.get("/yrl")
async def root():
    return {"message": "Hello yrl"}

@router.post("/incident")
def create_incident(payload:dict=Body()):
    print(payload)
    return {'data':'incident created successfully'}

@router.post("/Incident")
def create_incident(payload:Incident):
    print(payload.model_dump())
    return {'data':payload}

@router.get("/incidents")
def create_incident():
    # print(payload)
    # return {'data':'incident created successfully'}
    return {'data':my_incidents}

@router.get("/incidents/{id}")
def get_incident(id:int,response:Response):
# def get_incident(id:int):
    incident = [incident for incident in my_incidents if incident['id']==id]
    
    if len(incident)==0:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return 'notfound'
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'incident with this id:{id} not found')

    else:
        return {'data':incident[0]}


@router.post("/incidents",status_code=status.HTTP_201_CREATED)
def create_new_incident(payload:Incident):
    print(payload.model_dump())
    existing_incident_ids = [incident['id'] for incident in my_incidents]
    data_id = payload.id
    if data_id is None and data_id not in existing_incident_ids:
        new_incident_id = my_incidents[-1]['id'] +1 
        payload.id = new_incident_id
        my_incidents.append(payload.model_dump())
        return {'data':payload}
    else:
        existing_record = [incident for incident in my_incidents if incident['id'] == data_id][0]
        return {'data':f"incidents already exist with this id:{data_id}  records: {existing_record}"}

def find_existing_incident_index(id=''):
    record_index = None
    incident_index = [index for index,incident in enumerate(my_incidents) if incident['id']==id]
    
    if len(incident_index)>0:
        record_index = incident_index[0]
    return record_index

@router.put("/incidents/{id}")
def create_new_incident(payload:Incident,id:int):
    existing_incident_ids = [incident['id'] for incident in my_incidents]
    data_id = id
    if data_id is not None and data_id not in existing_incident_ids:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"incident with this id:{id} not found")
    else:
        record_index = find_existing_incident_index(data_id)
        print('Incident put -> record index',record_index)
        my_incidents[record_index]=payload
        return {'data':payload}

@router.delete("/incidents/{id}",status_code=status.HTTP_204_NO_CONTENT)
def create_new_incident(id:int):
    existing_incident_ids = [incident['id'] for incident in my_incidents]
    data_id = id
    if data_id is not None and data_id not in existing_incident_ids:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"incident with this id: {id} not found")
    else:
        record_index = find_existing_incident_index(data_id)
        my_incidents.pop(record_index)
        return
    