import requests
import os
import json
from datetime import datetime
from datetime import timezone
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

twitter_bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
gel_tenant = os.environ.get("GEL_TENANT")
gel_token = os.environ.get("GEL_TOKEN")
gel_host = os.environ.get("GEL_HOST")

def create_url():
    return "https://api.twitter.com/2/tweets/sample/stream?tweet.fields=created_at,lang"


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {twitter_bearer_token}"
    r.headers["User-Agent"] = "v2SampledStreamPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth, stream=True)
    print(f"Connection to Twitter API received {response.status_code} in return.")
    if response.status_code != 200:
        raise Exception(
            f"Request returned an error: {response.status_code} {response.text}"
        )
        
    
    # this will loop forever since we're streaming with a websocket
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            if json_response['data']['lang'] == 'en':
                push_to_loki(json_response)
    

def push_to_loki(json_response):
    loki_url = f"https://{gel_host}/loki/api/v1/push"

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
    headers = {'Content-Type': 'application/json'}
    response = requests.request(
        "POST",
        loki_url,
        data=json.dumps(loki_request),
        verify=False,
        headers=headers,
        auth=(gel_tenant, gel_token)
    )

    if response.status_code != 204:
        print("Request to Loki did not get a 204 in return")
        print(response.text)


def main():
    url = create_url()
    timeout = 0
    while True:
        connect_to_endpoint(url)
        timeout += 1


if __name__ == "__main__":
    main()