import sys

def estimatePrice(mileage, teta0, teta1):
    return teta0 + (teta1 * mileage)

def training():
    if (len(sys.argv) != 2):
        print("Usage: python model_training.py <data>")
        exit(1)
    dataset = []
    try:
        data = open(sys.argv[1], 'r')
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
        print("Error during training")

    teta0 = 0.0
    teta1 = 0.0
    alpha = 0.0000000001
    for _ in range(100):
        sumForTeta0 = 0
        sumForTeta1 = 0
        for data2 in dataset:
            tmp = (estimatePrice(data2[0], teta0, teta1) - data2[1])
            sumForTeta0 += tmp
            sumForTeta1 += tmp * data2[0]
        teta0 -= (alpha * sumForTeta0)/len(dataset)
        teta1 -= (alpha * sumForTeta1) / len(dataset)

    print(teta0, " - ", teta1)
    with open('teta.txt', 'w') as f:
        f.write(str(teta0) + "," + str(teta1))

if __name__ == '__main__':
    training()