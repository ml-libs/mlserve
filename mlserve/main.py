import asyncio
import argparse
import logging
from typing import Any

from aiohttp import web
from .utils import load_model_config, init


def _cli_parser() -> Any:
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Provide path to config file')
    parser.add_argument(
        '-H', '--host', help='Port for WEB/API', default='127.0.0.1'
    )
    parser.add_argument('-P', '--port', help='Port for WEB/API', default=9000)
    parser.add_argument('-w', '--workers', help='Number of workers', default=2)
    args = parser.parse_args()
    return args


def main() -> None:
    args = _cli_parser()
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    model_conf = load_model_config(args.config)
    app = loop.run_until_complete(init(args.workers, model_conf))
    web.run_app(app, host=args.host, port=args.port)
