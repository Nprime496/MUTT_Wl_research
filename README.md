
# MUTT
[Metrics Unit TesTing (MUTT)](https://www.aclweb.org/anthology/P16-1182/) for machine translation and other similarity metrics.

"To design better metrics, we need a principled approach to evaluating their performance. Historically, MT metrics have been evaluated by how well they correlate with human annotations ([Callison-Burch et al., 2010](https://www.aclweb.org/anthology/E06-1032/); [Machacek and Bojar, 2014](https://ufal.mff.cuni.cz/pbml/103/art-machacek-bojar.pdf). However, as we demonstrate in Sec. 5, human judgment can result in inconsistent scoring. This presents a serious problem for determining whether a metric is ”good” based on correlation with inconsistent human scores. When ”gold” target data is
unreliable, even good metrics can appear to be inaccurate. Furthermore, correlation of system output with human-derived scores typically provides an overall
score but fails to isolate specific errors that metrics tend to miss. This makes it difficult to discover system-specific weaknesses to improve their
performance. For instance, an ngram-based metric might effectively detect non-fluent, syntactic errors, but could also be fooled by legitimate paraphrases whose ngrams simply did not appear in the training set.

The goal of this paper (thus this repo) is to propose a process for consistent and informative automated analysis of evaluation metrics. This method is demonstrably more consistent and interpretable than correlation with human annotations. In addition, we extend the SICK dataset to include un-scored fluency-focused sentence comparisons and we propose a toy metric for evaluation."


### Edit
This version of MUTT tends to provide means to evaluate any metric on the same datase as the [paper](https://www.aclweb.org/anthology/P16-1182/) through the `evaluate_mutt` API

### Dependencies:
- python (3.*)


### Run :
To just evaluate metric, you have to clone the repo:

`git clone https://github.com/Nprime496/MUTT_Wl_research.git`
`cd MUTT_Wl_research/src`

You have to define your function which will be used to compare two sentences.
For example, for BERTScore
```
from bert_score import BERTScorer
scorer=BERTSCorer(...)

def evaluate_BERTScore_two_sentences(sent_a,sent_b):
  #computes F1-Score
  return scorer.score([sent_a],[sent_b])[2]
```
Then, you run the API using `evaluate_mutt`

```
from mutt_ import evaluate_mutt
evaluate_mutt([("<name of your model>",<function taking two sentences as input and returning a float value of the score>),...])
```
For our example (with BERTScore) , it will be

```
from mutt_ import evaluate_mutt
evaluate_mutt([("BERTScore",evaluate_BERTScore_two_sentences)])
```

