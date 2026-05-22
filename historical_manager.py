
from tase_trial.tase_interactions import tase_requests
from tase_trial.local_utils import file_handler
import time
from tase_trial.local_utils import logger
from pathlib import Path

# Project root
ROOT_DIR = Path(__file__).resolve().parents[0]


def getHistoData(stock_id, stDate, enDate):
    stDate_formatted = stDate + "T00:00:00.000Z"
    enDate_formatted = enDate + "T00:00:00.000Z"

    JsonResponse = tase_requests.reqHistoData(stock_id, stDate_formatted, enDate_formatted)
    if not JsonResponse:
        time.sleep(10)
        JsonResponse = tase_requests.reqHistoData(stock_id, stDate_formatted, enDate_formatted)
        if not JsonResponse:
            logger.simpleLog("unable to get data inside getHistoData: ")
            logger.simpleLog("stock " + str(stock_id) + "track from " + str(stDate_formatted) +  " until " + str(enDate_formatted))
            return False

    # got a valid JSON response, store in file
    print(JsonResponse["Data"][1].keys())
    print(JsonResponse["Data"][1])
    print(JsonResponse.keys())
    #print(JsonResponse)

    fields_to_keep = ['TradeDate', 'BaseRate', 'ClosingRate', 'HighRate', 'LowRate', 'OpenRate', 'TurnOver1000', 'DollarAdjustmentRate']
    csvData = file_handler.json_to_csv_string(JsonResponse["Data"], fields_to_keep)

    fileName = stock_id + " data.csv"
    filePath = ROOT_DIR / "testing_data/historic_data/"

    saveRes = file_handler.save_csv_file(csvData, filePath / fileName)

    return saveRes






def loadHistoData(stock_id):
    fileName = str(stock_id) + " data.csv"
    filePath = ROOT_DIR / "testing_data/historic_data/"
    saveRes = file_handler.read_csv_file(filePath / fileName)
    if saveRes:
        logger.simpleLog("loaded history file: " + fileName)
    return saveRes




