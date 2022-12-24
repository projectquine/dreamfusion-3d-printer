import asyncio, glob, os
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

df_working_directory = '/Users/shaunmulligan/Desktop/dreamfusion-project/df-api'

class Model(BaseModel):
    text: str
    workspace: UUID = Field(default_factory=uuid4)
    iterations = 10000

class URL(BaseModel):
    uri: str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/model/")
async def create_model(model: Model, request: Request):
    print(f'creating model with input text: {model.text}')
    cmd = f'python3 df.py --text "{model.text}" --workspace {model.workspace} --iters {model.iterations}'
    print(cmd)
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    print(request.url)
    if stderr:
        raise HTTPException(status_code=404, detail="Could not start training")
    return URL(uri=f'{request.url}/{model.workspace}')

@app.get("/model/{uuid}/obj")
async def get_object_file(uuid):
    dir_path = df_working_directory +'/'+ uuid + '/mesh'
    files = glob.glob(dir_path+'/*.obj')
    if files == []:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(files[0])

@app.get("/model/{uuid}/mtl")
async def get_mtl_file(uuid):
    dir_path = df_working_directory +'/'+ uuid + '/mesh'
    files = glob.glob(dir_path+'/*.mtl')
    if files == []:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(files[0])

@app.get("/model/{uuid}/result")
async def get_result_video_file(uuid):
    dir_path = df_working_directory +'/'+ uuid + '/results'
    files = glob.glob(dir_path+'/*.mp4')
    print(files)
    if files == []:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(files[0])

@app.get("/model/{uuid}/validation")
async def get_latest_validation_file(uuid):
    dir_path = df_working_directory +'/'+ uuid + '/validation'
    files = glob.glob(dir_path+'/*.png')
    files.sort(key=lambda x: os.path.getmtime(x))
    if files == []:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(files[0])