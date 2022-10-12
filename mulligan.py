from quizdb import get_game
from distro_maker import make_game
from configs import output_folder

from timeit import default_timer as tictoc
import datetime
import json

def get_title():
    return output_folder + 'QB_Practice-' + datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + '-Packet.json'

def create_game():
    tus, bons = make_game()
    return get_game(tus, bons)

def run_out():
    t0 = tictoc()
    g = create_game()
    gd = g.to_json_dict()
    title = get_title()
    with open(title, 'w') as f:
        json.dump(gd, f, indent=2)
    t1 = tictoc()
    et = t1 - t0
    print(f"Packet {title} successfully created in {et} seconds.")
    
if __name__ == '__main__':
    run_out()
    