

from tase_interactions import tase_requests
from local_utils import file_handler
from datetime import datetime
from local_utils import logger


# A function that converts an object data into a csv string


def runDailyRequest():

    current_date = datetime.now().strftime("%d-%m-%Y")
    logger.simpleLog("running daily request - today is " + current_date)

    fileName = current_date + ".csv"
    filePath = "testing_data/daily_data/"
    if file_handler.file_exists(filePath, fileName):
        logger.simpleLog("denied running daily request - file " + fileName + " already exists")
        return True
    response_JSON = tase_requests.reqAllBonds()

    DataDate = response_JSON["Date1"].replace("/", "-")
    fileName = DataDate + ".csv"
    if file_handler.file_exists(filePath, fileName):
        logger.simpleLog("denied running daily request - data for last date " + fileName + " already exists")
        return True


    fields_to_keep = ["Name", "Id", "ShareType", "ISIN", "MarketValue", "TurnOverValueShekel", "DealsNo"
        , "BaseRate", "HighRate", "LowRate", "OpenRate"]
    csvData = file_handler.json_to_csv_string(response_JSON["Data"], fields_to_keep)

    file_handler.save_csv_file(csvData, filePath + fileName)



def mergeToMonthlyRequest(CSV_data, date):
    pass



runDailyRequest()


