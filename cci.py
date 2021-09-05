import click

from backend.bots import CCIBot, CGroupBot

@click.command()
@click.argument("bot_name", nargs=1)
def cci(bot_name):
    if bot_name == "cci_bot":
        CCIBot().run()
    elif bot_name == "cgroup_bot":
        CGroupBot().run()
    else:
        click.echo("No such bot yet...")


if __name__ == '__main__':
    cci()
