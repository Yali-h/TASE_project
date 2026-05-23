from tase_trial.local_utils import file_handler
from pathlib import Path
import pandas as pd
from tase_trial import daily_manager
from datetime import datetime
from tase_trial.local_utils import logger
from tase_trial import historical_manager

ROOT_DIR = Path(__file__).resolve().parents[0]


# function that has
def pushToSync(new_CSV, date):
    sync_Name = ROOT_DIR / "testing_data/Sync_data/sync_file.csv"
    isFile = file_handler.file_exists(sync_Name)
    # error not pandas
    pdFile = pd.DataFrame(
        new_CSV[1:],
        columns = new_CSV[0]
    )
    pdFile['Date'] = date
    if not isFile:
        new_data = pdFile
    else:
        syncFile = file_handler.read_pds_csv(sync_Name)
        new_data = pd.concat(
            [syncFile, pdFile],
            ignore_index=True
        )

    file_handler.save_pds_csv(new_data, sync_Name)
    return True


def mergeAlldaily():
    # start by getting all daily files by keys
    file_list = daily_manager.FindAllDaily()
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
    filePath = ROOT_DIR / "testing_data/Sync_data/allDailyData.csv"
    didSave = file_handler.save_pds_csv(allMerged, filePath)
    return didSave




def pushUpdateToData(stockList, sync_path):
    stock_set = set(stockList)

    syncData = file_handler.read_pds_csv(sync_path)
    if syncData is False:
        logger.simpleLog("Errors when syncing: failed finding: " + sync_path)
    # Vectorized filtering (FAST)
    matching = syncData[syncData["Id"].isin(stock_set)]

    # Group by sid
    grouped = matching.groupby("Id")

    for stock, stock_data in grouped:
        didWork = mergeStock(stock, stock_data)

    return True



def mergeStock(stock, stock_data):
    stock_data = formatToSync(stock_data)
    historic_data = historical_manager.loadHistoDataToPD(stock)
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
        logger.simpleLog("failed merging for " + stock+ "error:" + str(e))
        return False
    logger.simpleLog("merged for " + str(stock))
    return True



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


