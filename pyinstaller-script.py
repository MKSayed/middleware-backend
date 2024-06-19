import uvicorn
import multiprocessing
import main

if __name__=="__main__":
    multiprocessing.freeze_support()  # To prevent possible recursions with multiple workers
    uvicorn.run("main:app", host="localhost", port=8000, reload=False, workers=5)