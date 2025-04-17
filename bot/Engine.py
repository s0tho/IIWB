import subprocess
import sys
from iiwb import _env


# Push IIWB's Token
sys.argv.insert(1, _env.TOKEN)

while True:
    p = subprocess.Popen('python {} {}'.format(_env.IIWB_MAIN, *sys.argv[1:]), shell=True).wait()

    if p != 0:
        continue
    else:
        break


"""
import argparse


if __name__ == "__main__":

   cmd_parser = argparse.ArgumentParser(description="Discord's bot IIWB")
   cmd_parser.add_argument("-t", "--token", help="Discord Bot Token")
   cmd_parser.add_argument("-L", "--log-level",
                           help="Logging level in [DEBUG,INFO,WARNING,ERROR] (default=INFO)",
                           default="INFO",
                           choices=["DEBUG", "INFO", "WARNING", "ERROR"])

   args, unknown = cmd_parser.parse_known_args()

print(args, unknown)
"""