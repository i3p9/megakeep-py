# MegaKeep-py

MegaKeep-py is a Python script that uses the MEGA CLI to check the usage of Mega accounts.

## Requirements

- Python 3.x
- MEGA CLI (download from https://mega.io/cmd)

## Usage

In the `keep.py` file, you can change the `txt_file_path` variable to the path of the accounts file to a text file that contains the accounts to be checked. Then run the script.

```bash
python keep.py
```

## Accounts file

The accounts.txt file is a text file that contains the accounts to be checked.

```
user@domain.com:password
```

## Logs

The logs are saved in the logs folder.

## Caveats

- Depending on your network/mega restirctions, you might get rate limited and may need to run the script multiple times or wait for the rate limit to reset.
