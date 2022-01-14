This repo accompanies the blog post [Low cost Twitter analysis with Loki](https://blog.grafana.com/)

This repo contains all the code needed to stream tweets into either Loki, GEL, or Grafana Cloud Logs. This repo does not include any code for deploying Loki or GEL. Loki is very easy to run on your laptop but you can also sign up for a [free Grafana Cloud account](https://grafana.com).

GEL stands for Grafana Enterprise Logs. GEL is the paid version of Loki with many features that large companies use, such as out-of-the-box authn/authz and a GUI for speed of initial onboarding.

# Scripts
Use `time_in_ns.sh` to get current timestamps for insertion into `test-data.json` so you can find them in Loki or GEL without setting a huge time range. The timestamps that are in there as you read this are probably old.

Use `test-loki.sh` or `test-gel.sh` to insert the data from `test-data.json` into either Loki or GEL.

Use `stream.py` to stream Tweets into either Loki, GEL, or Grafana Cloud Logs. `stream.py` relies on environment variables which are defined at the beginning of the script and explained below.


# How to run
1. Run `open-docker-env.sh` to create an interactive bash shell in the latest `python:3` container image
1. Run `pip install requests`. The "requests" library is the only dependency that's not in the standard library
1. Run `export LOKI_URL="your Loki URL here"`
1. Run `export TWITTER_BEARER_TOKEN="your Twitter API bearer token here"`
1. If you are using GEL or Grafana Cloud Logs, run `export LOKI_USERNAME="your username here"`
1. If you are using GEL or Grafana Cloud Logs, run `export LOKI_PASSWORD="your password here"`
1. Run either `python3 stream.py`

# Paths
For Loki and GEL, the URL path needs to be `/loki/api/v1/push`. If you are using Grafana Cloud Logs, there will be no path.

# Other notes
* The code that streams Tweets from the Twitter API filters out tweets that are not in English on line 50
* There is a 100ms wait between each Tweet on line 52 since the API has a tweet limit