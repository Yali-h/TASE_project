from tase_trial.local_utils import file_handler
from pathlib import Path
import pandas as pd
from tase_trial import daily_manager
from datetime import datetime
from tase_trial.local_utils import logger
from tase_trial import historical_manager

ROOT_DIR = Path(__file__).resolve().parents[0]
SYNC_FILE = ROOT_DIR / "testing_data/Sync_data/sync_file.csv"
ALL_DAILY_PATH = ROOT_DIR / "testing_data/Sync_data"


# function that adds to the SYNC_FILE new data
# The data is given to the function which pushes it to file
def pushToSync(new_CSV, date):

    isFile = file_handler.file_exists(SYNC_FILE)
    pdFile = pd.DataFrame(
        new_CSV[1:],
        columns = new_CSV[0]
    )
    pdFile['Date'] = date

    if not isFile:
        new_data = pdFile
    else:
        syncFile = file_handler.read_pds_csv(SYNC_FILE)
        new_data = pd.concat(
            [syncFile, pdFile],
            ignore_index=True
        )

    didSave = file_handler.save_pds_csv(new_data, SYNC_FILE)
    return didSave


def mergeAlldaily():
    # start by getting all daily files by keys
    file_list = daily_manager.listAllDaily()
    AllFiles = []
    errors = []
    for fl in file_list:
        date_obj = datetime.strptime(fl.stem, "%d-%m-%Y")

        pdFile = file_handler.read_pds_csv(fl)
        if pdFile is False:
            errors.append(date_obj)
            continue

        pdFile['Date'] = date_obj
        AllFiles.append(pdFile)
    if len(errors) > 0:
        logger.simpleLog("Errors when syncing on daily files for: ")
        logger.simpleLog(errors)
    if len(AllFiles) == 0:
        return True
    allMerged = pd.concat(
        AllFiles,
        ignore_index=True
    )
    # TO DO: find current date and make better format
    nameDate = str()
    fileName = "merged_daily_" + nameDate + ".csv"
    didSave = file_handler.save_pds_csv(allMerged, ALL_DAILY_PATH / fileName)
    if didSave:
        return AllFiles
    else:
        return False



# a function that given a stock list and the path for a sync file,
# syncing the historic data wth the entries in the sync, for each stock in list
def pushUpdateToData(stockList, sync_path):
    # running the merge operation on a list of stocks
    # returns a list of stocks that were synced and a list of errors

    stock_set = set(stockList)
    syncData = file_handler.read_pds_csv(sync_path)
    if syncData is False:
        logger.simpleErr("Errors when syncing- failed finding: " + sync_path)
        return [[], stockList]

    # Vectorized filtering (FAST)
    matching = syncData[syncData["Id"].isin(stock_set)]

    grouped = matching.groupby("Id")

    errors = []
    synced = []

    for stock, stock_data in grouped:
        didWork = mergeStock(stock, stock_data)
        if didWork:
            synced.append(stock)
        else:
            errors.append(stock)

    return synced, errors



def mergeStock(stock, stock_data):
    # function for merging a data with a single stock, returns bool for result
    try:
        stock_data = formatToSync(stock_data)
    except Exception as e:
        logger.simpleSmallErr("was not able to format data. error:" + str(e))
        return False

    historic_data = historical_manager.loadHistoDataToPD(stock)
    if historic_data is False:
        logger.simpleSmallErr("Error loading historic data for stock: " + stock)
        return False
    try:
        mergedFile = pd.concat(
            [stock_data, historic_data],
            ignore_index=True
        )
        mergedFile["TradeDate"] = pd.to_datetime(
            mergedFile["TradeDate"],
            format="%d/%m/%Y",
            errors="coerce"
        )
        mergedFile = mergedFile.drop_duplicates(subset=["TradeDate"], keep="last")
        mergedFile = mergedFile.sort_values("TradeDate")
        historical_manager.savePD(stock, mergedFile)
    except Exception as e:
        # TO DO: create a better indication of what is being merged
        logger.simpleSmallErr("failed merging for " + stock+ " error:" + str(e))
        return False
    logger.simpleInfo("merged for " + str(stock))
    return True



# this function commits changes to convert from daily file format to historic. V
def formatToSync(syncData):

    # Keep only relevant columns from the first file
    syncData = syncData[
        [
            "Date",
            "BaseRate",
            "LastRate",
            "HighRate",
            "LowRate",
            "OpenRate",
            "TurnOverValueShekel"
        ]
    ].copy()

    # Rename columns to match history format
    syncData = syncData.rename(columns={
        "Date": "TradeDate",
        "TurnOverValueShekel": "TurnOver1000",
        "LastRate" : "ClosingRate"
    })

    # Reorder columns to exactly match history format
    syncData = syncData[
        [
            "TradeDate",
            "BaseRate",
            "ClosingRate",
            "HighRate",
            "LowRate",
            "OpenRate",
            "TurnOver1000"
        ]
    ]

    return syncData


