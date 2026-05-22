import json
from pathlib import Path
import csv
import os
from io import StringIO
from tase_trial.local_utils import logger
# key formats are important against the S3



def read_csv_file(file_path):
    try:
        with open(
                file_path,
                "r",
                encoding="utf-8-sig"
        ) as f:

            reader = csv.DictReader(f)
            data = list(reader)

    except Exception as e:
        logger.simpleLog("Error saving data:" + str(e))
        return False

    return data


def getFiles_AllDaily():
    pass



def save_csv_file(csv_content, output_path):
    try:
        with open(
            output_path,
            "w",
            encoding="utf-8-sig",
            newline=""
        ) as f:
            f.write(csv_content)

    except Exception as e:
        logger.simpleLog("Error saving data:" + str(e))
        return False

    logger.simpleLog("CSV saved to: " + str(output_path))
    return True


def file_exists(folder_path, filename):

    full_path = os.path.join(
        folder_path,
        filename
    )

    return os.path.isfile(full_path)


def json_to_csv_string(data_json, fields_to_keep):
    csv_buffer = StringIO()

    writer = csv.DictWriter(
        csv_buffer,
        fieldnames=fields_to_keep
    )

    writer.writeheader()

    for row in data_json:

        filtered_row = {
            field: row.get(field)
            for field in fields_to_keep
        }

        writer.writerow(filtered_row)

    return csv_buffer.getvalue()

