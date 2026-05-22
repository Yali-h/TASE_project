from logging import exception

import boto3
import csv
from io import StringIO
from tase_trial.local_utils import logger
from botocore.exceptions import ClientError



s3 = boto3.client("s3")

BUCKET_NAME = "tase_data"




def getFile_byKey(file_key):
    try:
        response = s3.get_object(
            Bucket=BUCKET_NAME,
            Key=file_key
        )
        content = response["Body"].read().decode("utf-8")
        csv_buffer = StringIO(content)

        reader = csv.DictReader(csv_buffer)
    except:
        logger.simpleLog("Error getting file: " + file_key)
        return None

    return reader


def getHistFile_bySID(SID):
    #conversion from SID to key
    pref = "historic-data/"
    suf = ".csv"
    KeyFromSID = pref + SID + suf
    return getFile_byKey(KeyFromSID)


def getFiles_byPrefix(prefix):
    keys = []
    continuation_token = None

    # when calling for a list AWS might not tell us all the keys at once
    # that why we should hold a pointer that will progress between requests
    while True:
        request_info = {
            "Bucket": BUCKET_NAME,
            "Prefix": prefix
        }
        if continuation_token:
            request_info["ContinuationToken"] = continuation_token

        try:
            response = s3.list_objects_v2(**request_info)
            for obj in response.get("Contents", []):
                key = obj["Key"]
        except:
            logger.simpleLog("Error getting file list in getFiles_byPrefix")
            return []

        if not response.get("IsTruncated"):
            break
        continuation_token = response["NextContinuationToken"]

    return keys


def saveFile_byFields(key, rows, fieldnames):
    csv_buffer = StringIO()

    writer = csv.DictWriter(
        csv_buffer,
        fieldnames = fieldnames
    )

    writer.writeheader()
    writer.writerows(rows)

    try:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=csv_buffer.getvalue(),
            ContentType="text/csv"
        )
    except ClientError as e:
        logger.simpleLog("Error uploading file " + e)
        return None
    return  True


def delFile_ByKey(FileKey):
    try:
        s3.delete_object(
            Bucket=BUCKET_NAME,
            Key=FileKey
        )
    except ClientError as e:
        logger.simpleLog("failed deleting file " + FileKey + " from S3")
        return None
    logger.simpleLog("Deleted file from S3 - file: " + FileKey)
    return True


def delHistFile_bySID(SID):
    #conversion from SID to key
    pref = "historic-data/"
    suf = ".csv"
    KeyFromSID = pref + SID + suf
    return delFile_ByKey(KeyFromSID)


def saveHisFile(SID, rows, fieldnames):
    pref = "historic-data/"
    suf = ".csv"
    KeyFromSID = pref + SID + suf
    return saveFile_byFields(KeyFromSID, rows, fieldnames)


def delMulFiles_keys(keyList):
    objects = [{"Key": key} for key in keyList]
    try:
        s3.delete_objects(
            Bucket=BUCKET_NAME,
            Delete={
                "Objects": objects
            }
        )
    except exception as e:
        logger.simpleLog("failed batch deleting from S3 - " + e)
        return None
    return True


def DoesFileExist(key):
    try:
        s3.head_object(
            Bucket=BUCKET_NAME,
            Key=key
        )

        return True

    except ClientError as e:

        error_code = e.response["Error"]["Code"]
        if error_code == "404":
            return False
        logger.simpleLog("error when checking if file exists : " + key + " : " + error_code)
        raise
