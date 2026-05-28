from tase_trial.tase_interactions import tase_requests
from tase_trial.local_utils import file_handler
from datetime import datetime
from tase_trial.local_utils import logger
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[0]
DAILY_PATH = ROOT_DIR / "testing_data/daily_data/"


# Running a request for all the daily data using Tase
def runDailyRequest():
    try:
        current_date = datetime.now().strftime("%d-%m-%Y")
    except Exception as e:
        logger.simpleLog("failed to get date: " + str(e))
        return False
    logger.simpleLog("running daily request - today is " + current_date)

    fileName = current_date + ".csv"

    if file_handler.file_exists(DAILY_PATH / fileName):
        logger.simpleLog("denied running daily request - file " + fileName + " already exists")
        return True
    response_JSON = tase_requests.reqAllBonds()

    if response_JSON is False:
        logger.simpleLog("failed to act on daily request")
        return False

    DataDate = response_JSON["Date1"].replace("/", "-")
    fileName = DataDate[:10] + ".csv"
    if file_handler.file_exists(DAILY_PATH / fileName):
        logger.simpleLog("denied running daily request - data for last date " + fileName + " already exists")
        return True
    fields_to_keep = ["Name", "Id", "ShareType", "ISIN", "MarketValue", "TurnOverValueShekel", "DealsNo"
        , "BaseRate", "HighRate", "LowRate", "OpenRate", "LastRate"]
    # converts the json data from the request to file format
    csvData = file_handler.json_to_csv_string(response_JSON["Data"], fields_to_keep)

    saving_result = file_handler.save_csv_file(csvData, DAILY_PATH / fileName)
    # TO DO - add a call to the daily analysis

    return saving_result


# returns a pandas file of the daily csv file
def loadDailyFile_byDate_PD(date_format):
    # format %d-%m-%Y
    fileName = date_format + " data.csv"
    saveRes = file_handler.read_pds_csv(DAILY_PATH / fileName)
    if saveRes:
        logger.simpleLog("loaded daily file: " + fileName)
    return saveRes



def loadDailyFile_byDate_csv(date_format):
    # format %d-%m-%Y
    fileName = date_format + " data.csv"
    saveRes = file_handler.read_csv_file(DAILY_PATH / fileName)
    if saveRes:
        logger.simpleLog("loaded daily file: " + fileName)
    return saveRes



# returns a list of the daily files in the directory
def listAllDaily():
    return file_handler.allFilesInDir(DAILY_PATH)




