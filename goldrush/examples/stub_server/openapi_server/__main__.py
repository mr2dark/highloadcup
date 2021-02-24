#!/usr/bin/env python3
import logging
import os
import signal
import sys

import connexion
import flask_limiter as flim
import flask.logging as flog

from openapi_server import encoder
import openapi_server.controllers.default_controller as ctrl
from openapi_server.models.world import World

logger = logging.getLogger(__name__)
logger.addHandler(flog.default_handler)
logger.setLevel(logging.INFO)


def kill_handler(_signum, _frame):
    print(ctrl.world.get_client_report(), flush=True)
    print(ctrl.world.get_world_report(), flush=True)
    sys.exit(0)


def main():
    seed = int(os.getenv("SERVER_SEED", 0))
    rate_limit = os.getenv("DEFAULT_RATE_LIMIT", "1000 per second")
    run_time = int(os.getenv("SERVER_RUN_TIME_IN_SECONDS", 600))

    ctrl.world = World(seed)
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml', arguments={'title': 'HighLoad Cup 2021'}, pythonic_params=True)

    ctrl.limiter = flim.Limiter(app.app, default_limits=[rate_limit], key_func=lambda: 1)
    logger.info("Rate limit set to %s", rate_limit)

    signal.signal(signal.SIGALRM, kill_handler)
    signal.alarm(run_time)

    logger.info("Server will run for %d seconds", run_time)

    logger.info(ctrl.world.get_world_report())

    try:
        app.run(port=8000)
    finally:
        print(f"Final balance: {ctrl.world.balance}")


if __name__ == '__main__':
    main()
