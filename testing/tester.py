
from tase_trial import historical_manager
from tase_trial import daily_manager


def test_HistoricalData():
    #historical_data.getHistoData(str(662577), "1990-05-09", "2027-05-09")
    return historical_manager.loadHistoData(662577)

def test_dailyManager():
    #didSave = daily_manager.runDailyRequest()
    fList = daily_manager.getAllDailyFiles()
    return fList


stockHistory = test_dailyManager()
print(stockHistory)

