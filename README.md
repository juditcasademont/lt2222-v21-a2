# LT2222 V21 Assignment 2

Assignment 2 from the course LT2222 in the University of Gothenburg's winter 2021 semester.

Your name: Judit Casademont Moner (guscasaju)

*Answer all questions in the notebook here. You should also write whatever high-level documentation you feel you need to here.*

## Comments about decisions made throughout the code

**Part 1**
I chose to remove all punctuation because it might interfere at certain points in future functions.
I realized that, in order for verbs to be lemmatized properly, I had to specify it by using the pos tags.

**Part 2**
I decided to include words with entity type tags in the context. My reason is that, for example, if we have a sentence that says "Carl XVI Gustaf, king of Sweden (...)", I think Sweden is a relevant word that defines who Carl XVI Gustaf is. In the same way, Carl XVI Gustaf is part of the definition of Sweden as well.

**Part 3**
Just as a comment, I found out that by creating the DataFrame from lists of numbers (as I had done in assignment 1) would give me an error on the test_y[0] cell but, instead, if I built it from an empty DataFrame, it worked. However, depending on the method I used to rearrange the columns, that cell would give me an error anyways. I haven't been able to figure out why that happened yet, still a mystery.

**Part 5 COMMENT**
I would say that the results of both the training data and the test data are relatively bad, but I think the training data provides better prediction results. For some reason, both sets have the tendency to predict instances wrong in the same categories, 'eve', 'geo', 'gpe' and 'org'. It is possible that we might have more examples of these entity types in the corpus than of the others, so these tags get more contexts. In the same way, if some of the entity types have very few examples in the corpus, the algorithm will see a lot less examples of them and will be unable to identify them as easily.
My speculation is that my not very great results might have to do with my decision in part 2 of including words with entity types in the contexts. By not stopping the gathering of features when a new entity is found, contexts might overlap and get mixed up. So my guess is that, maybe, a named entity being part of the context of another named entity creates a "conflict of identity". Another reason for these results might be my decision of not removing filler words or words that are very common (such as 'a', 'the', 'this', 'that', 'what', etc.), since these words are so common that they can appear in any context, therefore making the task of learning a typical contexts for the named entities a very complicated task.
If I were to start the assignment all over again, I would for sure remove the named entities from the contexts of other named entities, as well as a collection of very common words.