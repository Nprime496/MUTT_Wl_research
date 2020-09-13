
# MUTT
[Metrics Unit TesTing (MUTT)](https://www.aclweb.org/anthology/P16-1182/) for machine translation and other similarity metrics.


### Edit
This version of MUTT tends to provide means to evaluate any metric on the same datase as the [paper](https://www.aclweb.org/anthology/P16-1182/) through the `evaluate_mutt` API

### Dependencies:
- python (3.*)

### Run
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

