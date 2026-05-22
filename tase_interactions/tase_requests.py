
import requests
from tase_trial.tase_interactions import payloads
from tase_trial.local_utils import logger


# requesting all the data from an historic point for a certain stock
def reqHistoData(stock_id, stDate_formatted, enDate_formatted):
    url = "https://api.tase.co.il/api/exportchart/chartdata"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Origin": "https://www.tase.co.il",
        "Referer": "https://www.tase.co.il/"
    }

    payload = payloads.TimeRangePayload(stock_id, stDate_formatted, enDate_formatted)

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload
        )
    except Exception as e:
        logger.simpleLog("request was unable to be sent, nothing was stored -" + str(e))
        return False


    if response.status_code == 200:
        logger.simpleLog("request passed for stock " + stock_id + " storing data")
        return response.json()

    else:
        logger.simpleLog("an error occurred while sending request for stock " + stock_id)
        logger.simpleLog("got status code: " + str(response.status_code) + " no changes were made")
        return False



# requesting all the daily data
def reqAllBonds():
    url = "https://api.tase.co.il/api/export/securitiesmarketdata"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://www.tase.co.il",
        "Referer": "https://www.tase.co.il/",
        "User-Agent": "Mozilla/5.0"
    }

    payload = payloads.AllBondsPayload()


    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )
    except Exception as e:
        logger.simpleLog("request was unable to be sent, nothing was "
                         "stored - " + str(e))
        return False


    if response.status_code == 200:
        logger.simpleLog("request passed for getting all bonds")
        return response.json()

    else:
        logger.simpleLog("an error occurred while sending request to get all bonds")
        logger.simpleLog("got status code: " + str(response.status_code) + " no changes were made")
        return False



