from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Union
from fastapi.middleware.cors import CORSMiddleware
import base64
import magic 

# API DONE BY MUKUND PU RA2111027020101

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PostRequestData(BaseModel):
    data: List[Union[str, int]]
    file_b64: Union[str, None] = None 

@app.api_route("/bfhl", methods=["GET", "POST"])
async def bfhl(request: Request, post_request: PostRequestData = None):
    if request.method == "GET":
        return {"operation_code": 1}

    elif request.method == "POST":
        try:
            # Sample hardcoded values
            full_name = "john_doe"
            dob = "17091999"
            user_id = f"{full_name}_{dob}"
            email = "john@xyz.com"
            roll_number = "ABCD123"

            numbers = []
            alphabets = []

            # Separate numbers and alphabets
            for item in post_request.data:
                if isinstance(item, str) and item.isalpha():
                    alphabets.append(item)
                else:
                    numbers.append(str(item))

            # Filter only lowercase alphabets and find the highest
            lowercase_alphabets = [char for char in alphabets if char.islower()]
            highest_lowercase_alphabet = max(lowercase_alphabets) if lowercase_alphabets else ""

            # Initialize response fields
            response = {
                "is_success": True,
                "user_id": user_id,
                "email": email,
                "roll_number": roll_number,
                "numbers": numbers,
                "alphabets": alphabets,
                "highest_lowercase_alphabet": [highest_lowercase_alphabet] if highest_lowercase_alphabet else [],
                "file_valid": False  # Default value, change if file is given
            }

            # Handle file validation (Base64)
            if post_request.file_b64:
                try:
                    # Decode Base64
                    file_data = base64.b64decode(post_request.file_b64)
                    
                    # Detect the file's MIME type
                    mime = magic.Magic(mime=True)
                    file_mime_type = mime.from_buffer(file_data)
                    file_size_kb = len(file_data) / 1024  # File size in KB
                    
                    # Update response with file details
                    response.update({
                        "file_valid": True,
                        "file_mime_type": file_mime_type,
                        "file_size_kb": round(file_size_kb, 2)
                    })
                except Exception as e:
                    response["file_valid"] = False

        except Exception as e:
            response = {
                "is_success": False,
                "error": str(e)
            }

        return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
