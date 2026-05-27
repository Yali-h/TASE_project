
from tase_trial.local_utils import file_handler
from tase_trial import historical_manager
from tase_trial import daily_manager
from tase_trial import Sync_manager
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


def test_HistoricalData():

    historical_manager.getHistoData(662577, "1990-05-09", "2027-05-09")

    #return historical_manager.loadHistoDataToPD(662577)


def test_dailyManager():
    didSave = daily_manager.runDailyRequest()
    #fList = daily_manager.getAllDailyFiles()
    return didSave


def test_syncManager():
    Sync_manager.mergeAlldaily()
    #Data = file_handler.read_csv_file(ROOT_DIR / "testing_data/daily_data/20-05-2026.csv")
    #print(Data)
    #Sync_manager.pushToSync(Data, "20-05-2026")
    #ROOT_DIR / "testing_data/daily_data/20-05-2026.csv"
    Sync_manager.pushUpdateToData([662577], ROOT_DIR / "testing_data/Sync_data/allDailyData.csv")



test_HistoricalData()
#test_dailyManager()
#test_syncManager()