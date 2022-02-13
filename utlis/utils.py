import math
import random


def generate_code():
    digits = [i for i in range(0, 10)]
    code = ""
    for i in range(6):
        index = math.floor(random.random() * 10)

        code += str(digits[index])

    return code

def generate_id(model):
    id = 0
    lastest_entry = model.objects.last()
    if lastest_entry is None:
        id = 1
    else:
        id = lastest_entry.id + 1

    return id