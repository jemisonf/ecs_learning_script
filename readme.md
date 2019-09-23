# OSU ECS Learning Script

This is a python script that queries the OSU Locations API to:
* Filter location data based on parking zone groups, presence of gender inclusive restrooms, building ID, campus, and generic query string

## Prerequisites

Before running, install dependencies with
```bash
pip3 install -r requirements.txt
```
Which will install the `requests` library required to run the script.

You should also create a config file with your credentials. The default config file name is `config.ini` but you can pass in a different name with the `--config` flag.

If you had an app with id `abcd` and secret `efghi` your config file would look like:

```ini
[credentials]
client_id = abcd
client_secret = efghi
```

## Running the program

With your config file set up, you can run the program with:

```bash
python3 get_data.py
```

To view options for filtering, use the `-h` or `--help` flag.
