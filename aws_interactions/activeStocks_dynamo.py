import boto3
from datetime import date
from tase_trial.local_utils import logger
from botocore.exceptions import ClientError, EndpointConnectionError, NoCredentialsError


dynamodb = boto3.resource("dynamodb")
ACTIVE_STOCKS_TABLE = "stocksActive"


# checking if some table exists
def table_exists(table_name):
    # trying to access dynamodb to check if a certain table exists
    try:
        dynamodb.Table(table_name).load()
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            # table not found
            return False
        # other error while calling
        logger.simpleLog(f"Failed interaction with dynamodb {table_name}: {e}")
        raise
    except (NoCredentialsError,EndpointConnectionError)  as e:
        # some aws connection issue
        logger.simpleLog(f"Failed to connect to dynamodb table {table_name}: {e}")
        raise



# making sure the ACTIVE_STOCKS_TABLE is created
def create_table_active_stocks():
    if table_exists(ACTIVE_STOCKS_TABLE):
        return True

    logger.simpleLog("Creating active stocks table")

    try:
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
    except Exception as e:
        logger.simpleLog(f"Error while trying to create stocks table: {e}")
        return False

    logger.simpleLog("Table created successfully")
    return True


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
            Key={"stock_id": str(stock_id)},
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


# TO DO - correct error handling, checking why scan failed
# gets all the items in ACTIVE_STOCKS_TABLE

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
#setNewState(662577, True)
#print(getStockFromDB("00662577"))
#print("we won")


