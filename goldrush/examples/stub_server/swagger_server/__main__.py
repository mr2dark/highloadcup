#!/usr/bin/env python3

import connexion

from swagger_server import encoder
import swagger_server.controllers.default_controller as ctrl
from swagger_server.models.world import World


def main():
    seed = 0
    ctrl.world = World(seed)
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'HighLoad Cup 2021'}, pythonic_params=True)
    app.run(port=8000)


if __name__ == '__main__':
    main()
