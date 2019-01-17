from gevent import monkey  # isort:skip
monkey.patch_all(select=False)  # isort:skip

import click

from sspider import __version__ as version
from sspider.core.engine import Engine


@click.group()
@click.version_option(version)
def main():
    """Sspider command line tool."""
    pass


@main.command()
@click.option('--process', '-p', is_flag=True, help='use Process not Thread')
@click.option('--num', '-n', default=1, help='Worker num')
def runlocal(process, num):
    engine = Engine.from_settings()
    engine.run_local(process=process, worker_num=num)


@main.command()
def runworker():
    engine = Engine.from_settings()
    engine.work()


@main.command()
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
