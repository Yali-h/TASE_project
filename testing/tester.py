
import tase_requests



response_json = tase_requests.reqAllBonds()
print(response_json)

data_json = response_json.get("data", [])
print(data_json)


