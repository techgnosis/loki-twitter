GEL stands for Grafana Enterprise Logs. GEL is the paid version of Loki with many features that large companies use, such as out-of-the-box authn/authz and a GUI for speed of initial onboarding.


Use `time_in_ns.sh` to get current timestamps for `test-data.json` so you can find them in Loki or GEL without setting a huge time range. The timestamps that are in there as you read this could be extremely old.

Use `test-loki.sh` or `test-gel.sh` to insert the data from `test-data.json` into either Loki or GEL.

Use `stream-to-loki.py` or `stream-to-gel.py` to stream Tweets into either Loki or GEL. Both scripts rely on environment variables which are defined at the beginning of the scripts.


# How to run
1. Run `open-docker-env.sh` to create an interactive bash shell in the latest `python:3` container image
2. Run `pip install requests`. The "requests" library is the only dependency that's not in the standard library
3. Export your required environment variables
4. Run either `python3 stream-to-loki.py` or `python3 stream-to-gel.py`