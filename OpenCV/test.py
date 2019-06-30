import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-x', '--one')
parser.add_argument('-y', '--two')
parser.add_argument('-z', '--three')

args = vars(parser.parse_args())

args["one"] = "okay"

print(args)