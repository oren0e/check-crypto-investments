from backend.data_tools import DataHandler

import click


@click.command()
@click.option('-r', '--remote', is_flag=True, default=False, help="Get initial investments info from S3")
def cci(remote: bool = False) -> None:
    if remote:
        click.echo("Getting base prices from S3...")
        dh = DataHandler(remote_initial=True)
    else:
        dh = DataHandler()
    dh.send_msg()


if __name__ == '__main__':
    cci()

