![example workflow name](https://github.com/oren0e/check-crypto-investments/workflows/CI/badge.svg)

# Get Alerts for Your Crypto Investments

## Overview

Allows you to monitor the returns on your coin investments
with an alerts via Telegram. Further alert senders can be implemented as well.

## Installation

**Note**: Currently this tool is only available for Mac or Linux users.

1.  Clone this repo.
2.  `pip install pycoingecko`
3.  `pip install etherscan-python` (Go to https://etherscan.io/, sign up and get your API key).
4.  Create a environment variable called `INITIAL_INVESTMENTS`. Each line in this variable
    should contain the id of the coin you are interested to monitor followed by a single space
    followed by the initial price you bought this coin for (price per 1 coin).

        - If you're not sure about the `id` of your coin you should check at coingecko's API - i.e.:
        ```

    curl -X 'GET' 'https://api.coingecko.com/api/v3/coins/list' -H 'accept: application/json'

    ```

    ```

5.  For using telegram:
    - Check out [this link](https://core.telegram.org/bots#6-botfather) and get a token.
    - Get the `chat_id` by writing something in the chat of your new bot and then
      visit `https://api.telegram.org/bot<YourBOTToken>/getUpdates` and get the `chat_id` under the key
      `mesasge['chat']['id']`
    - Add a configuration environment variable with a `yml` structure, you can see an example in the
      `tests/data/correct_config.yml` file. You need to add the bot you implemented with the abstract methods
      in the `backend/interfaces` folder and it's corresponding API key and chat ID of the Telegram chat you want
      the messages to be sent to.

## Usage

The main purpose of this tool is for scheduling a cron-job on an always available instance (i.e., server).
The usage is simple: `python cci.py <BOT NAME>`.

## TODO

2. Make a library for easy installation
3. Add an option for a threshold only above which alerts will be sent to Telegram
4. Write more tests
5. Make available for Windows users as well
6. Use poetry for requirements
