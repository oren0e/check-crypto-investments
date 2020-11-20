# Get Alerts for Your Crypto Investments
## Overview
This Python script allows you to monitor the returns on your coin investments
with an alert via Telegram.

## Installation
1. Clone this repo.
2. `pip install pycoingecko`
3. Create a text file called `initial_investments` inside the `lists/` folder. Each line in this file
should contain the id of the coin you are interested to monitor followed by a single space
followed by the initial price you bought this coin for (price per 1 coin).  
If you're not sure about the `id` of your coin you can use the provided `CoinSearch` class to search
for ids or any text you want in the list of all available coins (including ids and symbols as well).  
For example, to search for the id of SNX:  
```python
from backend.data_tools import CoinSearch
cs = CoinSearch()
cs.search_for_coin('snx')
```
4. For using telegram:
    - Check out [this link](https://core.telegram.org/bots#6-botfather) and get a token.
    - Get the `chat_id` by writing something in the chat of your new bot and then 
    visit https://api.telegram.org/bot<YourBOTToken>/getUpdates and get the `chat_id` under the key
    `mesasge['chat']['id']`
    - The last step is to add 2 environment variables: TELEGRAM_API_TOKEN and TELEGRAM_CHAT_ID with the
    acquired API token and `chat_id`, respectively.

## Usage
The main purpose of this tool is for scheduling a cron-job on an always available instance (i.e., server).

## TODO
1. Make a library for easy installation
2. Add an option for a threshold only above which alerts will be sent to Telegram
3. Write more tests 