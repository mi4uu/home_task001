from fastapi import APIRouter, File, UploadFile

router = APIRouter()


@router.get("/")
async def list_files():
    return ["Hello", "World"]


@router.get("/{item_id}")
async def get_file(id: int):
    return {
        "Hello": "World",
    }


@router.post("/", status_code=201)
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        await file.close()

    return {"message": f"Successfuly uploaded {file.filename}"}
