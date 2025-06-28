from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
import psycopg.rows
from pydantic import BaseModel
from typing import Optional
import random
import psycopg
import time
from app.Environment_variables import *
class Incident(BaseModel):
    short_description:str
    description:str
    priority:int
    id:Optional[int] = None

app = FastAPI()

maxattempts = 5
retriedattempts = 1
while retriedattempts<=maxattempts:
    try:
        conn = psycopg.connect(
        host=dbhost,
        dbname=dbname,
        user=dbuser,   # ✅ correct parameter name and spelling
        password=dbpass,
        row_factory=psycopg.rows.dict_row)
        cursor = conn.cursor()
        print("Database Connected successfully")
        break
    except Exception as E:
        print("Database Connection failed")
        print("Error: "+str(E))
        time.sleep(2)
    
    finally:
        print(f"Attempt: {retriedattempts} to connect to db server")
        retriedattempts+=1
    if retriedattempts >maxattempts:
        print("Max Attempt and unable to connect to db server")

        break

my_incidents = [{'id':1,'short_description':'internet issue','desc':'internet not working for user alice'},
                {'id':2,'short_description':'mouse issue','desc':'mouse not working for user john doe'}]


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/yrl")
async def root():
    return {"message": "Hello yrl"}

@app.post("/incident")
def create_incident(payload:dict=Body()):
    print(payload)
    return {'data':'incident created successfully'}

@app.post("/Incident")
def create_incident(payload:Incident):
    print(payload.model_dump())
    return {'data':payload}

@app.get("/incidents")
def create_incident():
    # print(payload)
    # return {'data':'incident created successfully'}
    return {'data':my_incidents}

@app.get("/incidents/{id}")
def get_incident(id:int,response:Response):
# def get_incident(id:int):
    incident = [incident for incident in my_incidents if incident['id']==id]
    
    if len(incident)==0:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return 'notfound'
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'incident with this id:{id} not found')

    else:
        return {'data':incident[0]}


@app.post("/incidents",status_code=status.HTTP_201_CREATED)
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

@app.put("/incidents/{id}")
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

@app.delete("/incidents/{id}",status_code=status.HTTP_204_NO_CONTENT)
def create_new_incident(id:int):
    existing_incident_ids = [incident['id'] for incident in my_incidents]
    data_id = id
    if data_id is not None and data_id not in existing_incident_ids:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"incident with this id: {id} not found")
    else:
        record_index = find_existing_incident_index(data_id)
        my_incidents.pop(record_index)
        return
    


@app.get("/posts")
def create_incident():
    # print(payload)
    # return {'data':'incident created successfully'}
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {'data':posts}

@app.get("/posts/{id}")
def get_post_by_id(id:int,response:Response):
# def get_incident(id:int):
    cursor.execute(f"""SELECT * FROM posts WHERE id={id}""")    
    posts= cursor.fetchone()
    print(type(posts))
    if posts is None or len(posts)==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with this id:{id} not found')

    else:
        return {'data':posts}
