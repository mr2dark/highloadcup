#!/usr/bin/env python3
import os
import signal
import sys

import connexion
import flask_limiter as flim

from swagger_server import encoder
import swagger_server.controllers.default_controller as ctrl
from swagger_server.models.world import World


def kill_handler(_signum, _frame):
    print(f"Final balance: {ctrl.world.balance}", flush=True)
    sys.exit(0)


def main():
    seed = 0
    rate_limit = os.getenv("DEFAULT_RATE_LIMIT", "1000 per second")
    run_time = int(os.getenv("SERVER_RUN_TIME_IN_SECONDS", 600))

    ctrl.world = World(seed)
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'HighLoad Cup 2021'}, pythonic_params=True)

    ctrl.limiter = flim.Limiter(app.app, default_limits=[rate_limit], key_func=lambda: 0)

    signal.signal(signal.SIGALRM, kill_handler)
    signal.alarm(run_time)

    try:
        app.run(port=8000)
    finally:
        print(f"Final balance: {ctrl.world.balance}")


if __name__ == '__main__':
    main()
