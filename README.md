# ursa v1.0 - currently a work in progress

##**Theory**
The concept of ursa is to perform fast fuzzy string matches by applying approximation techniques to minimize the time 
complexity associated with the algorithm.  The concept behind this is simple, but the precision of this program varies with 
how the algorithm numerically "rationalizes" to determine whether a two words are potential matches.  The encompassing theory
behind this is

**The likelihood of any pair of words matching exponentially decreases with increasing number of differences between the said
two words.**  

Understanding this concept proposes a number of implications that can incredibly expedite fuzzy string matches.  From a 
series of tests, I have determined that there is approximately a 50% difference threshold between letters within 
two words such that the said two words are indistinguishable.

For example, the word 'distinguish' can be claimed to be unrecognizable from 'dustkngosh'.  **By applying this theory, I am
able to compare words only knowing the length of the 'correct' word, since incorrect words reveal themselves beyond a 
determined score threshold.  The benefit of this is that I am able to apply partioning methods at linear speeds (at the
most optimal case) to significantly expedite runtime since the algorithm never has to search for a sequence, circumventing 
the usage of sequence matching algorithms that run in polynomial time!.**

##**So what are the consequences of this?**
URSA is capable of running at extreme speeds compared to various other string matching algorithms:
*ex to be shown*

The algorithm is capable of handling extreme cases of fuzzy string matches like no other algorithm can:
*second example*

URSA's scoring system is incredibly detailed, being lenient on words with minimal errors, while harsher on words with 
multiple errors, as opposed to the commonly seen linear scoring system.
*third example*

##**What Can Be Improved on URSA**
While URSA has a plethora of benefits, it is still incredibly new and due to the numerous amount of fuzzy string cases
that may possibly exist, I am almost certain that URSA is still at its most optimal form.  That being said, here are a few
current issues with URSA that are seeking to be addressed in the future.

- Due to the partitioning method, it is incredibly difficult to remove words that have been previously searched.  A given
  substring may be spaced out across a sentence such that single word removal is not adequate for URSA's performance.
- URSA's scoring system is not perfect.  While it is more punishing toward words that have a higher number of errors, 
  I am not positive whether the scoring system is at the current moment a matching pair with the score parsing algorithm.


