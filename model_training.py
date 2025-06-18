import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt

ITERATIONS = 1000
ALPHA = 0.01

def plot_step(mileage, price, theta0, theta1, iteration):
    plt.clf()
    plt.scatter(mileage, price, color='blue', label='Data')

    x_line = np.linspace(min(mileage), max(mileage), 100)
    y_line = theta0 + theta1 * x_line
    plt.plot(x_line, y_line, color='red', label=f'regression for {iteration} iterations')

    plt.title(f"linear regression at iterations {iteration}")
    plt.xlabel("Mileage")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.pause(0.05)

def get_data(filename):
    dataset = []
    try:
        data = open(filename, 'r')
        data_line = data.readline()
        while data_line:
            # data_line = data.readline()
            splitedData = data_line.split(',')
            try:
                nombres = list(map(int, splitedData))
                dataset.append(nombres)
            except:
                print("Bad format of dataline, skipping...")
            data_line = data.readline()
        data.close()
    except:
        print("Error during reading file")
        exit(1)
    return dataset

def training():
    show_linear = False
    show_training = False

    parser = argparse.ArgumentParser(description='Linear Regression training model')
    parser.add_argument("data", help="CSV file of data (mileage, price)")
    parser.add_argument("-w", "--window", action="store_true", help="Display the linear regression view")
    parser.add_argument("-s", "--show-training", action="store_true", help="Display the linear regression while training")

    args = parser.parse_args()

    dataset = get_data(args.data)

    if args.window:
        show_linear = True
    if args.show_training:
        show_linear = True
        show_training = True

    # -- Normalize data --
    dataset = np.array(dataset, dtype=float)
    mileage = dataset[:, 0]
    price = dataset[:, 1]

    mileage_mean = np.mean(mileage)
    mileage_std = np.std(mileage)
    price_mean = np.mean(price)
    price_std = np.std(price)

    mileage_normalized = (mileage - mileage_mean) / mileage_std
    price_normalized = (price - price_mean) / price_std

    # -- Calculate theta --
    theta0 = 0.0
    theta1 = 0.0
    for i in range(ITERATIONS):
        estimated_price = theta0 + (theta1 * mileage_normalized)
        theta0 -= (ALPHA * np.sum( estimated_price - price_normalized ))/len(dataset)
        theta1 -= (ALPHA * np.sum( (estimated_price - price_normalized) * mileage_normalized )) / len(dataset)
        if show_training and i % 10 == 0:
            theta1_display = theta1 * (price_std / mileage_std)
            theta0_display = price_mean + price_std * theta0 - theta1_display * mileage_mean
            plot_step(mileage, price, theta0_display, theta1_display, i)

    theta1 = theta1 * (price_std / mileage_std)
    theta0 = price_mean + price_std * theta0 - theta1 * mileage_mean
    print("Theta found: T0: ", theta0, ", T1: ", theta1)

    if show_linear:
        plot_step(mileage, price, theta0, theta1, ITERATIONS)
        plt.ioff()
        plt.show()

    # -- write final theta in file --
    with open('theta.txt', 'w') as f:
        f.write(str(theta0) + "," + str(theta1))

if __name__ == '__main__':
    training()