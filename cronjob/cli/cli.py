from gevent import monkey  # isort:skip
monkey.patch_all(select=False)  # isort:skip

import sys
from functools import wraps

import click
from redis.exceptions import ConnectionError

from cronjob import __version__ as version
from cronjob.core.engine import Engine
from cronjob.settings import settings


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
    """cronjob command line tool."""
    pass


@main.command()
@click.option(
    '--mode', '-m', default='thread', help="distributed, thread or process.")
@click.option('--node', help="If distributed mode, run master or worker.")
@click.option('--num', '-n', default=1, help="The number of workers.")
def run(mode, node, num):
    if mode == 'distributed':
        if node is None:
            raise ValueError("If distributed mode, run master or worker.")
        click.echo('Use distributed mode.')
        run_with_distributed(node)
    elif mode in ['thread', 'process']:
        click.echo(f'user {mode} mode.')
        run_with_local(mode, num)
    else:
        raise ValueError(
            'mode error, must use distributed, thread or process.')


def run_with_distributed(node):
    assert settings.QUEUE_CONFIG['queue_type'] in {'redis'}, (
        'In distributed mode, can not use thread and process,'
        'please change QUEUE_CONFIG in settings file')
    engine = Engine.from_settings()
    if node == 'master':
        engine.schedule()
    elif node == 'worker':
        engine = Engine.from_settings()
        engine.work()


def run_with_local(mode, num):
    msg = (f'Cli command option --mode=={mode} cat not match settings '
            'file, please change QUEUE_CONFIG in settings file.')
    if mode == 'process':
        assert settings.QUEUE_CONFIG['queue_type'] == 'process', msg
        engine = Engine.from_settings()
        engine.run_local(process=True, worker_num=num)
    elif mode == 'thread':
        assert settings.QUEUE_CONFIG['queue_type'] == 'thread', msg
        engine = Engine.from_settings()
        engine.run_local(worker_num=num)
    else:
        raise 'In local mode, can only use thread or process option.'


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
@click.option('--job', '-s', help='展示指定爬虫调度情况')
@click.option('--cancel', '-c', is_flag=True, help='取消指定爬虫')
def job(display, job, cancel):
    pass


if __name__ == '__main__':
    main()
