import pykemon
import random
import requests
import os
import shutil
import sys
from PIL import Image

from util import convert_to_jpg
from img2txt import ansify_image

HTTP_OK = 200
MAX_POKEMON_ID = 719

SPRITES_DIR_NAME = 'sprites/'
POKEAPI_BASE = 'http://pokeapi.co'


def get_random_pokemon_id():
    """Generates a random pokemon id."""
    return random.randint(1, MAX_POKEMON_ID)

def get_random_pokemon():
    """Generates a random pokemon sprite object using the pokeapi.co API"""
    pokemon_id = get_random_pokemon_id()
    return pykemon.get(sprite_id=pokemon_id)

def get_pokemon_sprite(sprite_resource):
    url = POKEAPI_BASE + sprite_resource.image

    response = requests.get(url)
    if response.status_code != HTTP_OK:
        raise Exception("Response was not OK")

    file_name = os.getcwd() + '/sprites/' + sprite_resource.pokemon['name'] + '.png'

    # let's make sure this file doesn't exist.
    if os.path.exists(file_name):
        return file_name

    # ok, cool. time to get it.
    with open(file_name, 'wb') as pokemon_file:
        pokemon_file.write(response.content)

    return file_name

def maybe_create_sprite_dir():
    sprites_dir = os.path.dirname(SPRITES_DIR_NAME)

    # return if the directory exists.
    if os.path.exists(sprites_dir):
        return

    os.makedirs(sprites_dir)

if __name__ == '__main__':
    maybe_create_sprite_dir()

    pokemon = get_random_pokemon()
    sprite_file = get_pokemon_sprite(pokemon)

    jpeg_file = convert_to_jpg(pokemon.pokemon['name'], sprite_file)
    ansified_image = ansify_image(jpeg_file, 80)

    sys.stdout.write(ansified_image)
    sys.stdout.flush()
