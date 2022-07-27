
import pandas as pd
import re
import numpy as np
import csv
import boto3


def process_line(line):
    regex_result = re.search(r"\[(\d{1,2}\/\d{1,2}\/\d{2}) (\d\d:\d\d:\d\d)\] ([\w| ]*): (.*)$", line)
    name_in_line = regex_result.group(3)
    message = regex_result.group(4)

    return {
            "label": name_in_line,
            "Message_Clean": message,
            "text": message.lower(),
           }

def is_valid_message(message):
    m = re.search(r"^(\w|\s)*$", message)
    return m is not None

def handler(event, context):
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    filename = event["Records"][0]["s3"]["object"]["key"]

    s3_handler = boto3.client("s3")


    file_content = s3_handler.get_object(Bucket=bucket, Key=filename)["Body"].read()
    print(file_content)

    # after_process = pd.DataFrame()
    #
    # with open("./Alloy_Del_Negro-Clean.txt", "r") as chat:
    #     for line in chat:
    #         try:
    #             after_process = after_process.append(process_line(line), ignore_index=True)
    #         except Exception as err:
    #             print(err)
    #             print(line)
    #             pass
    #
    #
    # after_process = after_process[after_process["text"].apply(is_valid_message)]
    #
    # after_process.to_csv("./alloy_dataset", columns=["label", "text"], index=False,quoting=csv.QUOTE_NONNUMERIC)
