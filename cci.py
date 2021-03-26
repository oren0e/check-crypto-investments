from backend.data_tools import DataHandler, CGroupHandler

import click


@click.group()
def check():
    pass


@check.command()
@click.option('-r', '--remote', is_flag=True, default=False, help="Get initial investments info from S3")
def cci(remote: bool = False) -> None:
    if remote:
        click.echo("Getting base prices from S3...")
        dh = DataHandler(remote_initial=True)
    else:
        dh = DataHandler()
    dh.send_msg()


@check.command()
def cgroup() -> None:
    CGroupHandler().send_msg()


if __name__ == '__main__':
    check()

