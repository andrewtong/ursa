# ursa v3.1
URSA is now functional for usage!

##**Theory**
The concept of ursa is to perform fast fuzzy string matches by applying approximation techniques to minimize the time 
complexity associated with the algorithm.  The concept behind this is simple, but the precision of this program varies with 
how the algorithm numerically "rationalizes" to determine whether a two words are potential matches.  The encompassing theory
behind this is

*The likelihood of any pair of words matching exponentially decreases with an increasing number of differences between the 
said two words.* 

Understanding this concept proposes a number of implications that can incredibly expedite fuzzy string matches.  From a 
series of tests, I have determined that there is approximately a 50% difference threshold between letters within 
two words such that the said two words are indistinguishable.

For example, the word 'distinguish' can be claimed to be unrecognizable from 'dustkngosh'.  URSA will attempt to 
reconstruct the substring by predicting errors within the string pattern and comparing the sum of errors to a calculated
threshold.  **By applying this theory, I am able to compare words only knowing the length of the 'correct' word, since
incorrect words are filtered out beyond a determined score threshold.  The benefit of this is that I am able to apply
partioning methods at linear speeds (at the most optimal case) to significantly expedite runtime since the algorithm never
has to search for a sequence, circumventing the usage of sequence matching algorithms that run in polynomial time!.**

##**So what are the consequences of this?**
URSA is capable of running at fast speeds compared to various other string matching algorithms:
Note times and scores are computed as of the v2.0 patch! (current patch is v3.1, but results should vary minimally!)

```
%timeit compare('The quick brown fox jmuped over the lazy dog.','jumped')
1000 loops, best of 3: 307 μs per loop
```

```
%timeit compare('Performance varies minimally with the complexity of the input, despite the length of the string pattern.','complexity')
1000 loops, best of 3: 545 μs per loop
```

```
%timeit compare('Sally sells seashells down by the seaschore.','seashore')
1000 loops, best of 3: 758 μs per loop
```

```
%timeit compare('Sesahells are slod down by the seacshore by Slally.,'seashore')
1000 loops, best of 3: 597 μs per loop
```

These tests were done using IPython, and the takeaway from this is that runtime is *highly* dependent on the partioning!.
If you look at the 3rd and 4th tests, the 4th tests takes shorter because 'seashore' is partioned as the 3rd possibility
as opposed to the 4th.  Despite having multiple words that start with the same letter, URSA is capable of computing results
without significant increases in runtime.  

The algorithm is capable of handling extreme cases of fuzzy string matches like no other algorithm can:

```
compare('W o r d s can be s p a c e d by almost any amount with almost no peanlty','spaced')
Match found to spaced with a certainty of 100, reconstructed word is spaced.
```

```
compare('Ursa can handle cases where spam may be qwertyupresent.','present')
Match found to present with a certainty of 100, reconstructed word is present.
```

```
compare('Scenarios where letters may be misig are fine as well!','missing')
Match found to missing with a certainty of 78, reconstructed word is missing.
```

```
compare('Letters that are swpapde are no problem either.','swapped')
Match found to swapped with a certainty of 85, reconstructed word is swapped.
```

```
compare('Even the most complex of istkeas can be recognized by URSA.','mistakes')
Match found to mistakes with a certainty of 71, reconstructed word is mistakes.
```

Whether it may be an incorrect, swapped, missing letters or a combination of all, URSA is capable of solving fuzzy string
matches without issue, and scores approximately depending on the likeliness between the correctly and incorrectly spelled
word.

Of course, if you would like only the integer value to be returned from the algorithm, a secondary function 'score' can be 
used.  This is primarily useful if URSA is to function as a module.

```
score('A secondary fnctin comparescore can be used to exclusively retrieve the likeliness between two strings.', 'function')
88
```

##**Scoring System of URSA**
One of the main goals of URSA once it was functional was to adapt a scoring system that provides meaningful score values to 
user.  Scores should indicate a definitive yes or no and optimally minimize in the mid range zone.  I define the mid range
zone that encompasses scores between approximately 40-65, where there is no definitive answer as to whether the word is 
a true match or not.  Originally scores are computed on a linear based function, where for example, a 4 letter word with 
a single incorrect letter may receive a score between 75 to 85, depending on the severity of the error. In addition, scores 
that did not exceed a threshold were automatically deemed as incorrect.  The original threshold was at 20, but has been 
bumped up to 25 with the introduction of the new scoring system.

The graph below depicts how the new scoring system works.  The purpose of adjusted the score is to return an increased 
quantity of higher and lower scores while minimizing the quantity of 'mid-ranged' scores as previously discussed due to 
their ambiguous nature.

![ursascoringimg](https://cloud.githubusercontent.com/assets/10404525/6912202/72a095f0-d721-11e4-8d79-6dc73fc9e8d7.png)

##**What Can Be Improved on URSA**
While URSA has a plethora of benefits, it is still incredibly new and due to the numerous amount of fuzzy string cases
that may possibly exist, I am almost certain that URSA is still far from its optimal form.  That being said, here are a few
current issues with URSA that are seeking to be addressed in the future.

- Due to the partitioning method, it is incredibly difficult to remove words that have been previously searched.  A given
  substring may be spaced out across a sentence such that single word removal is not adequate for URSA's performance.
- Currently URSA does not support multiple word input, or prefixes like 'not'/'un'/'im' that can easily change the meaning
  of a word.


