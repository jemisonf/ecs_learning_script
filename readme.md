# OSU ECS Learning Script

This is a python script that queries the OSU Locations API to figure out:
* What percentage of OSU locations are in Corvallis

Before running, install dependencies with
```bash
pip3 install -r requirements.txt
```
Which will install the `requests` library required to run the script.

To run it, you need an OSU API Key. The key should be stored in a `$AUTH_TOKEN` environment variable. If you auth token was `abcd`, you would run the script with:

```bash
AUTH_TOKEN="Bearer abcd" python3 get_data.py
```

