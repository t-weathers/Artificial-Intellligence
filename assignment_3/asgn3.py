import sys
import string
import math
#from collections import deque
#from collections import defaultdict 

def main():

    #arguments: [0] = filename, [1] = trainingSet.txt, [2] = testSet.txt
    if(len(sys.argv) != 3):
        print("ERROR: incorrect arguments")
        return 1

    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    vocabulary = create_vocab(punctuations)
    #print(vocabulary)

    LEN_VOCAB = len(vocabulary)

    preprocess_train = preprocess(1,vocabulary,punctuations,LEN_VOCAB)
    #print(preprocess_train)
    preprocess_test = preprocess(2,vocabulary,punctuations,LEN_VOCAB)
    write_file(1,vocabulary,preprocess_train)
    write_file(2,vocabulary,preprocess_test)
    

    percent1 = process(vocabulary,preprocess_train, 1, punctuations)
    percent2 = process(vocabulary,preprocess_train, 2, punctuations)
    output = [percent1,percent2]
    
    fo = open("results.txt","w")
    for i in range(1,3):
        fo.write("-----------------------------\n")
        fo.write("NAIVE BAYES CLASSIFIER TESTED WITH: ")
        fo.write(str(sys.argv[i]))
        fo.write("\n")
        fo.write("ACCURACY: ")
        fo.write(str(output[i - 1]))
        fo.write("%\n")
        fo.write("----------------------------\n")
        fo.write("\n")
    fo.close()


    return 0






def preprocess(arg, vocabulary, punctuations, LEN_VOCAB):

    ff = open(sys.argv[arg])
    ff.seek(0)
    line = ff.readline()
    #print(line)
    prep_train = []
    linenum = 0
    while line:
        prep_train.append([])

        words = line.split()
        sign = words[-1]    #grab the postiive or negative
        words = words[:-1] 
        for a in range(0,len(words)):
            words[a] = ''.join(words[a][b] for b in range(len(words[a])) if words[a][b] not in punctuations)    #remove punctuation
            words[a] = words[a].lower()

        for i in range(0,LEN_VOCAB):
            if vocabulary[i] in words:
                prep_train[linenum].append(1)
            else:
                prep_train[linenum].append(0)

        prep_train[linenum].append(int(sign))

        #print(prep_train)
        line = ff.readline()
        linenum += 1

    #output pre-processed training and testing data to 
        #preprocessed_train.txt
        #preprocessed_test.txt
    ff.close()
    return prep_train

def create_vocab(punctuations):
    f = open(sys.argv[1])
    line = f.readline()

    vocabulary = []
    while line:     #strip all punctuation and spaces, only words

        words = line.split()    #split by space and tab
        words = words[:-1]      #remove class ID from the end

        for a in range(0,len(words)):
            words[a] = ''.join(words[a][b] for b in range(len(words[a])) if words[a][b] not in punctuations)    #remove punctuation
            words[a] = words[a].lower()

        #print(words)
        for i in words:
            if i.isalpha():
                if(len(vocabulary) > 0):
                    
                    if i not in vocabulary:
                        counter = 0
                        while counter < len(vocabulary):  #find location of alphabetical order
                            if (i < vocabulary[counter] and i > vocabulary[counter-1]) or  (i < vocabulary[counter] and counter == 0):
                                vocabulary.insert(counter,i)
                                break
                            counter += 1

                        if counter == len(vocabulary) - 1:
                            vocabulary.append(i)
                else:
                    vocabulary.insert(0,i)        #first word in vocabulary

        #print(vocabulary)
        line = f.readline()
    f.close()

    #print(vocabulary)
    return vocabulary

def write_file(outarg, vocabulary, matrix):
    
    if outarg == 1:
        #preprocessed_train.txt
        fo = open("preprocessed_train.txt","w")
    else:
        #preprocessed_test.txt
        fo = open("preprocessed_test.txt","w")

    fo.write(','.join(vocabulary))
    fo.write(',classlabel\n')
    for i in range(0,len(matrix)):
        fo.write(','.join(map(str,matrix[i])))
        fo.write('\n')
    fo.close()

def process(vocabulary, prep_train, arg, punctuations):
    
    #tally number of true and false
    TallyT = 0
    TallyF = 0
    TallyTotal = 0
    for row in range(0,len(prep_train)):
        if prep_train[row][-1] == 0:
            TallyF += 1
        else:
            TallyT += 1
        TallyTotal += 1
    #training phase
    #calulate probabilities of each (word | TRUE~FALSE )
    #4 cases each (word -T, T), (Word - F, T), (Word - T, F), (Word - F, F)

    #dictionary: {word : [P(T|T), P(T|F), P(F|T), P(T|T)]}

    #1 means word is IN the sentence, 0 means word is not in the sentence
    #class Label 1 means sentence is positive, 0 means sentence is negative

    #loop thorough each word in dictionary, find the probabiltiies from the prep_train matrix of 4 cases
    probLookUp = {}
    for col in range(0,len(prep_train[0])-1): 
        FgivF = 0
        FgivT = 0
        TgivF = 0
        TgivT = 0
        for row in range(0,len(prep_train)):
            if prep_train[row][col] == 1 and prep_train[row][-1] == 1:
                TgivT += 1
            elif prep_train[row][col] == 1 and prep_train[row][-1] == 0:
                TgivF += 1
            elif prep_train[row][col] == 0 and prep_train[row][-1] == 1:
                FgivT += 1
            elif prep_train[row][col] == 0 and prep_train[row][-1] == 0:
                FgivF += 1

        pTgivT = math.log(((TgivT + 1) / (TallyT+ 2)))
        pTgivF = math.log(((TgivF + 1)  / (TallyF + 2)))
        pFgivT = math.log(((FgivT + 1) / (TallyT + 2)))
        pFgivF = math.log(((FgivF + 1) / (TallyF + 2)))
        prob_array = [pTgivT,pTgivF,pFgivT,pFgivF]                 #[P(T|T), P(T|F), P(F|T), P(F|F)]
        probLookUp[vocabulary[col]] = prob_array
        
    #print out dictionary of probabilities in log space
    #for i in range(0,len(probLookUp)):
     #   print(vocabulary[i],": ",probLookUp[vocabulary[i]])


    #testing phase
    predicted = []

    probT = math.log((TallyT / TallyTotal)) #P(classlabel = T)
    probF = math.log((TallyF / TallyTotal)) #P(classLabel = F)
    
    ff = open(sys.argv[arg]) #open the testing file
    line = ff.readline()
    ReadClassLabels = []

    while line:     #strip all punctuation and spaces, only words

        words = line.split()    #split by space and tab
        ReadClassLabels.append(int(words[-1]))  #save class ID
        words = words[:-1]      #remove class ID from the end

        for a in range(0,len(words)):
            words[a] = ''.join(words[a][b] for b in range(len(words[a])) if words[a][b] not in punctuations)    #remove punctuation
            words[a] = words[a].lower()

        #begin calculating probabilities of each line
        probT = math.log((TallyT / TallyTotal)) #P(classlabel = T)
        probF = math.log((TallyF / TallyTotal)) #P(classLabel = F)
        for word in words:
            if word in probLookUp:

                probT = probT + probLookUp[word][0]
                probF = probF + probLookUp[word][1]

        if probT > probF:
            predicted.append(1)
        else:
            predicted.append(0)            

        line = ff.readline()
    ff.close()

    totalcorrect = 0
    num_predicted = len(predicted)
    
    for index in range(0,len(ReadClassLabels)):
        if ReadClassLabels[index] == predicted[index]:
            totalcorrect += 1
    
    return (totalcorrect/num_predicted) * 100

main()