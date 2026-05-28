
from tase_trial.tase_interactions import tase_requests
from tase_trial.local_utils import file_handler
import time
from tase_trial.local_utils import logger
from pathlib import Path
import pandas as pd


# Project root
ROOT_DIR = Path(__file__).resolve().parents[0]
HISTO_PREFIX = ROOT_DIR / "testing_data/historic_data/"
HISTO_SUFFIX = " data.csv"



def getHistoData(stock_id, stDate, enDate):
    stDate_formatted = stDate + "T00:00:00.000Z"
    enDate_formatted = enDate + "T00:00:00.000Z"

    JsonResponse = tase_requests.reqHistoData(str(stock_id), stDate_formatted, enDate_formatted)
    if not JsonResponse:
        time.sleep(10)
        JsonResponse = tase_requests.reqHistoData(str(stock_id), stDate_formatted, enDate_formatted)
        if not JsonResponse:
            logger.simpleLog("unable to get data inside getHistoData for request: ")
            logger.simpleLog("stock " + str(stock_id) + " track from " + str(stDate_formatted) +  " until " + str(enDate_formatted))
            return False

    #print(JsonResponse)

    fields_to_keep = ['TradeDate', 'BaseRate', 'ClosingRate', 'HighRate', 'LowRate', 'OpenRate', 'TurnOver1000']
    csvData = file_handler.jsonToCSV(JsonResponse["Data"], fields_to_keep)
    fileName = str(stock_id) + HISTO_SUFFIX

    csvData["TradeDate"] = pd.to_datetime(
        csvData["TradeDate"],
        format="%d/%m/%Y",
        errors="coerce"
    )

    saveRes = file_handler.save_pds_csv(csvData, HISTO_PREFIX / fileName)

    return saveRes


# TO DO - create a version with moving date
def getAllHistoData(stock_id):
    return getHistoData(stock_id, "1990-05-09", "2027-05-09")


def getBatchHisto(stocks):
    correct = []
    errors = []
    for stock in stocks:
        # wait a few seconds between requests

        didPass = getAllHistoData(stock)
        if didPass:
            correct.append(stock)
        else:
            errors.append(stock)
        if stock != stocks[-1]:
            time.sleep((stock % 9) + 5)


    return correct, errors


# loading an history file to PD
def loadHistoDataToPD(stock_id):
    fileName = str(stock_id) + HISTO_SUFFIX
    saveRes = file_handler.read_pds_csv(HISTO_PREFIX / fileName)
    if not saveRes is False:
        logger.simpleLog("loaded history file: " + fileName)
    return saveRes



def savePD(stock_id, stockData):
    fileName = str(stock_id) + HISTO_SUFFIX
    saveRes = file_handler.save_pds_csv(stockData, HISTO_PREFIX / fileName)
    if saveRes:
        logger.simpleLog("saved new history file: " + fileName)
    return saveRes


