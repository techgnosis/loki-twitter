import requests
import os
import json
import sys
import time
from datetime import datetime
from datetime import timezone
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

twitter_bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
loki_url = os.environ.get("LOKI_URL")

if not twitter_bearer_token or not loki_url:
    print("Both TWITTER_BEARER_TOKEN and LOKI_URL are required environment variables")
    print("LOKI_URL requires scheme and path. The default Loki path is /loki/api/v1/push")
    sys.exit(1)

loki_username = os.environ.get("LOKI_USERNAME")
loki_password = os.environ.get("LOKI_PASSWORD")

if loki_username and loki_password:
    print("LOKI_USERNAME and LOKI_PASSWORD are defined. Assuming Grafana Cloud Logs or GEL")


def connect_to_twitter():
    url = "https://api.twitter.com/2/tweets/sample/stream?tweet.fields=created_at,lang"
    headers = {}
    headers["Authorization"] = f"Bearer {twitter_bearer_token}"
    headers['Content-Type'] = 'application/json'
    response = requests.request("GET", url, headers=headers, stream=True)
    print(f"Connection to Twitter API received {response.status_code} in return.")
    if response.status_code != 200:
        raise Exception(
            f"Connection to Twitter API returned an error: {response.status_code} {response.text}"
        )
        
    
    # this will loop forever since we're streaming with a websocket via stream=True in the request
    print("Starting tweet streaming. Updates printed to screen every 10 tweets")
    tweets = 0
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            if json_response['data']['lang'] == 'en':
                if push_to_loki(json_response):
                    time.sleep(1.3)
                    tweets += 1
                    if tweets % 10 == 0:
                        print(f"Ingested {tweets} tweets")
    

def push_to_loki(json_response):
    # figure out timestamp for Loki
    created_at = json_response['data']['created_at']
    datetime_object = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S.000Z')
    timestamp = datetime_object.replace(tzinfo=timezone.utc).timestamp()
    timestamp_nanoseconds = int(timestamp * 1000000000)
    
    
    tweet = json_response['data']['text']
    
    submission = [str(timestamp_nanoseconds), tweet]

    loki_request = {}
    loki_request["streams"] = []

    static_labels = {
        "source": "twitter"
    }

    values = []
    values.append(submission)
    
    internal_dict = {
        "stream": static_labels,
        "values": values
    }

    loki_request["streams"].append(internal_dict)
    
    if loki_username and loki_password:
        headers = {'Content-Type': 'application/json'}
        response = requests.request(
            "POST",
            loki_url,
            data=json.dumps(loki_request),
            verify=False,
            headers=headers,
            auth=(loki_username, loki_password)
        )
    else:
        headers = {'X-Scope-OrgID': 'fake', 'Content-Type': 'application/json'}
        response = requests.request(
            "POST",
            loki_url,
            data=json.dumps(loki_request),
            verify=False,
            headers=headers
        )

    if response.status_code != 204:
        print("Request to Loki did not get a 204 in return")
        print(f"Response code was {response.status_code}")

    return True


if __name__ == "__main__":
    connect_to_twitter()