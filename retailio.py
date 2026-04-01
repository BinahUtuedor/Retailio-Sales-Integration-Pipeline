import os
import boto3
import pandas as pd
import awswrangler as wr
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

access = os.getenv("ACCESS_KEY")
secret = os.getenv("SECRET_KEY")
region = os.getenv("REGION")
bucket = "retailio-data-lake-eng"

# Validate credentials
if not all([access, secret, region]):
    raise ValueError("Missing AWS credentials or region in environment variables.")

session = boto3.Session(
    aws_access_key_id=access,
    aws_secret_access_key=secret,
    region_name=region
)

datasets = {
    "products": "data/product_V2.csv",
    "customers": "data/customer_V2.csv",
    "sales": "data/sales_V2.csv",
}

for name, path in datasets.items():
    if Path(path).is_file():
        df = pd.read_csv(path, encoding='latin1')
        wr.s3.to_parquet(
            df=df,
            path=f"s3://{bucket}/raw/{name}/",
            index=False,
            mode='overwrite',
            dataset=True,
            boto3_session=session
        )
        print(f"Uploaded {name} successfully.")
    else:
        print(f"Path does not exist: {path}")
