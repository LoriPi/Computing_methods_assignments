import argparse
import string
import time

from loguru import logger
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(prog='wordcount',
    description='Count the letter frequency in a text')
parser.add_argument('infile', help='the name of the file of your choice')
parser.add_argument('-p', '--plot', action='store_true',
    help='plot a bar chart of the character frequencies')
parser.add_argument('-s', '--stats', action='store_true',
    help='print out basic book stats (number of characters, number of words, number of lines)')
parser.add_argument('-k', '--skip', type=str,
    help='skip the parts of the text that do not pertain to the book (preamble and license), the argument signals the end of the preamble and the start of the license section')


def process_file(file_path, plot=False, stats=False, skip=None):

    """Process open file and count the occurrences of each
    character.

    Arguments
    ---------
    file_path : str
        Path to the input file.
    plot : bool
        If true, plot letter occurrences.
    stats : bool
        If true, print book stats.
    skip : str
        Skip preamble and license, signaled by a line containing the argument.
    """

    start_time = time.time()
    #for elapsed time emasurement
    logger.info(f'Opening input file {file_path}...')
    with open(file_path, encoding="utf8") as input_file:
        data = input_file.readlines()
    input_file.close()
    logger.info('Input file data copied successfully')
    #convert file to list of strings (the lines of the book)

    if skip:
        logger.info('Deleting preamble and license...')
        book = False
        #only True when reading the actual book
        new_data = list()
        for line in data:
            if skip in line:
                book = not book
                logger.info(f'book value switched to {book}')
                continue
            #switches the value of book to True at the and of the preamble and back to False at the start of the license section
            if book == True:
                new_data.append(line)
            #new_data only contains the actual book lines
        data = new_data
        logger.info('File data updated successfully')

    characters = sum(len(line) for line in data)
    logger.info(f'{characters} character(s) found.')
    alphabet = list(string.ascii_lowercase)
    #make a list of the alphabet
    occurrences = list()
    logger.info('Counting letter occurrences...')
    for letter in alphabet:
        N = 0
        for line in data:
            N += line.lower().count(letter)
        occurrences.append(N)
    #count the occurrences of each letter in every line
    logger.info('Occurrences counted')
    #append the number of occurrences of each letter to occurrences (not case sensitive)
    total_occurrences = sum(occurrences)
    frequency = np.divide(occurrences, total_occurrences)
    #obtain the relative frequencies from the occurrences
    for index, letter in enumerate(alphabet):
        print(f'relative frequency of letter {letter}: {frequency[index]}')
    #print the relative occurrencies of each letter

    if stats:
        logger.info('Elaborating file stats...')
        spaces = sum(line.count(' ') for line in data)
        words = sum(len(line.split()) for line in data)
        #count number of spaces and words in file
        lines = len(data)
        #count number of lines
        skips = 0
        for line in data:
            if line.strip() == '':
                skips += 1
        #count number of empty lines
        print('book stats:')
        print(f'number of characters: {characters}, of which {spaces} are spaces')
        print(f'number of words: {words}')
        print(f'number of lines: {lines}, of which {skips} are empty')

    elapsed_time = time.time() - start_time
    print(f'total elapsed time = {elapsed_time}')

    if plot:
        logger.info('Plotting stuff...')
        plt.bar(alphabet, frequency)
        plt.show()

    logger.info('All done')


if __name__ == '__main__':
    args = parser.parse_args()
    process_file(args.infile, args.plot, args.stats, args.skip)