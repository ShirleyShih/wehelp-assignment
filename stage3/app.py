# uvicorn app:app --reload
from fastapi import *
from fastapi import FastAPI, Request, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error
# from dbconfig import db_config # connect to dbconfig.py
import uuid

app=FastAPI()

load_dotenv()  # Load environment variables from .env file
# Initialize S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name=os.environ.get('AWS_REGION')
)

# Define S3 bucket
S3_BUCKET = os.environ.get('AWS_BUCKET_NAME')

# Database connection configuration
RDS_PASSWORD = os.environ.get('AWS_RDS_PASSWORD')
db_config = {
    'user': 'admin',
    'password': f"{RDS_PASSWORD}",
    'host': 'wehelpstage34.cb280weeg64t.us-west-2.rds.amazonaws.com',
    'database': 'wehelpstage3'
}

@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./index.html", media_type="text/html")

@app.get("/api/message")
async def get_message():
    try:
        con = mysql.connector.connect(**db_config)
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT textContent, imageURL FROM stage3")
        result = cursor.fetchall()
        cursor.close()
        con.close()

        if result:
            return {"data": result}
        else:
            return {"error": True, "message": "message not found"}

    except Error as e:
        return {"error": True, "message": str(e)}


@app.post("/api/message")
async def create_message(textContent: str = Form(...), fileInput: UploadFile = File(...)):
    try:
        # Upload file to S3
        print(textContent,fileInput)
        file_content = await fileInput.read()
        print("File content read successfully")

        imageno=str(uuid.uuid4())
        s3.put_object(
            Body=file_content,
            Bucket=S3_BUCKET,
            Key=imageno #fileInput.filename
        )
        print("File uploaded to S3 successfully")

        # file_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{fileInput.filename}"
        file_url = f"https://d3cutng1gh49pz.cloudfront.net/{imageno}"
        print(f"File URL: {file_url}")

        con = mysql.connector.connect(**db_config)
        cursor=con.cursor()
        cursor.execute("insert into stage3(textContent,imageURL) values(%s,%s)",(textContent,file_url))
        con.commit()
        cursor.close()
        con.close()

        # Return response
        return {
            "ok": True,
            "textContent": textContent,
            "imageURL": file_url
        }
    except NoCredentialsError:
        raise HTTPException(status_code=403, detail="AWS credentials are not available")
    except PartialCredentialsError:
        raise HTTPException(status_code=403, detail="Incomplete AWS credentials")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))