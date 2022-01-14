GEL stands for Grafana Enterprise Logs. GEL is the paid version of Loki with many features that large companies use, such as out-of-the-box authn/authz and a GUI for speed of initial onboarding.


Use `time_in_ns.sh` to get current timestamps for `test-data.json` so you can find them in Loki without setting a huge time range. The timestamps that are in there could be extremely old.

Use `test-loki.sh` and `test-gel.sh` to insert the data from `test-data.json` into either Loki or GEL.