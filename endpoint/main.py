from fastapi import FastAPI, File, UploadFile
from file_analyzer import FileAnalizer

app = FastAPI()

@app.post("/uploadcoordinates/")
async def create_coordinates_file(file: UploadFile = File(...)):
    
    if file.content_type == 'text/csv':
        
        file_analyzer = FileAnalizer(file.file)
        coordinates, warnings = file_analyzer.analyze()
        
        if len(warnings) == 0:
            return {"statusCode": 200, "status": "OK","success": True, "message": "The file has been uploaded successfully."}
        else:
            return {"statusCode": 200, "status": "OK", "success": True, "message": "The file has been uploaded successfully, but the lines with warnings have been discarded", "warnings": warnings}

    else:
        return {"statusCode": 415, "status": "Unsupported Media Type","success": False, "error_message": "The content type must be text/csv."}