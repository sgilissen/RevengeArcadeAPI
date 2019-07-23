from typing import Optional, Awaitable

__author__ = 'Steve Gilissen'
__copyright__ = 'Copyright 2019 - Steve Gilissen'
__credits__ = ['Steve Gilissen']
__license__ = 'MIT'
__version__ = '0.0.1'

# ---------------------------------------------------------
# MODULE IMPORTS
# ---------------------------------------------------------
import os
import threading

from PIL import Image
from winregistry import WinRegistry as Reg
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from pystray import Icon, Menu, MenuItem

registry = Reg()
reg_path = r'HKCU\Software\ONIROS\Revenge'
image = Image.open("trayicon.png")

# ---------------------------------------------------------
# THREADS
# ---------------------------------------------------------
thread = threading.Thread(daemon=True, target=lambda: Icon(
    'Brixel Revenge API',
    image,
    title='Brixel Revenge API',
    menu=Menu(
        MenuItem(
            'Exit',
            lambda icon, item: kill_app(icon)))).run())
thread.start()
    

# ---------------------------------------------------------
# TORNADO HANDLER CLASSES
# ---------------------------------------------------------
class HomeHandler(RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        self.write("BRIXEL Revenge API version {0} - Ready".format(__version__))


class APIHandler(RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        high_scores = {}

        for hs_key_index in range(8):
            player_name = registry.read_value(reg_path, 'HN_{0}'.format(hs_key_index))['data']
            player_score = registry.read_value(reg_path, 'HS_{0}'.format(hs_key_index))['data']
            high_scores[player_name] = player_score

        data = {
            'total_uptime': registry.read_value(reg_path, 'PoweredTime'.format(hs_key_index))['data'],
            'total_playtime': registry.read_value(reg_path, 'PlayedTime'.format(hs_key_index))['data'],
            'coins_counter': registry.read_value(reg_path, 'NbCoins'.format(hs_key_index))['data'],
            'games_counter': registry.read_value(reg_path, 'NbGames'.format(hs_key_index))['data'],
            'highest_time': registry.read_value(reg_path, 'HighestTime'.format(hs_key_index))['data'],
            'coins_needed': registry.read_value(reg_path, 'Coin'.format(hs_key_index))['data'],
            'coins_adder': registry.read_value(reg_path, 'CoinAdder'.format(hs_key_index))['data'],
            'demo_sound': registry.read_value(reg_path, 'DemoSound'.format(hs_key_index))['data'],
            'difficulty': registry.read_value(reg_path, 'Difficulty'.format(hs_key_index))['data'],
            'high_scores': high_scores
        }

        self.write(data)


def kill_app(icon):
    icon.stop()
    io_loop.stop()
    os._exit(1)


def make_app():
    urls = [
        ("/", HomeHandler),
        ("/api/", APIHandler),
    ]
    return Application(urls)


if __name__ == '__main__':
    app = make_app()
    app.listen(8580)
    io_loop = IOLoop.instance()
    io_loop.start()
    thread.join()
