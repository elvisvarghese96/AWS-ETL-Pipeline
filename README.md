# AWS-ETL-Pipeline

## **Overview**
This project contains an AWS Lambda function that serves as a serverless ETL (Extract, Transform, Load) pipeline. It is designed to automatically process raw JSON order data, flatten its structure, and store it in a more efficient format for analysis.

### How It Works
The pipeline is triggered automatically by an event-driven architecture and performs the following steps:

Trigger: The Lambda function is invoked every time a new JSON file is uploaded to the designated S3 bucket.

Extract: It reads the newly uploaded JSON file from the S3 bucket. The raw data contains nested structures with order and customer details, along with a list of products.

Transform: The transform function processes the raw JSON data. It uses the pandas library to flatten the nested product information, creating a single, denormalized record for each product within an order.

Load: The transformed data is then converted into the Apache Parquet format, which is highly optimized for analytical queries. The Parquet file is then saved to a staging sub-directory in the same S3 bucket, named with a timestamp for versioning.

Post-Processing: Finally, the function triggers an AWS Glue Crawler to automatically discover the schema of the newly created Parquet file and update the AWS Glue Data Catalog. This makes the transformed data immediately available for querying via services like Amazon Athena.

### Technologies Used
AWS Lambda: The serverless compute service that hosts the Python ETL code.

Amazon S3: Used as the data lake for both raw JSON files and the processed Parquet files.

Boto3: The AWS SDK for Python, used to interact with S3 and Glue services.

Pandas: A Python data analysis library essential for the data transformation step.

Pyarrow: Used by Pandas to efficiently write the data into the Parquet file format.

AWS Glue: A fully managed ETL service, specifically its crawler, used to discover and catalog the transformed data.

### Lambda Function Breakdown
Transform(data): This core function takes the raw JSON data (a list of dictionaries) and flattens it into a list of dictionaries, one for each product. It then converts this into a pandas.DataFrame.

lambda_handler(event, context): The entry point of the Lambda function. It handles the S3 trigger event, fetches the file, calls the transform function, and orchestrates the loading and Glue Crawler steps.

Dependencies: The function requires the following libraries, which must be included in the deployment package: boto3, pandas, pyarrow.

### Setup & Deployment
Created an S3 Bucket with a designated folder for raw data (e.g., raw_orders_data/) and a staging folder for the processed Parquet files (e.g., orders_data_parquet/).

Lambda Function: Deployed package (a .zip file) containing the Python code and its dependencies (pandas, pyarrow).

Created the Lambda Function: In the AWS Management Console, created a new Lambda function with the code from this project. Configure the handler as lambda_function.lambda_handler.

Configured the S3 Trigger: Add an S3 trigger to the Lambda function. Set it to trigger on a Put event in your raw_orders_data/ folder.

Glue Crawler: Set up an AWS Glue Crawler named etl-pipeline-orders. Configure its data source to be the orders_data_parquet/ folder in your S3 bucket.