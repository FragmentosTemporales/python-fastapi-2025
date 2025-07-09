from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os


# RUTAS

file_router = APIRouter()


@file_router.get(
        '/get_file',
        tags=["file"],
        status_code=200,
        response_description="Obtener archivo README.md.")
def get_file():
    # Navigate from routes directory to src directory, then to data
    file_path = os.path.join(os.path.dirname(__file__), 'data')
    file = os.path.join(file_path, "README.md")

    # Check if file exists before returning
    if not os.path.exists(file):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file, filename="README.md", media_type='text/markdown')
