import subprocess
import sys

filename = 'run.py'
while True:
    p = subprocess.Popen('python {} {}'.format(filename, *sys.argv[1:]), shell=True).wait()

    if p != 0:
        continue
    else:
        break