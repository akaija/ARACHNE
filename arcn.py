#!/usr/bin/env python

import os

import click
import yaml

import arachne
from arachne.files import read_config
from arachne.arachne import view_monomer, all_atom_polymer

def start(config_path):
    config = read_config(config_path)
    arcn_dir = os.path.dirname(os.path.dirname(arachne.__file__))
    config["output_path"] = os.path.join(arcn_dir, config["monomer"])
    os.makedirs(config["output_path"], exist_ok=True)
    with open(os.path.join(config["output_path"], "config.yaml"), "w") as f:
        yaml.dump(config, f, default_flow_style=False)
    return config

@click.group()
def arcn():
    pass

@arcn.command()
@click.argument("config_path", type=click.Path())
def render_input(config_path):
    config = start(config_path)
    view_monomer(config)

@arcn.command()
@click.argument("config_path", type=click.Path())
def polymerize_all_atom(config_path):
    config = start(config_path)
    all_atom_polymer(config)

if __name__ == "__main__":
    arcn()
