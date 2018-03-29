import re
from bsimcmg import *

def read_mdl(file):
    mdl = {}
    with open(file,'r') as f:
        lines = f.read().splitlines()
    for line in lines:
        param, value = re.split('[=\s]+', line)
        mdl[param] = float(value)
    return mdl

filepath = "modelcard.l"
param = read_mdl(filepath)

Id, Ig, Is, Ib = BSIMCMG(**param).calc()

print(f'Id = {Id:>16.9e} A')
print(f'Ig = {Ig:>16.9e} A')
print(f'Is = {Is:>16.9e} A')
print(f'Ib = {Ib:>16.9e} A')