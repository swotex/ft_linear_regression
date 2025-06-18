import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt

ITERATIONS = 1000
ALPHA = 0.01

def estimatePrice(mileage, teta0, teta1):
    return teta0 + (teta1 * mileage)

def plot_step(mileage, price, teta0, teta1, iteration):
    plt.clf()
    plt.scatter(mileage, price, color='blue', label='Data')

    x_line = np.linspace(min(mileage), max(mileage), 100)
    y_line = teta0 + teta1 * x_line
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
    # if (len(sys.argv) != 2):
    #     print("Usage: python model_training.py <data>")
    #     exit(1)

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


    dataset = np.array(dataset, dtype=float)
    mileage = dataset[:, 0]
    price = dataset[:, 1]

    mileage_mean = np.mean(mileage)
    mileage_std = np.std(mileage)
    price_mean = np.mean(price)
    price_std = np.std(price)

    mileage_normalized = (mileage - mileage_mean) / mileage_std
    price_normalized = (price - price_mean) / price_std


    teta0 = 0.0
    teta1 = 0.0
    for i in range(ITERATIONS):
        estimatePrice = teta0 + (teta1 * mileage_normalized)
        teta0 -= (ALPHA * np.sum( estimatePrice - price_normalized ))/len(dataset)
        teta1 -= (ALPHA * np.sum( (estimatePrice - price_normalized) * mileage_normalized )) / len(dataset)
        if show_training and i % 10 == 0:
            teta1_display = teta1 * (price_std / mileage_std)
            teta0_display = price_mean + price_std * teta0 - teta1_display * mileage_mean
            plot_step(mileage, price, teta0_display, teta1_display, i)

    teta1 = teta1 * (price_std / mileage_std)
    teta0 = price_mean + price_std * teta0 - teta1 * mileage_mean
    print("Teta found: T0: ", teta0, ", T1: ", teta1)

    if show_linear:
        plot_step(mileage, price, teta0, teta1, ITERATIONS)
        plt.ioff()
        plt.show()

    with open('teta.txt', 'w') as f:
        f.write(str(teta0) + "," + str(teta1))

if __name__ == '__main__':
    training()