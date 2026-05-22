from tase_trial.tase_interactions import tase_requests
from tase_trial.local_utils import file_handler
from datetime import datetime
from tase_trial.local_utils import logger
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]



def runDailyRequest():

    current_date = datetime.now().strftime("%d-%m-%Y")
    logger.simpleLog("running daily request - today is " + current_date)

    fileName = current_date + ".csv"
    filePath = ROOT_DIR / "testing_data/daily_data/"
    if file_handler.file_exists(filePath / fileName):
        logger.simpleLog("denied running daily request - file " + fileName + " already exists")
        return True
    response_JSON = tase_requests.reqAllBonds()

    DataDate = response_JSON["Date1"].replace("/", "-")
    fileName = DataDate + ".csv"
    if file_handler.file_exists(filePath / fileName):
        logger.simpleLog("denied running daily request - data for last date " + fileName + " already exists")
        return True


    fields_to_keep = ["Name", "Id", "ShareType", "ISIN", "MarketValue", "TurnOverValueShekel", "DealsNo"
        , "BaseRate", "HighRate", "LowRate", "OpenRate"]
    csvData = file_handler.json_to_csv_string(response_JSON["Data"], fields_to_keep)

    saving_result = file_handler.save_csv_file(csvData, filePath / fileName)
    return saving_result



def loadDailyFile_byDate(date_format):
    # format %d-%m-%Y
    fileName = date_format + " data.csv"
    filePath = ROOT_DIR / "testing_data/daily_data/"
    saveRes = file_handler.read_csv_file(filePath / fileName)
    if saveRes:
        logger.simpleLog("loaded daily file: " + fileName)
    return saveRes




def getAllDailyFiles():
    filePath = ROOT_DIR / "testing_data/daily_data/"
    file_list = file_handler.allFilesInDir(filePath)
    return file_list





