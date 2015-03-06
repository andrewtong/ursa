# ursa v1.0 - currently a work in progress

##**Theory**
The concept of ursa is to perform fast fuzzy string matches by applying approximation techniques to minimize the time 
complexity associated with the algorithm.  The concept behind this is simple, but the precision of this program varies with 
how the algorithm numerically "rationalizes" to determine whether a two words are potential matches.  The encompassing theory
behind this is

**The likelihood of any pair of words matching exponentially decreases with increasing number of differences between the said
two words.**  

Understanding this concept proposes a number of implications that can incredibly expedite fuzzy string matches.  For example,
assume a user is attempting to check if the substring 'computer' is contained within the sentence 'My computer is new.'.  

As the substring 'computer' becomes increasingly mispelled,

- Colputer : This can be easily assumed as a mispelling of 'computer'.
- Colkuter
- Colkwter : This is increasingly difficult to determine that the original intent of the word was to be 'computer'
- Colkwber
- Colkwbmr : This is almost impossible to determine that the original intent of the word was to be 'computer'.

the substring eventually hits a threshold where it becomes so deformed that is is no longer recognizable from the original 
word. This threshold is noticable once a word differs from another by approximately 50% of its letters.  

##**So what are the consequences of this?**
Traditional string matches perform a computation of the Levenshtein distance to determine the proximity between two given 
words.  For a string pattern of length 'm' and a substring of length 'n', the time complexity of the Levenshtein distance
is O(mn).  However, applying the 50% error soft cap as previously shown approximately reduces the time complexity to O(mn/2),
which may make a significant difference in realistic scenarios.  

However, it is possible to further optimize this by removing words that are deemed incorrect.  Ursa is designed to initially
perform fast operations to weed out words that are certainly incorrect in order to reduce the string pattern that needs to be
scanned.  If it does find a potential match, it will then perform a more accurate check to determine whether the substring
is a true match.

##**Performance**
The following demonstrates how ursa is to operate for a string pattern and a given substring.

String pattern: 'The red apple is ripe and steady.'

Substring: 'ready'

The program will notice that there are two words that start with 'r'
- The **r**ed apple is **r**ipe and steady.
So there are two potential matches, but no certain matches, so we move to the next substring indexes
- The **re**d apple is **r**ipe and steady.
So 'red' appears to be a match, and will be analyzed to check whether it is a match.  The software will realize that 'red' is
too poor of a match, and decide to remove it.  'ripe' on the other hand, will not be analyzed since it will be marked as a 
poor matches once it the next indexes are matched.  Because of this, 'red' and 'ripe' will be removed and the string pattern
will be 
- 'The apple is and steady.'
Because of this, we scan the next substring index 'e' in the main pattern
- 'The apple is and st**e**ady.'
Following a similar process, the program will notice that 'eady' is a good match to 'ready', but with one letter off.  It 
will return this as a match but with an imperfect, but high score.

Note that if 'steady' was never in the string pattern, if no solid match was found after the substring index 'a', then the
program will stop searching since it exceeds the 50% error threshold there is an extremely high chance that there will be no
matches between the substring and the string pattern.


