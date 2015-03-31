from re import sub

#Terminology:
#
#String Pattern: The input that is to be compared against to check whether the substring exists within.  
#For example, if I want to check if the word 'dog' is in 'The dog is tired.', the latter sentence is considered
#as the string pattern.
#
#Substring: The input that the user wants to know whether it exists within the string pattern.  In the above
#example, it would be the word 'dog'/
#
#Partitions: The string pattern is partitioned based off the letters of the substring in chronological order.  
#For the above example, the string pattern would initially be partitioned by the letter 'd'.  If no answer
#is found, latter letter partitions are performed ('o' followed by 'g') to check whether a mispell of the 
#substring may be present.
#
#Score: A score is associated with every partitioned set of words.  The score is an aggregate of how 'incorrect'
#a set of partitioned characters are.  Because the algorithm never does a full letter by letter comparison
#(which can be very performance costly), it relies on the score to tell it how incorrect the partitioned set
#of characters are.  If the score gets too high, the algorithm will remove the set of characters as a possible
#match.
#
#Various Indexes: The algorithm uses several indexes to count the position If you are wondering why the index
#error has a function as opposed to throwing a error/warning, it is because usage of the index errors is an easy
#way to catch missing end letters on the partitioned string patterns, since you can't check to see if a letter
#equals 'None' without getting an index error.

def compare(main, substring):
    #The input is initially filtered, than it is partitioned.  The number of partitions is dependent on
    #whether an answer is found and also the length of the substring.  If a match is found, it will stop
    #otherwise, it procedes with latter letter partitions until the algorithm knows there can be no
    #more possible matches.
    main = filterstringpattern(main)
    for k in range(0, len(substring)):
        dividedlist = divlist(main, substring[k], len(substring))
        scores = [k*10]*len(dividedlist)
        result = checklist(dividedlist, substring[k:], 0, scores)
        for key,v in result.items():
            if key is not None:
                if int(v) > 25:
                    adjustedscore = -0.1*abs((int(v)-100))**1.6 + 100
                    #Adjusted score is the score that better represents the accuracy of the predicted matched word.
                    #The purpose of using the adjusted score is that the inverse exponential portion makes the scoring such that
                    #lower and higher end scores are more likely to be output, which give a definitive answer, while
                    #medium-ranged scores that are not exactly very informative of how accurate the word is are distrubuted
                    #less often.
                    print('Match found to ' + substring + ' with a certainty of ' + str(int(adjustedscore)) + ', reconstructed word is ' + substring[:k] + key +'.')
                    return
        if k > int(len(substring)/2):
            print('No matches were found to ' + substring + ' with reasonable certainty.')
            return     
        
       
#This function filters out irrelevant characters from the string pattern
def filterstringpattern(strg):
    words = sub(r'[^\w\s]','',strg) #Remove all punctuation
    words = words.replace(' ','') #Removes spaces between words
    words = words.lower()  #Turn all capital letters to lower letters
    return words

#divlist will return a list with all sets of words that start with delimiter 'delim'
#It is important to know that all of the elements return by divlist will have a minimum length equal 
#to the length of the substring.  This is done using a neat partitioning trick that works almost in linear
#time by using a queue.
def divlist(strg, delim, sslen): #assumes string is already filtered
    q = []
    splitlist = []
    dividedlist = []
    for ch in strg:
        if ch not in delim:
            splitlist.append(ch)
        else:
            if splitlist:
                templength = abs(len(splitlist) - sslen)
                if splitlist[0] == delim:
                    if len(splitlist) < sslen:
                        q.append(templength)
                        templength = 0
                    dividedlist.append(''.join(splitlist))
            splitlist = []
            splitlist.append(ch)
        if q:
            for i in range (1,len(q)+1): #not sure if this can be made into a comprehension
                dividedlist[-i] += ch
            q = [elem - 1 for elem in q]
            if q[0] is 0:
                q.pop(0)
    if splitlist:
        dividedlist.append(''.join(splitlist))
    return dividedlist

#This is the basic function to perform a preliminary check to see whether the partitioned words
#may possibly be the 'correct' word.  If it is, it is sent to a secondary check which singles out the 
#potential word.
def checklist(dividedlist, substr, index, scores):
    rating = {}
    dlistlen = len(dividedlist)
    #[obj, obj, obj, obj]
    #[ s1, s2 , s3 , s4 ]
    
    for i in range(0,dlistlen):
        
        #If this function is called and the index is greater than the length of the substring, this will
        #indicate there is no answer.  This will occur during latter letter partitions in complex cases.            
        if index >= len(substr):
            return {None:0}
        
        #This sets a predetermined threshold for how 'wrong' a word can be.  The threshold is based off
        #the length of the substring, with adjustments based off what letter the substring is being 
        #partitioned on.
        if index >= len(substr)/2:
            threshold = (len(substr) - index)*20
        else:
            threshold = 0;
        
        try:
            #Searchdist is fairly arbitrary, but what it means is that there is generally a 5 character leeway
            #when a searchdist of 3 is applied.  What this means is that a letter can be two positions backwards
            #or two positions forward from the index, and the algorithm will be able to recognize that there 
            #is a character match.  That being said, the further off the character is off from the original
            #position, the more points it earns toward the word being 'incorrect'.
            searchdist = 3 #, len(substr)-index)

            #if there is no direct letter match at the same index
            if dividedlist[i][index] is substr[index]: 
                scores[i] += 0
            #if two letters are correct but just swapped, the algorithm swaps them back.
            elif index < len(dividedlist[i]) - 1 and substr[index + 1] is dividedlist[i][index] and dividedlist[i][index + 1] is substr[index]:
                dividedlistl = list(dividedlist[i])
                dividedlistl[index + 1], dividedlistl[index] = dividedlistl[index], dividedlistl[index + 1]
                dividedlist[i] = ''.join(dividedlistl)
                scores[i] += 10
            #if a letter is out of place, letter insertions/deletions are performed.
            elif substr[index + 1] in dividedlist[i][index:index+searchdist+1]:
                nextletterindex = dividedlist[i][index:index+searchdist+1].index(substr[index + 1]) + index
                #case of a one letter off 
                if nextletterindex < index + 1:
                    dividedlistl = list(dividedlist[i])
                    dividedlistl.insert(index,substr[index])
                    dividedlist[i] = ''.join(dividedlistl)
                    scores[i] += 15
                #case where there are multiple letters on the index
                elif nextletterindex >= index + 1:
                    dividedlist[i] = dividedlist[i].replace(dividedlist[i][index:nextletterindex],substr[index])
                    scores[i] += 10 + 3**((nextletterindex - (index + 1)) + 1)

            else: #if word does not match, and is not one over within a margin of 3
                #likely indicates that the current and next letter are off, so the word needs to check
                #the following letter to see if it is correct
                dividedlistl = list(dividedlist[i])
                dividedlistl.insert(index,substr[index])
                dividedlist[i] = ''.join(dividedlistl)
                scores[i] += 35
        except IndexError:
            #string pattern length is smaller than the length of the substring
            dividedlistl = list(dividedlist[i])
            dividedlistl.insert(index,substr[index])
            dividedlist[i] = ''.join(dividedlistl)
            scores[i] += 15
        
        #Once every word in dlistlen is checked, the scores of all elements are checked.  Any scores
        #that are reasonable are further checked, while poor scores are thrown out.
        if i is dlistlen-1:  
            #checks uncertainty of the word
            for idx, score in enumerate(scores):
                #if it is bad, then you throw the word out from the dividedlist
                if score > len(substr)*10:
                    dividedlist.pop(idx)
                    scores.pop(idx)
                if score < threshold:
                    #check accuracy should return a dictionary with the 'word' and its accuracy
                    #add the dictionary to the dictionary rating
                    dictresult = checkaccuracy(dividedlist[idx], substr, index + 1, score)
                    if rating:
                        maxword = max(rating, key=(lambda key: rating[key]))
                        maxscre = rating[maxword]
                        for k,v in dictresult.items():
                            if v > maxscre:
                                rating.update(dictresult)
                    else:
                        rating.update(dictresult)
                    #sort the dictionary by highest rating its size is > 1
                    #return the highest value from the dictionary
            if rating:
                word = max(rating, key=(lambda key: rating[key]))
                scre = rating[word]
                return {word:scre}
            
            #If there are no more possible matches, the algorithm knows that partitions at this letter have
            #no correct matches.
            if not dividedlist:
                return {None: 0}
            
            #If there a no satisfactory scores, the algorithm repeats at the following index.
            return checklist(dividedlist, substr, index + 1, scores)
        
        #This is the end condition where no possible matches are found.  Happens in extreme cases where
        #the string pattern is very small in length (e.x. 2 characters).
        if i == dlistlen and index == len(substr):
            return {None: 0}

#This performs a similar function to checklist except it checks a single element against the substring.  
#This is used when the algorithm is fairly certain there may be a match, and will return a rating from
#0-100 depending on the accuracy.  See the checklist function for greater detail on how this function operates.
def checkaccuracy(words, substr, index, score):
    
    for i in range(index, len(substr)):
        try:
            searchdist = 3
            #if there is no direct letter match at the same index
            if words[i] is substr[i]: 
                #score add 0 
                score += 0
            elif i < len(words) - 1 and substr[i + 1] is words[i] and words[i + 1] is substr[i]:
                wordsl = list(words)
                wordsl[i + 1], wordsl[i] = wordsl[i], wordsl[i + 1]
                words = ''.join(wordsl)
                score += 10
            elif substr[i + 1] in words[i:i+searchdist+1]:
                nextletterindex = words[i:i+searchdist+1].index(substr[i + 1]) + i
                #case of a one letter off 
                if nextletterindex < i + 1:
                    wordsl = list(words)
                    wordsl.insert(index,substr[i])
                    words = ''.join(wordsl)
                    score += 15
                #case where there are multiple letters on the index
                elif nextletterindex >= i + 1:
                    words = words.replace(words[i:nextletterindex],substr[i])
                    score += 10 + 3**((nextletterindex - (i + 1)) + 1)

            else:
                wordsl = list(words)
                wordsl.insert(i,substr[i])
                words = ''.join(wordsl)
                score += 35
        except IndexError:
            #this means that the word is 1 letter shorter than the substring, and it hits an index error
            wordsl = list(words)
            wordsl.insert(i,substr[i])
            words = ''.join(wordsl)
            score += 15

    rating = 100*(1 - score/(len(substr)*20))
    #Now the matching string needs to be found
    matcher = words[0:len(substr)]
    return {matcher:rating}

