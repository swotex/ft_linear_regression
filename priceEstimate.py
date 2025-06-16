def get_teta():
    try:
        file = open('teta.txt', 'r')
        teta_line = file.read()
        file.close()
        tetas = teta_line.split(',')
        while len(tetas) < 2:
            tetas.append('0.0')
        tetas[0] = float(tetas[0])
        tetas[1] = float(tetas[1])
        return tetas
    except:
        print('Set default teta at 0')
        return [0.0, 0.0]

def estimate_price():
    tetas = get_teta()
    print("Teta0: " + str(tetas[0]) + " - " + "Teta1: " + str(tetas[1]))
    try:
        userEntry = int(input("Set a mileage: "))
    except ValueError:
        print("error: Is not a valid mileage")
        exit(1)
    if userEntry < 0:
        print("error: Is not a valid mileage")
        exit(1)
    print((tetas[0] + (tetas[1] * userEntry)))

if __name__ == '__main__':
    estimate_price()