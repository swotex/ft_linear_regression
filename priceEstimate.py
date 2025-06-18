def get_theta():
    try:
        file = open('theta.txt', 'r')
        theta_line = file.read()
        file.close()
        thetas = theta_line.split(',')
        while len(thetas) < 2:
            thetas.append('0.0')
        thetas[0] = float(thetas[0])
        thetas[1] = float(thetas[1])
        return thetas
    except:
        print('Set default theta at 0')
        return [0.0, 0.0]

def estimate_price():
    thetas = get_theta()
    print("theta0: " + str(thetas[0]) + " - " + "theta1: " + str(thetas[1]))
    try:
        userEntry = int(input("Set a mileage: "))
    except ValueError:
        print("error: Is not a valid mileage")
        exit(1)
    if userEntry < 0:
        print("error: Is not a valid mileage")
        exit(1)
    print((thetas[0] + (thetas[1] * userEntry)))

if __name__ == '__main__':
    estimate_price()