from typing import Annotated

from fastapi import APIRouter, UploadFile, Request, Response, status
from fastapi.responses import FileResponse
import os

from api.deps import CurrentUserDep

router = APIRouter()

# In-memory storage for updates (you can use a database or file system for persistence)
updates = {}


# Endpoint to upload a new update
@router.post("/upload-update")
async def upload_update(update_file: UploadFile, machine_ids: list[str] = None):
    file_path = f"updates/{update_file.filename}"
    with open(file_path, "wb") as f:
        contents = await update_file.read()
        f.write(contents)

    # for machine_id in machine_ids:
    #     updates[machine_id] = file_path

    done = {"message": "Update uploaded successfully"}
    print(done)
    return done


# Endpoint to check for available updates
@router.get("/check-update/{machine_id}")
async def check_update(machine_id: str):
    update_path = updates.get(machine_id)
    if update_path:
        return {"update_available": True, "update_path": update_path}
    else:
        return {"update_available": False}


# Dictionary to hold the update info for each machine
updates_info = {
    "machine1": {"version": "1.0.1", "fileName": "update1.zip"},
    "machine2": {"version": "1.0.2", "fileName": "update2.zip"},
}


# Endpoint to download the update file
# If "useMultipleRangeRequest": true which means the electron app will
# send a single request picking all byte ranges in 1 request
@router.get("/download-update/{update_path:path}")
async def download_update(update_path: str, request: Request):
    print(request.headers)
    file_path = f"updates/{update_path}"
    if not os.path.exists(file_path):
        return {"message": "Update file not found"}

    file_size = os.path.getsize(file_path)
    range_header = request.headers.get("Range")
    if range_header:
        content_type = "application/octet-stream"  # MIME type for binary files
        boundary = "3d6b6a416f9b5"  # Random unique string for the boundary
        multipart_content = []

        # Splitting the Range header to handle multiple ranges
        ranges = range_header.replace("bytes=", "").split(",")
        for part in ranges:
            start_end = part.split("-")
            start = int(start_end[0])
            end = int(start_end[1]) if start_end[1] else file_size - 1

            if start >= file_size or end >= file_size:
                return Response(
                    status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
                    headers={"Content-Range": f"bytes */{file_size}"},
                )  # Range Not Satisfiable

            length = end - start + 1
            with open(file_path, "rb") as f:
                f.seek(start)
                data = f.read(length)
            multipart_content.append(
                f"--{boundary}\r\n"
                f"Content-Type: {content_type}\r\n"
                f"Content-Range: bytes {start}-{end}/{file_size}\r\n\r\n".encode(
                    "utf-8"
                )
            )
            multipart_content.append(data)  # Appending binary data directly

        multipart_content.append(f"\r\n--{boundary}--".encode("utf-8"))
        full_response = b"".join(multipart_content)
        headers = {
            "Content-Type": f"multipart/byteranges; boundary={boundary}",
            "Accept-Ranges": "bytes",
        }
        print("PartTTTTTTTTTTTTTTTTTTT returning")
        return Response(
            content=full_response,
            status_code=status.HTTP_206_PARTIAL_CONTENT,
            headers=headers,
        )
    else:
        print("FULLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL returning")
        return FileResponse(file_path, media_type="application/octet-stream")


# # Endpoint to download the update file
# # If "useMultipleRangeRequest": false which means the electron app will
# # send hundreds of requests picking 1-byte-range per request
# @router.get("/download-update/{update_path:path}")
# async def download_update(update_path: str, request: Request):
#     print(request.headers)
#     file_path = f"updates/{update_path}"
#     if not os.path.exists(file_path):
#         return {"message": "Update file not found"}
#
#     file_size = os.path.getsize(file_path)
#     range_header = request.headers.get('Range')
#     if range_header:
#         ranges = range_header.replace("bytes=", "").split("-")
#         start = int(ranges[0])
#         end = int(ranges[1]) if ranges[1] else file_size - 1
#
#         if start >= file_size or end >= file_size:
#             return Response(status_code=416, headers={"Content-Range": f"bytes */{file_size}"})  # Range Not Satisfiable
#
#         length = end - start + 1
#         with open(file_path, 'rb') as f:
#             f.seek(start)
#             data = f.read(length)
#         headers = {
#             "Content-Range": f"bytes {start}-{end}/{file_size}",
#             "Content-Length": str(length),
#             "Accept-Ranges": "bytes",
#             "Content-Type": "application/octet-stream",  # or the appropriate MIME type
#         }
#         print("PartTTTTTTTTTTTTTTTTTTT returning")
#         return Response(content=data, status_code=206, headers=headers)
#     else:
#         print("FULLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL returning")
#         return FileResponse(file_path, media_type='application/octet-stream')
