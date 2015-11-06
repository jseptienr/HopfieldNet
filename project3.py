from collections import OrderedDict
from hopfieldnet import HopfieldNet
from sampleset import SampleSet


def show_menu():
    """ Show menu to user """
    print('1) Enter 1 to train a net.')
    print('2) Enter 2 to test a network.')
    selection = input('Select: ')
    if selection == '1':
        print('Enter the filename that contains the samples to store.')
        selection = input('Filename: ')


def train_network(samples_filename, weights_filename):
    """ Perform training on network from file and save weights. """
    sample_set = SampleSet()
    sample_set.init_from_file(samples_filename)
    net = HopfieldNet(sample_set.sample_size)
    net.initialize()
    for sample in sample_set:
        net.train(sample)
    save_weights_to_file(net.weights, weights_filename)


def test_network(weights_filename, samples_filename):
    """ Perform testing on network from weights file."""
    weights = read_weights_from_file(weights_filename)
    net = HopfieldNet(len(weights), weights)
    sample_set = SampleSet()
    sample_set.init_from_file(samples_filename)
    results = []
    for sample in sample_set:
        results.append(net.test(sample))
    return results


def save_weights_to_file(weights, filename):
    """ save weights to specified file """
    with open(filename, 'w') as f:
        f.write('\n'.join([" ".join([str(n) for n in weight]) for weight in weights])) #format weights rows by newline columns by space


def read_weights_from_file(filename):
    """ Read weights from specified file. """
    weights = []
    with open(filename) as f:
        raw_lines = f.readlines()
    for line in raw_lines:
        weights.append(list(map(int, line.strip().split())))
    return weights


def save_results_to_file(results, filename):
    formated_results = []
    for result in results:
        pattern = generate_pattern(result, 10)
        formated_results.append('\n'.join(pattern))
    with open(filename, 'w') as f:
        f.write('\n\n'.join(formated_results))

def generate_pattern(vector, row_size):
    pattern = []
    row = []
    count = 0
    for bit in vector:
        if count == 10:
            pattern.append(''.join(row))
            row = []
            count = 0
        row.append('o' if bit == 1 else '_')
        count += 1
    return pattern

menu = OrderedDict([
    ('', ''),
    ('', '')
])

if __name__ == '__main__':
    train_network('training_samples1.txt', 'weight_settings.txt')
    results = test_network('weight_settings.txt', 'test_samples.txt')
    save_results_to_file(results, 'results.txt')