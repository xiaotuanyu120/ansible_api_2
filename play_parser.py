# coding=utf-8

import yaml


def yaml_parser(file):
    with open(file, 'r') as stream:
        try:
            print(yaml.load(stream))
        except yaml.YAMLError as ye:
            print(ye)


if __name__ == '__main__':
    yaml_parser('./test.yml')
