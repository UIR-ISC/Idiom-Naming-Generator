import torch
from exchange_idioms import main_replace
from random_place import random_replace

cpname1="吴邪"
cpname2="张起灵"
cpname3="闷油瓶"

def cpname(cpname1,cpname2):
    position1=random_replace(len(cpname1))
    position2=random_replace(len(cpname2))
    modified_idioms=main_replace([cpname1[position1],cpname2[position2]])
    return modified_idioms['modified_idioms'].tolist()

print(cpname(cpname1,cpname2))