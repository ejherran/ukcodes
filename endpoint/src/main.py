from fastapi import FastAPI, File, UploadFile
from file_analyzer import FileAnalizer

from celery.result import AsyncResult
from tasks import analyze_file

app = FastAPI()

@app.post('/ukcodes/upload')
async def create_coordinates_file(file: UploadFile = File(...)):
    
    if file.content_type == 'text/csv':
        
        task = analyze_file.delay(file.file.read().decode('utf-8'))

        return {'statusCode': 200, 'status': 'OK','success': True, 'task_id': task.id, 'message': f'The file has been uploaded successfully. Go to /ukcodes/{task.id} to check the task state.'}

    else:
        return {'statusCode': 415, 'status': 'Unsupported Media Type','success': False, 'error_message': 'The content type must be text/csv.'}

@app.get('/ukcodes/{task_id}')
async def get_task_status(task_id: str):
    task = AsyncResult(task_id)
    
    if task.successful():

        if len(task.result) == 0:
            return {"statusCode": 200, "status": "OK","success": True, "message": "The file has been successfully processed."}
        else:
            return {"statusCode": 200, "status": "OK", "success": True, "message": "The file has been successfully processed, but the lines with warnings have been discarded", "warnings": task.result}
    
    elif task.failed():
        return {'statusCode': 500, 'status': 'Internal Server Error'}
    
    else:
        return {'statusCode': 200, 'status': 'Pendiente'}