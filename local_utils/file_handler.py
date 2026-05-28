
from pathlib import Path
import csv
import os
from io import StringIO
from tase_trial.local_utils import logger
import pandas as pd



# key formats are important against the S3

# given file path, returns the file as csv - data list
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


# the csv content, and a file path, saves data to file. Overwrite if needed
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


# checks if there is a file by a certain name
def file_exists(full_path):
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


def jsonToCSV(data_json, fields_to_keep):
    df = pd.DataFrame(data_json)
    try:
        df = df[fields_to_keep]
    except Exception as e:
        logger.simpleLog("Error converting JSON to CSV: " + str(e))
    return df


def allFilesInDir(dir_path):
    csv_files = list(dir_path.glob("*.csv"))
    return csv_files


def save_pds_csv(PDdata_file, output_path):
    try:
        PDdata_file.to_csv(output_path, index = False)

    except Exception as e:
        logger.simpleLog("Error saving data:" + str(e))
        return False

    logger.simpleLog("CSV saved to: " + str(output_path))
    return True


def read_pds_csv(filePath):

    try:
        fileLoaded = pd.read_csv(
            filePath,
            encoding="utf-8-sig"
        )

    except Exception as e:
        logger.simpleLog("Error reading data: " + str(e))
        return False

    return fileLoaded


