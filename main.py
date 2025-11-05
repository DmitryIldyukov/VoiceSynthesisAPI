from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from gtts import gTTS
import os
import uuid

app = FastAPI(title="Voice Synthesis API")

def remove_file(path: str):
    if os.path.exists(path):
        os.remove(path)

@app.post("/synthesize/")
def synthesize(text: str, lang: str = "en", background_tasks: BackgroundTasks = None):
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    filename = f"{uuid.uuid4()}.mp3"
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Unsupported language code: {lang}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Удаляем файл после того, как ответ будет отправлен клиенту
    background_tasks.add_task(remove_file, filename)
    return FileResponse(filename, media_type="audio/mpeg", filename="speech.mp3")
