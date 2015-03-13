from re import sub

def compare(main, substring):
    #assume substring is of only alphabet letters
    main = filterstringpattern(main)
    for k in range(0, len(substring)):
        dividedlist = divlist(main, substring[k], len(substring))
        scores = [k*10]*len(dividedlist)
        result = checklist(dividedlist, substring[k:], k, scores)
        for key,v in result.items():
            if key is not None:
                if int(v) > 20:
                    print('Match found to ' + substring + ' with a certainty of ' + str(int(v)) + ', reconstructed word is ' + substring[:k] + key +'.')
                    return
        #yes I know this looks bad, but currently there are more important issues
        if k > int(len(substring)/2):
            print('No matches were found to match ' + substring + ' with reasonable certainty.')
            return     
        
       

def filterstringpattern(strg):
    words = sub(r'[^\w\s]','',strg) #Remove all punctuation
    words = words.replace(' ','') #Removes spaces between words
    words = words.lower()  #Turn all capital letters to lower letters
    return words

#divlist will return a list with all sets of words that start with delimiter 'delim'
def divlist(strg, delim, sslen): #assume string is already filtered
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

def checklist(dividedlist, substr, index, scores):
    rating = {}
    dlistlen = len(dividedlist)
    #[obj, obj, obj, obj]
    #[ s1, s2 , s3 , s4 ]

    #check if each word is possibly the word
    for i in range(0,dlistlen):
        if index >= len(substr)/2:
            threshold = (len(substr) - index)*20
        else:
            threshold = 0;

        try:
            searchdist = min(3, len(substr)-index) #may have to change 3 to something else
            #if there is no direct letter match at the same index
            if dividedlist[i][index] is substr[index]: 
                #score add 0 
                scores[i] += 0
            elif index < len(dividedlist[i]) - 1 and substr[index + 1] is dividedlist[i][index] and dividedlist[i][index + 1] is substr[index]:
                dividedlistl = list(dividedlist[i])
                dividedlistl[index + 1], dividedlistl[index] = dividedlistl[index], dividedlistl[index + 1]
                dividedlist[i] = ''.join(dividedlistl)
                scores[i] += 10
            elif substr[index + 1] in dividedlist[i][index:index+searchdist]:
                nextletterindex = dividedlist[i][index:index+searchdist].index(substr[index + 1]) + index
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
        
        if i is dlistlen-1:  
            #check uncertainty of the word
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
            
            #if list is empty -> no matches found, then return
            if not dividedlist:
                return {None: 0}
                #-1 will indicate that there are no matches
            
            return checklist(dividedlist, substr, index + 1, scores)
        
        if i == dlistlen and index == len(substr):
            return {None: 0}

    
def checkaccuracy(words, substr, index, score):
    #get a score from 0-100 then return it given the current index and score
    
    for i in range(index, len(substr)):
        try:
            searchdist = min(3, len(substr) - 1)#may have to change 3 to something else
            #if there is no direct letter match at the same index
            if words[i] is substr[i]: 
                #score add 0 
                score += 0
            elif i < len(words) - 1 and substr[i + 1] is words[i] and words[i + 1] is substr[i]:
                wordsl = list(words)
                wordsl[i + 1], wordsl[i] = wordsl[i], wordsl[i + 1]
                words = ''.join(wordsl)
                score += 10
            elif substr[i + 1] in words[i:i+searchdist]:
                nextletterindex = words[i:i+searchdist].index(substr[i + 1]) + i
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

