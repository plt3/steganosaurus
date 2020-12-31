import sys
import random
import string


def makeSentOrPar(oldList, sentence=True):
    if sentence:
        lowerBound = 15
        upperBound = 30
    else:
        lowerBound = 4
        upperBound = 8

    sentParLength = random.randint(lowerBound, upperBound)
    returnList = []
    counter = 0
    sentPar = ''

    for wordSent in oldList:
        if counter == 0:
            if sentence:
                sentPar += wordSent.title() + ' '
            else:
                sentPar += '\t' + wordSent + ' '
            counter += 1
        elif counter == sentParLength:
            if sentence:
                sentPar += wordSent + '.'
            else:
                sentPar += wordSent + '\n'
            returnList.append(sentPar)
            sentPar = ''
            sentParLength = random.randint(lowerBound, upperBound)
            counter = 0
        else:
            sentPar += wordSent + ' '
            counter += 1

    returnList.append(sentPar.rstrip())

    return returnList


def lorem(number):
    wordsList = []
    for _ in range(number):
        wordsList.append(''.join([
            random.choice(string.ascii_lowercase)
            for _ in range(random.randint(1, 7))
        ]))

    sentenceList = makeSentOrPar(wordsList)
    paragraphList = makeSentOrPar(sentenceList, sentence=False)

    return ''.join(paragraphList).rstrip()


if __name__ == '__main__':
    try:
        numWords = int(sys.argv[1])
        print(lorem(numWords))
    except ValueError:
        print('ERROR: positional argument must be an integer')
    except IndexError:
        print('ERROR: must include a positional argument for number of words.')
