This repo accompanies the blog post [Low cost Twitter analysis with Loki](https://blog.grafana.com/)

This repo contains all the code needed to stream tweets into either Loki, GEL, or Grafana Cloud Logs. This repo does not include any code for deploying Loki or GEL. Loki is very easy to run on your laptop but you can also sign up for a [free Grafana Cloud account](https://grafana.com).

GEL stands for Grafana Enterprise Logs. GEL is the paid version of Loki with many features that large companies use, such as out-of-the-box authn/authz and a GUI for speed of initial onboarding.

# Scripts
Use `stream.py` to stream Tweets into either Loki, GEL, or Grafana Cloud Logs. `stream.py` relies on environment variables which are defined at the beginning of the script and explained below.

Use `test-loki.sh` or `test-cloud-or-gel.sh` to insert the data from `test-data.json` into either Loki or GEL. Both scripts use the same environment variables as `stream.py`.

Use `time_in_ns.sh` to get current timestamps for insertion into `test-data.json` so you can find them in Loki or GEL without setting a huge time range. The timestamps that are in `test-data.json` as you read this are dated far back in the past.

# Requirements to run the code
Docker, or you can use your own Python environment if that's in your skillset

# How to run
1. Run `open-docker-env.sh` to create an interactive bash shell in the latest `python:3` container image
1. Run `pip install requests`. The "requests" library is the only dependency that's not in the Python 3 standard library
1. Export the following environment variables:
    * `TWITTER_BEARER_TOKEN`
    * `LOKI_URL`
    * `LOKI_USERNAME` (if required)
    * `LOKI_PASSWORD` (if required)
1. Run `python3 stream.py`

# Paths
For Loki and GEL, the URL path needs to be `/loki/api/v1/push`. If you are using Grafana Cloud Logs, there will be no path.

# Other notes
* The code that streams Tweets from the Twitter API filters out tweets that are not in English. The filtering occurs on line 45
* There is a 1.3s wait between each Tweet. The wait occurs on line 47. The author's Twitter account has a limit of 2 million tweets a month and 1.3s gives me exactly 2m tweets if the script ran for a whole month.