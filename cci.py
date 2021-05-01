import os
import click

from backend.data_tools import PriceHandler, DataReader, DataDisplayer
from utils.telegram import Bot, Chat, BotPool, telegram_send


@click.command()
@click.option('-s', '--source', default="local", help="Specify the source of the initial investments data: local or remote")
@click.option('--only-gas', is_flag=True, default=False, help="Get only gas price estimate")
def cci(source: str = "local", only_gas: bool = False) -> None:
    main(source, only_gas)


def main(source: str = "local", only_gas: bool = False) -> None:
    bot_pool = BotPool()
    bot_pool.add_bot(Bot(name="cci_bot", api_token=os.environ.get('TELEGRAM_API_TOKEN'),
                         chats={"cci_chat": Chat("cci_chat", chat_id=os.environ.get('TELEGRAM_CHAT_ID'))}))
    bot_pool.add_bot(Bot(name="cgroup_bot", api_token=os.environ.get("TELEGRAM_CGROUP_TOKEN"),
                         chats={"cgroup_chat": Chat("cgroup_chat", chat_id=os.environ.get("TELEGRAM_CGROUP_CHAT_ID"))}))
    data_reader = DataReader()
    gas_msg = DataDisplayer().display_eth_gas(data_reader.get_gas_estimate())
    if only_gas:
        telegram_send(bot_pool.pool["cgroup_bot"], "cgroup_chat", gas_msg)
    else:
        initial_investments = data_reader.get_initial_investments_from_source("initial_investments", source)
        returns = PriceHandler(initial_investments).get_prices().calculate_returns()
        output_msg = DataDisplayer.display_returns(returns) + gas_msg
        telegram_send(bot_pool.pool["cci_bot"], "cci_chat", output_msg)


if __name__ == '__main__':
    cci()

