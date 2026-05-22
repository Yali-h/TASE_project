from tase_trial.local_utils import file_handler
from tase_trial.aws_interactions import activeStocks_dynamo
from tase_trial.tase_interactions import tase_requests


def sync_Delta():
    stockList = activeStocks_dynamo.getActiveStocks()
    pass

def merge_Alldaily():
    # start by getting all daily files by keys

    # continue by going over each daily file, scanning him and adding to a list




    # at the end go over all files that were merged and delete them

    pass



def mergeCsvFiles(keys):
    pass







