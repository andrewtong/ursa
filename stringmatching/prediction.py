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
    result = score(main, substring)
    if result > 0:
        print('Match found to ' + substring + ' with a certainty of ' + str(result) +'.')
        return
    else:
        print('No matches were found to ' + substring + ' with reasonable certainty.')
        return         
        
def score(main, substring):
    #score functions identically to compare, except it returns the integer value that represents the likeliness between
    #the two strings as opposed to a string value.
    main = filter_string_pattern(main)
    for k in range(0, len(substring)):
        divided_list = div_list(main, substring[k], len(substring))
        scores = [k*10]*len(divided_list)
        result = check_list(divided_list, substring[k:], 0, scores)
        for key,v in result.items():
            if key is not None and int(v) > 25:
                adjusted_score = -0.1*abs((int(v)-100))**1.6 + 100
                #Adjusted score is the score that better represents the accuracy of the predicted matched word.
                #The purpose of using the adjusted score is that the inverse exponential portion makes the scoring such that
                #lower and higher end scores are more likely to be output, which give a definitive answer, while
                #medium-ranged scores that are not exactly very informative of how accurate the word is are distributed
                #less often.
                return int(adjusted_score)
        if k > int(len(substring)/2):
            return 0
     
       
#This function filters out irrelevant characters from the string pattern
def filter_string_pattern(strg):
    words = sub(r'[^\w\s]','',strg) #Remove all punctuation
    words = words.replace(' ','') #Removes spaces between words
    words = words.lower()  #Turn all capital letters to lower letters
    return words

#div_list() will return a list with all sets of words that start with delimiter 'delim'
#It is important to know that all of the elements return by div_list() will have a minimum length equal 
#to the length of the substring.  This is done using a neat partitioning trick that works almost in linear
#time by using a queue.

#Notation
#string_pat: String Pattern
#delim: delimiting letter of the substring
#ss_len: substring length

def div_list(string_pat, delim, ss_len): #assumes string is already filtered
    q = []
    split_list = []
    divided_list = []
    for ch in string_pat:
        if ch not in delim:
            split_list.append(ch)
        else:
            if split_list:
                temp_length = abs(len(split_list) - ss_len)
                if split_list[0] == delim and len(split_list) < ss_len:
                    #if len(split_list) < ss_len:
                    q.append(temp_length)
                    temp_length = 0
                    divided_list.append(''.join(split_list))
            split_list = []
            split_list.append(ch)
        if q:
            for i in range (1,len(q)+1): #not sure if this can be made into a comprehension
                divided_list[-i] += ch
            q = [elem - 1 for elem in q]
            if q[0] is 0:
                q.pop(0)
    if split_list:
        divided_list.append(''.join(split_list))
    return divided_list

#This is the basic function to perform a preliminary check to see whether the partitioned words
#may possibly be the 'correct' word.  If it is, it is sent to a secondary check which singles out the 
#potential word.
def check_list(divided_list, substr, index, scores):
    rating = {}
    div_list_len = len(divided_list)
    #[obj, obj, obj, obj]
    #[ s1, s2 , s3 , s4 ]
    
    for i in range(0,div_list_len):
        
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
            search_dist = 3 #, len(substr)-index)

            #if there is no direct letter match at the same index
            if divided_list[i][index] is substr[index]: 
                scores[i] += 0
            #if two letters are correct but just swapped, the algorithm swaps them back.
            elif index < len(divided_list[i]) - 1 and substr[index + 1] is divided_list[i][index] and divided_list[i][index + 1] is substr[index]:
                divided_listl = list(divided_list[i])
                divided_listl[index + 1], divided_listl[index] = divided_listl[index], divided_listl[index + 1]
                divided_list[i] = ''.join(divided_listl)
                scores[i] += 10
            #if a letter is out of place, letter insertions/deletions are performed.
            elif substr[index + 1] in divided_list[i][index:index+search_dist+1]:
                next_letter_index = divided_list[i][index:index+search_dist+1].index(substr[index + 1]) + index
                #case of a one letter off 
                if next_letter_index < index + 1:
                    divided_listl = list(divided_list[i])
                    divided_listl.insert(index,substr[index])
                    divided_list[i] = ''.join(divided_listl)
                    scores[i] += 15
                #case where there are multiple letters on the index
                elif next_letter_index >= index + 1:
                    divided_list[i] = divided_list[i].replace(divided_list[i][index:next_letter_index],substr[index])
                    scores[i] += 10 + 3**((next_letter_index - (index + 1)) + 1)

            else: #if word does not match, and is not one over within a margin of 3
                #likely indicates that the current and next letter are off, so the word needs to check
                #the following letter to see if it is correct
                divided_listl = list(divided_list[i])
                divided_listl.insert(index,substr[index])
                divided_list[i] = ''.join(divided_listl)
                scores[i] += 35
        except IndexError:
            #string pattern length is smaller than the length of the substring
            divided_listl = list(divided_list[i])
            divided_listl.insert(index,substr[index])
            divided_list[i] = ''.join(divided_listl)
            scores[i] += 15
        
        #Once every word in dlistlen is checked, the scores of all elements are checked.  Any scores
        #that are reasonable are further checked, while poor scores are thrown out.
        if i is div_list_len-1:
            return search_highest_match(scores, substr, threshold, divided_list, rating, index)  

        
        #This is the end condition where no possible matches are found.  Happens in extreme cases where
        #the string pattern is very small in length (e.x. 2 characters).
        if i == div_list_len and index == len(substr):
            return {None: 0}
        
def search_highest_match(scores, substr, threshold, divided_list, rating, index):
    #checks uncertainty of the word
    for idx, score in enumerate(scores):
        #if it is bad, then you throw the word out from the dividedlist
        if score > len(substr)*10:
            divided_list.pop(idx)
            scores.pop(idx)
        if score < threshold:
            #check accuracy should return a dictionary with the 'word' and its accuracy
            #add the dictionary to the dictionary rating
            dict_result = check_accuracy(divided_list[idx], substr, index + 1, score)
            if rating:
                max_word = max(rating, key=(lambda key: rating[key]))
                max_score = rating[max_word]
                for k,v in dict_result.items():
                    if v > max_score:
                        rating.update(dict_result)
            else:
                rating.update(dict_result)
            #sort the dictionary by highest rating its size is > 1
            #return the highest value from the dictionary
    if rating:
        word = max(rating, key=(lambda key: rating[key]))
        scre = rating[word]
        return {word:scre}
    
    #If there are no more possible matches, the algorithm knows that partitions at this letter have
    #no correct matches.
    if not divided_list:
        return {None: 0}
    
    #If there a no satisfactory scores, the algorithm repeats at the following index.
    return check_list(divided_list, substr, index + 1, scores)
    

#This performs a similar function to checklist except it checks a single element against the substring.  
#This is used when the algorithm is fairly certain there may be a match, and will return a rating from
#0-100 depending on the accuracy.  See the checklist function for greater detail on how this function operates.
def check_accuracy(words, substr, index, score):
    
    for i in range(index, len(substr)):
        try:
            search_dist = 3
            #if there is no direct letter match at the same index
            if words[i] is substr[i]: 
                #score add 0 
                score += 0
            elif i < len(words) - 1 and substr[i + 1] is words[i] and words[i + 1] is substr[i]:
                words_list = list(words)
                words_list[i + 1], words_list[i] = words_list[i], words_list[i + 1]
                words = ''.join(words_list)
                score += 10
            elif substr[i + 1] in words[i:i+search_dist+1]:
                next_letter_index = words[i:i+search_dist+1].index(substr[i + 1]) + i
                #case of a one letter off 
                if next_letter_index < i + 1:
                    words_list = list(words)
                    words_list.insert(index,substr[i])
                    words = ''.join(words_list)
                    score += 15
                #case where there are multiple letters on the index
                elif next_letter_index >= i + 1:
                    words = words.replace(words[i:next_letter_index],substr[i])
                    score += 10 + 3**((next_letter_index - (i + 1)) + 1)

            else:
                words_list = list(words)
                words_list.insert(i,substr[i])
                words = ''.join(words_list)
                score += 35
        except IndexError:
            #this means that the word is 1 letter shorter than the substring, and it hits an index error
            words_list = list(words)
            words_list.insert(i,substr[i])
            words = ''.join(words_list)
            score += 15

    rating = 100*(1 - score/(len(substr)*20))
    #Now the matching string needs to be found
    matcher = words[0:len(substr)]
    return {matcher:rating}

#compare('A secondary fnctin comparescore can be used to exclusively retrieve the likeliness between two strings.', 'function')
#print(score('A secondary fnctin comparescore can be used to exclusively retrieve the likeliness between two strings.', 'function'))
