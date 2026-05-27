
  
# The aws_interactions directory:  
  
The directory has all the applications that interact with AWS.  
In this way we can separate the files needed for local development   
against those required for enabling and working with the cloud  
  
  
It contains 2 files:  
  
## activeStocks_dynamo:
Contains all the calls needed for a dynamo DB, we will use this db  
in order to manage a list of stocks relevant to our project.  
We will also add functionality to save simple values in here, like certain  
data on the stock that we might want to receive quickly.  
The use of dynamoDB instead of S3 lets has save small objects without  
the cost coming from S3.   
  
### abilities:

**table_exists(table_name)**: str -> bool 
checks dynamoDB for a table name table_name. return True of False - for errors sends to the logger and raises the error.

**create_table_active_stocks()**: None -> bool 
makes sure the active stocks table was created.