# NoteScript
## What it does?

UCLA spends a lot of money on hiring notetakers. To save the unnecessary spending, we created NoteScript to let technology handle the job of note taking.

## How it works?
Sends input text to Google NLP API for parsing sentence by sentence. Constructs a tree from the linguistic dependencies that the NLP API returns that places the subject noun at the root node, it's children being verbs and the children of the verb nodes being the objects that the verbs relate the subject to. 
These sentence level trees were then combined into a directed graph that starts at the most important noun and recursively creates add edges (verbs) and vertices (nouns) to it. 
The weights of the edges specify the relation between two nouns.
That is:
An edge going from Noun A to Noun B with weight 0 indicates:
    - Noun A is the subject 
    - Noun B is the object
    - Label of the edge is the verb
    - Noun A is more important to the text than Noun B

An edge going from Noun A to Noun B with weigh indicates: 
    - Noun A is the object
    - Noun B is the subject  
    - Label of the edge is the verb
    - Noun A is more important to the text than Noun B

The graph is then traversed to give the final output i.e. condensed notes of the input text.
The traversal starts at the first vertex of the graph (i.e. the vertex for the most important noun)
It then recursively prints out the verbs and nouns to give the desired output.
In cases where the weight of the edge is 0, the verb is printed first followed by the noun.
In cases where the weight of the edge is 1, the noun is printed first followed by the verb and a placeholder pronoun.
