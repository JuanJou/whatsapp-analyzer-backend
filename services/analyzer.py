import pandas as pd
from fastapi import UploadFile
import re
from datetime import datetime



async def parse_file(lines: str):
    print(f"Parse file")
    processed_file = pd.DataFrame()
    all_chat = lines.replace("\n", " ")
    splitted_chat = re.findall("\d{1,2}\/\d{1,2}\/\d{4}, \d{1,2}:\d{2} - \+[()\d\w\s-]+: [\s\S]*?(?=\d{1,2}\/\d{1,2}\/\d{4}, \d{1,2}:\d{2} - \+|$)", all_chat)
    for line in splitted_chat:
        try:
            processed_line = process_line(line)
            processed_file = pd.concat([processed_file, processed_line])
        except Exception as err:
            pass
    return processed_file

def process_line(line):
    #10/3/2024, 12:44 - +54 9 11 3763-1285: Muchas Gracias !!! Ya compre entradas.
    regex_result = re.search("^(\d{1,2}\/\d{1,2}\/\d{4}), (\d\d:\d\d) - (\+(\d*) (?:9 (\d*)|([()\d\w\s-]*))([()\d\w\s-]*)): ([\s\S]*)$", line)
    raw_message = line
    date = regex_result.group(1)
    time = regex_result.group(2)
    phone_number = regex_result.group(3)
    message = regex_result.group(8)
    date = datetime.strptime(f"{date} {time}", "%d/%m/%Y %H:%M")
    return pd.DataFrame([{
            "user": phone_number,
            "raw_message": raw_message,
            "clean_message": message,
            "lower_message": message.lower() ,
            "date": date,
            "hour": date.hour,
            "day_of_the_week": date.weekday()
           }])

async def parse_pickle(uuid):
    df = pd.read_pickle(f"{uuid}.pkl")
    print(f"HEAD: {df.head()} ")
    return df
