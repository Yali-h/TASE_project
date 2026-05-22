import boto3
from datetime import date
from tase_trial.local_utils import logger

dynamodb = boto3.resource("dynamodb")
ACTIVE_STOCKS_TABLE = "stocksActive"


def table_exists(table_name):
    try:
        dynamodb.Table(table_name).load()
        return True
    except:
        return False


def create_table_active_stocks():
    if table_exists(ACTIVE_STOCKS_TABLE):
        return

    logger.simpleLog("Creating active stocks table")

    table = dynamodb.create_table(
        TableName=ACTIVE_STOCKS_TABLE,
        KeySchema=[
            {"AttributeName": "stock_id", "KeyType": "HASH"}
        ],
        AttributeDefinitions=[
            {"AttributeName": "stock_id", "AttributeType": "S"}
        ],
        BillingMode="PAY_PER_REQUEST"
    )

    table.wait_until_exists()
    logger.simpleLog("Table created successfully")


def set_new_stock_state(stock, new_state):
    table = dynamodb.Table(ACTIVE_STOCKS_TABLE)

    try:
        table.put_item(
            Item={
                "stock_id": stock,
                "state": new_state,
                "last_updated": str(date.today())
            }
        )

        logger.simpleLog(f"Updated stock={stock} state={new_state}")
        return True

    except Exception as e:
        logger.simpleLog(f"Failed update stock={stock}: {e}")
        return False



def getStockFromDB(stock_id):
    table = dynamodb.Table(ACTIVE_STOCKS_TABLE)
    try:
        response = table.get_item(
            Key={
                "stock_id": stock_id
            }
        )
    except Exception as e:
        logger.simpleLog(f"Failed to search stock in db stock {stock_id}: {e}")
        return False

    if "Item" not in response:
        return None
    return response["Item"]


def setNewState(stock_id, newState):
    table = dynamodb.Table(ACTIVE_STOCKS_TABLE)
    try:
        table.update_item(
            Key={"stock_id": stock_id},
            UpdateExpression="SET #s = :val",
            ExpressionAttributeNames={
                "#s": "state"
            },
            ExpressionAttributeValues={
                ":val": newState
            }
        )
        return True
    except Exception as e:
        logger.simpleLog(f"Failed to set new state to stock {stock_id}: {e}")
        return False




def getAllItems():
    table = dynamodb.Table(ACTIVE_STOCKS_TABLE)
    try:
        response = table.scan()
    except Exception as e:
        logger.simpleLog(f"Failed to scan db {ACTIVE_STOCKS_TABLE}: {e}")
        return None
    return response["Items"]




#setNewState("00662577", False)
#print(getAllItems())
#setNewState("00662577", True)
#print(getStockFromDB("00662577"))
#print("we won")


