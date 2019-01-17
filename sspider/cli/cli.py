from gevent import monkey  # isort:skip
monkey.patch_all(select=False)  # isort:skip

import sys
from functools import wraps

import click
from redis.exceptions import ConnectionError

from sspider import __version__ as version
from sspider.core.engine import Engine


def cli_decorator(code=0):
    def cli_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except ConnectionError as e:
                click.echo(e)
                sys.exit(code)
            except KeyboardInterrupt:
                click.echo()
                sys.exit(0)

        return wrapper

    return cli_wrapper


@click.group()
@click.version_option(version)
def main():
    """Sspider command line tool."""
    pass


@main.command()
@click.option('--process', '-p', is_flag=True, help='use Process not Thread')
@click.option('--num', '-n', default=1, help='Worker num')
@cli_decorator(1)
def runlocal(process, num):
    engine = Engine.from_settings()
    engine.run_local(process=process, worker_num=num)


@main.command()
@cli_decorator(2)
def runworker():
    engine = Engine.from_settings()
    engine.work()


@main.command()
@cli_decorator(3)
def runmaster():
    engine = Engine.from_settings()
    engine.schedule()


@main.command()
@click.option('--display', '-d', is_flag=True, help='展示所有爬虫调度情况')
@click.option('--spider', '-s', help='展示指定爬虫调度情况')
@click.option('--cancel', '-c', is_flag=True, help='取消指定爬虫')
def spider(display, spider, cancel):
    pass


if __name__ == '__main__':
    main()
