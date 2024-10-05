from fastapi import FastAPI, File, UploadFile, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models.violence_detection_model import FightDetectionModel
import os
import shutil
from uuid import uuid4
import asyncio

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

# Mount the annotated_videos directory to serve annotated videos
annotated_videos_dir = os.path.join(os.path.dirname(__file__), 'annotated_videos')
os.makedirs(annotated_videos_dir, exist_ok=True)
app.mount("/annotated_videos", StaticFiles(directory=annotated_videos_dir), name="annotated_videos")

# Set up templates
templates = Jinja2Templates(directory="../frontend/templates")

# Initialize the model
model_path = os.path.join('..', 'fight_detection_yolov8', 'Yolo_nano_weights.pt')
model = FightDetectionModel(model_path)

# Ensure uploads directory exists
uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(uploads_dir, exist_ok=True)

# Dictionary to manage WebSocket connections
connections = {}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    connections[client_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            # This server does not expect to receive messages, but you can handle if needed
    except WebSocketDisconnect:
        del connections[client_id]

@app.post("/detect")
async def detect_violence(request: Request, video: UploadFile = File(...)):
    if not video:
        return JSONResponse(content={"error": "No video file provided"}, status_code=400)
    
    if video.filename == "":
        return JSONResponse(content={"error": "No selected file"}, status_code=400)
    
    # Extract client_id from request headers for WebSocket
    client_id = request.headers.get('client-id')
    websocket = connections.get(client_id)
    if not websocket:
        return JSONResponse(content={"error": "WebSocket connection not established"}, status_code=400)
    
    # Generate a unique filename to prevent collisions
    unique_filename = f"{uuid4().hex}_{video.filename}"
    video_path = os.path.join(uploads_dir, unique_filename)
    
    # Save the uploaded video
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)
    
    # Define the path for the annotated video
    annotated_filename = f"annotated_{unique_filename}"
    annotated_video_path = os.path.join(annotated_videos_dir, annotated_filename)
    
    try:
        # Run the detection
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(None, model.detect, video_path, annotated_video_path, websocket)
    except Exception as e:
        # Handle exceptions during detection
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
    # Optionally, delete the uploaded video after processing to save space
    os.remove(video_path)
    
    # Create a URL for the annotated video
    annotated_video_url = f"/annotated_videos/{annotated_filename}"
    
    # Add the annotated video URL to the results
    results['annotatedVideoUrl'] = annotated_video_url
    
    return JSONResponse(content=results, status_code=200)
