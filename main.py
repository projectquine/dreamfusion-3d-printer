import asyncio, glob, os
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

df_working_directory = '/home/ubuntu/stable-dreamfusion'

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

async def run_training(cmd):
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    print(stdout)

@app.post("/model/")
async def create_model(model: Model, request: Request, background_tasks: BackgroundTasks):
    print(f'creating model with input text: {model.text}')
    cmd = f'python {df_working_directory}/main.py --text "{model.text}" --workspace {model.workspace} --iters {model.iterations}'
    print(cmd)
    background_tasks.add_task(run_training, cmd)
    print(request.url)
    return URL(uri=f'{request.url}{model.workspace}')

@app.get("/model/{uuid}/obj")
async def get_object_file(uuid):
    dir_path = os.getcwd() +'/'+ uuid + '/mesh'
    files = glob.glob(dir_path+'/*.obj')
    if files == []:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(files[0])

@app.get("/model/{uuid}/mtl")
async def get_mtl_file(uuid):
    dir_path = os.getcwd() +'/'+ uuid + '/mesh'
    files = glob.glob(dir_path+'/*.mtl')
    if files == []:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(files[0])

@app.get("/model/{uuid}/result")
async def get_result_video_file(uuid):
    dir_path = os.getcwd() +'/'+ uuid + '/results'
    files = glob.glob(dir_path+'/*.mp4')
    print(files)
    if files == []:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(files[0])

@app.get("/model/{uuid}/validation")
async def get_latest_validation_file(uuid):
    dir_path = os.getcwd() +'/'+ uuid + '/validation'
    files = glob.glob(dir_path+'/*_rgb.png')
    files.sort(key=lambda x: os.path.getmtime(x))
    print(files)
    if files == []:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(files[0])