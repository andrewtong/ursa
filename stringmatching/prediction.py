import re

def compare(main, substring):
    #assume substring is of only alphabet letters
    main = filter(main)
    for k in range(0, len(substring)):
        dividedlist = divlist(main, substring[k])
        scores = [k]*len(dividedlist)
        result = checklist(dividedlist, substring, k, scores)
        for k,v in result.items():
            if k is not None:
                if int(v) > 20:
                    print('Found ' + k + ' to match with ' + substring + ' with a likeliness of ' + str(int(v)) + '.')
            else:
                print('No matches were found to match ' + substring + ' with reasonable certainty.')            

def filter(str):
    words = re.sub(r'[^\w\s]','',str) #Remove all punctuation
    words.replace(' ','') #Removes spaces between words
    words.lower() #Turn all capital letters to lower letters

    return words

#divlist will return a list with all sets of words that start with delimiter 'delim'
def divlist(strg, delim): #assume string is already filtered
    splitlist = []
    dividedlist = []
    for ch in strg:
        if ch not in delim:
            splitlist.append(ch)
        else:
            if splitlist:
                if splitlist[0] == delim:
                    dividedlist.append(''.join(splitlist))
            splitlist = []
            splitlist.append(ch)
    if splitlist:
        dividedlist.append(''.join(splitlist))
    return dividedlist

def checklist(dividedlist, substr, index, scores):
    rating = {}
    dlistlen = len(dividedlist)
    #[obj, obj, obj, obj]
    #[ s1, s2 , s3 , s4 ]

    #check if ea word is possibly the word
    for i in range(0,dlistlen):
        if index >= len(substr)/2:
            threshold = (len(substr) - index)*2
        else:
            threshold = 0;
        try:
            if dividedlist[i][index] is substr[index]: #if word matches
                #score add 0 
                scores[i] += 0
            elif dividedlist[i][index] is substr[index + 1]: #if word is next one over (sorted off)
                #score add 1
                scores[i] += 1
                #swap such that the letters are correct
                dividedlist[i][index],dividedlist[i][index + 1] = dividedlist[i][index + 1],dividedlist[i][index]
            else: #if word does not match, and is not one over
                #score add 2
                scores[i] += 2
        except IndexError:
            #index error, you just add 2, since the letter does not match anyways
            scores[i] += 2
        
        if i is dlistlen-1:   
            removed = 0 
            #check uncertainty of the word
            for idx, score in enumerate(scores):
                #if it is bad, then you throw the word out from the dividedlist
                if score > len(substr):
                    dividedlist.pop(idx)
                    scores.pop(idx)
                    removed += 1
                if score < threshold:
                    #check accuracy should return a dictionary with the 'word' and its accuracy
                    #add the dictionary to the dictionary rating
                    rating.update(checkaccuracy(dividedlist[idx], substr, index, score))
                
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
            if words[i] is substr[i]: #if word matches
                #score add 0 
                score += 0
            elif words[i] is substr[i+1]: #if word is next one over (sorted off)
                #score add 1
                score += 1
                #swap such that the letters are correct
                words[i], words[i + 1] = substr[i+1], substr[i]
            else: #if word does not match, and is not one over
                #score add 2
                score += 2
        except IndexError:
            #index error, you just add 2, since the letter does not match anyways
            score += 2
    #max score = len(substr)*2
    #score can be from 0 to len(substr)*2
    #Get the rating that ranges from 0-100
    rating = 100*(1 - score/(len(substr)*2))
    
    #Now the matching string needs to be found
    matcher = words[0:len(substr)]
    return {matcher:rating}
