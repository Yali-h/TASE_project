
from tase_trial.tase_interactions import tase_requests
from tase_trial.local_utils import file_handler
import time
from tase_trial.local_utils import logger
from pathlib import Path
import pandas as pd


# Project root
ROOT_DIR = Path(__file__).resolve().parents[0]


def getHistoData(stock_id, stDate, enDate):
    stDate_formatted = stDate + "T00:00:00.000Z"
    enDate_formatted = enDate + "T00:00:00.000Z"

    JsonResponse = tase_requests.reqHistoData(str(stock_id), stDate_formatted, enDate_formatted)
    if not JsonResponse:
        time.sleep(10)
        JsonResponse = tase_requests.reqHistoData(str(stock_id), stDate_formatted, enDate_formatted)
        if not JsonResponse:
            logger.simpleLog("unable to get data inside getHistoData: ")
            logger.simpleLog("stock " + str(stock_id) + "track from " + str(stDate_formatted) +  " until " + str(enDate_formatted))
            return False

    #print(JsonResponse)

    fields_to_keep = ['TradeDate', 'BaseRate', 'ClosingRate', 'HighRate', 'LowRate', 'OpenRate', 'TurnOver1000']
    csvData = file_handler.jsonToCSV(JsonResponse["Data"], fields_to_keep)
    fileName = str(stock_id) + " data.csv"
    filePath = ROOT_DIR / "testing_data/historic_data/"

    csvData["TradeDate"] = pd.to_datetime(
        csvData["TradeDate"],
        format="%d/%m/%Y",
        errors="coerce"
    )

    saveRes = file_handler.save_pds_csv(csvData, filePath / fileName)

    return saveRes




def loadHistoDataToPD(stock_id):
    fileName = str(stock_id) + " data.csv"
    filePath = ROOT_DIR / "testing_data/historic_data/"
    saveRes = file_handler.read_pds_csv(filePath / fileName)
    if not saveRes is False:
        logger.simpleLog("loaded history file: " + fileName)
    return saveRes


def savePD(stock_id, stockData):
    fileName = str(stock_id) + " data.csv"
    filePath = ROOT_DIR / "testing_data/historic_data/"
    saveRes = file_handler.save_pds_csv(stockData, filePath / fileName)
    if saveRes:
        logger.simpleLog("saved new history file: " + fileName)
    return saveRes


