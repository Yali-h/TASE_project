
# a file containing the needed payloads for requests



# payload for a daily data requests
def AllBondsPayload():
    payload = {
        "FilterData": {
            "dType": 1,
            "TotalRec": 1,
            "pageNum": 1,
            "cl1": "0",
            "lang": "0"
        },
        "isAdd": False
    }
    return payload



# payload for a history request in a certain time frame
def TimeRangePayload(stock_id, stDate_formatted, enDate_formatted):
    payload = { "FilterData": {
        "lang": 0,
        "ct": 1,
        "ot": 1,
        "oid": stock_id,
        "cp": 8,
        "cv": 0,
        "cl": 0,
        "dFrom": stDate_formatted,
        # start date
        "dTo": enDate_formatted,
        # end date
        "objName": ""
    }}
    return payload