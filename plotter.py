import matplotlib.pyplot as plt
import csv

modes = ['helicopter', 'thrust', 'gravity']


class Plotter:

    def __init__(self, mode):
        self.mode = mode
        self.maxs = []
        self.mins = []
        self.averages = []

        self.read_csv_file()

    def read_csv_file(self):
        filename = self.mode + '.csv'
        with open(filename, 'r') as file:
            csvreader = csv.reader(file)
            fields = next(csvreader)

            for row in csvreader:
                self.maxs.append(int(row[0]))
                self.mins.append(int(row[1]))
                self.averages.append(float(row[2]))

    def plot(self):
        generations = [x + 1 for x in range(0, len(self.maxs))]

        plt.plot(generations, self.maxs, label='best fitness')
        plt.plot(generations, self.mins, label='worst fitness')
        plt.plot(generations, self.averages, label='average fitness')

        plt.xlabel('generations')
        plt.ylabel('fitness')

        plt.title('Statistics')

        plt.legend()

        plt.show()


if __name__ == '__main__':
    mode = input('please enter game mode : ')
    while mode not in modes:
        print("Mode not exists!")
        mode = input('please enter proper game mode : ')

    plotter = Plotter(mode)
    plotter.plot()
