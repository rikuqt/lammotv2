import json 
import requests
import random
import time


def random_lammot():
    cpu = 0
    cpupros = 0
    ram = 0
    rampros = 0

    alfa = 0
    while alfa < 100:
        cpu = random.randint(80,85)
        cpupros = random.randint(60,70)
        ram = random.randint(35,40)
        rampros = random.randint(65,70)

        measurement = { }
        measurement['alfa'] = alfa
        measurement['cpu'] = cpu
        measurement['cpupros'] = cpupros
        measurement['ram'] = ram
        measurement['rampros'] = rampros
    
        # TODO: lähetä data HTTP Postilla serverille
        s = json.dumps(measurement)
        response = requests.post("http://localhost:5000/uusimittaus", data = s)

        print(s)
        time.sleep(1)

        alfa += 1

def main ():
    random_lammot()
    


main ()