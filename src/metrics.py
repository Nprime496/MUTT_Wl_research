"""                                                                              
 Text-Machine Lab: MUTT  

 File Name : metrics.py
                                                                              
 Creation Date : 17-02-2016
                                                                              
 Created By : Renan Campos                                               
                                                                              
 Purpose : Script containing wrappers to use various MT metrics suites.

"""
import json
import tqdm
import os
import sys
import numpy as np


import re
from subprocess import check_output, CalledProcessError, STDOUT

def getstatusoutput(cmd):
    try:
        data = check_output(cmd, shell=True, universal_newlines=True, stderr=STDOUT)
        status = 0
    except CalledProcessError as ex:
        data = ex.output
        status = ex.returncode
    if data[-1:] == '\n':
        data = data[:-1]
    return status, data

METRICS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'metrics')

#
# coco-caption
#
# Add modules to path to make importing easy here:
sys.path.append(os.path.join(METRICS_DIR, 'coco-caption'))


from pycocotools.coco import COCO
from pycocoevalcap.eval import COCOEvalCap

# The set of meaning preserving corruptions
m_p = set(['det_sub', 'near_syms', 'passive'])

def coco(sent_a, sent_b, ref_5, ref_10, ref_20, corruption, f,metrics,showoff):
  """
    Runs the coco evaluation for each ref list and prints to the output file.
  """
  print(f,file=sys.stderr)
  print("Corruption:", corruption ,file=sys.stderr)
  all_ref=[ref_5,ref_10,ref_20]

  for metric in metrics:
    coco_results= [coco_accuracy(sent_a, sent_b, ref_5, corruption in m_p,metric,showoff),
                 coco_accuracy(sent_a, sent_b, ref_10, corruption in m_p,metric,showoff),
                 coco_accuracy(sent_a, sent_b, ref_20, corruption in m_p,metric,showoff)]
    if showoff==True:
      continue
    print("\n#  References:     5   |    10   |    20")
    print( "-----------------------+---------+---------")
    print("   %10s: %0.1f | %0.1f | %0.1f" % (metric[0], 
                                               coco_results[0][metric[0]] * 100, 
                                               coco_results[1][metric[0]] * 100, 
                                               coco_results[2][metric[0]] * 100))
    print("-----------------------+---------+---------")
    print("")

def coco_accuracy(sent_a, sent_b, refs, near,metric_,showoff):
  """
    For the coco-caption metric 
    to extract the accuracy of all the metrics that were run.
  """
  res   = {}
  total = 0.0
  for a, b in zip(coco_eval(sent_a, refs,metric_,showoff), coco_eval(sent_b, refs,metric_,showoff)):
    for metric in a.keys():
      #print(" {}[{}]={} ".format(a,metric,a[metric]))
      #print(" {}[{}]={} ".format(b,metric,b[metric]))
      # Special case of meaning preserving corruptions j
      if near:
        # Adding .1 to everything to avoid divide by zero error
        per_diff = abs((a[metric] - b[metric]) / float(a[metric] + 1e-9)) * 100
        # 15 % threshold
        if per_diff <= 15:
          try:
            res[metric] += 1
          except:
            res[metric]  = 1
      elif a[metric] > b[metric]:
        try:
          res[metric] += 1
        except:
          res[metric]  = 1
    total += 1

  for metric in res.keys():
    res[metric] /= total
  return res

def load_mdata_eval(candidates_file):
  print("mdata :: ",candidates_file,file=sys.stderr)
  with open(candidates_file, "r") as f:
    f=json.load(f)
    annotations=f["annotations"]
  return annotations

def load_rdata_eval(candidates_file):
  print("rdata :: ",candidates_file,file=sys.stderr)
  with open(candidates_file, "r") as f:
    f=json.load(f)
    annotations=f
  return annotations


def micro_eval(candidates_file, references_file,metric,showoff=False,num=5):

  annotations,corruptions=load_mdata_eval(references_file),load_rdata_eval(candidates_file)
  annotations,corruptions=annotations[:num],corruptions[:num]
  for corr in corruptions:
    l=[]
    result={}
    result['image_id']=corr['image_id']
    while(i<len(annotations) and annotations[i]['image_id']==corr['image_id']):
      r=float(metric[1](annotations[i]['caption'],corr['caption']))
      l.append(r)
      print(" %50s | %50s | %0.1f" % (annotations[i]['caption'],corr['caption'],r))
      i+=1
    result[metric[0]]=np.mean(l)
    output.append(result)

def coco_eval(candidates_file, references_file,metric,showoff=False,num=5):
  """
    Given the candidates and references, the coco-caption module is 
    used to calculate various metrics. Returns a list of dictionaries containing:
    -BLEU
    -ROUGE
    -METEOR
    -CIDEr
  """

  # This is used to suppress the output of coco-eval:
  old_stdout = sys.stdout
  sys.stdout = open(os.devnull, "w")
  if showoff==True:
    return micro_eval(candidates_file, references_file,metric,num)

  try:
    result={}
    annotations,corruptions=load_data_eval(candidates_file),load_data_eval(references_file)
    i=0
    output=[]
    for corr in tqdm.tqdm(corruptions):
      l=[]
      result={}
      result['image_id']=corr['image_id']
      while(i<len(annotations) and annotations[i]['image_id']==corr['image_id']): 
        l.append(float(metric[1](annotations[i]['caption'],corr['caption'])))
        i+=1
      result[metric[0]]=np.mean(l)
      output.append(result)
  finally:
    # Change back to standard output
    sys.stdout.close()
    sys.stdout = old_stdout
  return output#cocoEval.evalImgs

#
# badger
#
def badger(sent_a, sent_b, ref_5, ref_10, ref_20, corruption, f):
  """
    Runs the badger evaluation for each ref list and prints to the output file.
  """

  print()
  print(f, "Corruption:", corruption,file=sys.stderr)
  print(f, "#  References:     5   |    10   |    20",file=sys.stderr)
  print(f, "-----------------------+---------+---------",file=sys.stderr)
  print(f, "   %10s: %0.1f | %0.1f | %0.1f" % ('badger',
                                                 badger_accuracy(sent_a, sent_b, ref_5, corruption in m_p) * 100, 
                                                 badger_accuracy(sent_a, sent_b, ref_10, corruption in m_p) * 100, 
                                                 badger_accuracy(sent_a, sent_b, ref_20, corruption in m_p) * 100),file=sys.stderr)
  print(f, "-----------------------+---------+---------",file=sys.stderr)
  print(f, "",file=sys.stderr)

def badger_accuracy(sent_a, sent_b, refs, near):
  """
    Calculates the accuracy for the badger metric.
  """

  count = 0.0
  total = 0.0
  for a,b in zip(badger_eval(sent_a, refs), badger_eval(sent_b, refs)):
    # Special case of meaning preserving corruptions
    if near:
      per_diff = abs((a - b) / float(a+1e-9)) * 100
      # 15 % threshold
      if per_diff <= 15:
        count += 1
    elif a > b:
      count += 1
    total += 1
  return count / total


def badger_eval(cand_file, ref_file):
  """
    Runs badger and extracts a list of scores.
  """
  out_dir = os.path.join(METRICS_DIR, 'badger', 'willie', 'out')
  exec_file = os.path.join(METRICS_DIR, 'badger', 'badger.jar')
  cmd = 'java -jar %s -r %s -t %s -o %s' % (exec_file, ref_file,cand_file,out_dir)
  status,output = getstatusoutput(cmd)
  
  # assert badger worked correctly
  check = 'Scoring \w+ doc example_set::doc1 seg (\d+) (\d+) references found'
  matches = re.findall(check, output)
#  for match in matches:
#      if match[1] != '1':
#          ind = int(match[0])
#          print ind
#          exit()


  # parse results
  metric_scores = []
  res_file = '%s/SmithWatermanGotohWindowedAffine/Badger-seg.scr' % out_dir
  with open(res_file, 'r') as f:
      for line in f.readlines():
          toks = line.strip().split('\t')
          score = float(toks[-1])
          metric_scores.append(score)

  return metric_scores
#
# nist
#
def nist(sent_a, sent_b, ref_5, ref_10, ref_20, corruption, f):
  """
    Runs the badger evaluation for each ref list and prints to the output file.
  """

  print()
  print(f, "Corruption:", corruption,file=sys.stderr)
  print(f, "#  References:     5   |    10   |    20",file=sys.stderr)
  print(f, "-----------------------+---------+---------",file=sys.stderr)
  print(f, "   %10s: %0.5f | %0.5f | %0.5f" % ('nist',
                                                 badger_accuracy(sent_a, sent_b, ref_5), 
                                                 badger_accuracy(sent_a, sent_b, ref_10), 
                                                 badger_accuracy(sent_a, sent_b, ref_20)),file=sys.stderr)
  print(f, "-----------------------+---------+---------",file=sys.stderr)
  print(f, "",file=sys.stderr)

def nist_accuracy(sent_a, sent_b, refs):
  """
    Calculates the accuracy for the nist metric.
  """

  count = 0.0
  total = 0.0
  for a,b in zip(nist_eval(sent_a, refs), badger_eval(sent_b, refs)):
    if a > b:
      count += 1
    total += 1
  return count / total


def nist_eval(cand_file, ref_file):
  """
    Runs nist and extracts a list of scores for bleu and nist.
  """

  exec_file = os.path.join(METRICS_DIR, 'nist', 'mteval-v13a.pl')
  # invoke nist
  cmd = 'perl mteval-v13a.pl -r %s -s %s -t %s' % (exec_file, ref_file,src_file,tst_file)
  status,output = getstatusoutput(cmd)

  # parse results
  sections = output.split('# ' + '-'*72)

  nist_reg = 'NIST:  (\d\.\d+)   (\d\.\d+)   (\d\.\d+)   (\d\.\d+)   (\d\.\d+)'
  nist_match = re.search(nist_reg, sections[1])
  nist_scores = map(float, nist_match.groups())

  bleu_reg = 'BLEU:  (\d\.\d+)   (\d\.\d+)   (\d\.\d+)   (\d\.\d+)   (\d\.\d+)'
  bleu_match = re.search(bleu_reg, sections[1])
  bleu_scores = map(float, bleu_match.groups())

  return nist_scores, bleu_scores

#
# terp
#
def terp(sent_a, sent_b, ref_5, ref_10, ref_20, corruption, f):
  """
    Runs the terp evaluation for each ref list and prints to the output file.
  """

  print(f, "Corruption:", corruption,file=sys.stderr)
  print(f, "#  References:     5   |    10   |    20",file=sys.stderr)
  print(f, "-----------------------+---------+---------",file=sys.stderr)
  print(f, "   %10s: %0.1f | %0.1f | %0.1f" % ('terp',
                                                 terp_accuracy(sent_a, sent_b, ref_5,  corruption in m_p) * 100, 
                                                 terp_accuracy(sent_a, sent_b, ref_10, corruption in m_p) * 100, 
                                                 terp_accuracy(sent_a, sent_b, ref_20, corruption in m_p) * 100),file=sys.stderr)
  print(f, "-----------------------+---------+---------",file=sys.stderr)
  print(f, "",file=sys.stderr)

def terp_accuracy(sent_a, sent_b, refs, near):
  """
    Calculates the accuracy for the nist metric.
  """

  count = 0.0
  total = 0.0
  for a,b in zip(terp_eval(sent_a, refs), terp_eval(sent_b, refs)):
    # Special case of meaning preserving corruptions
    if near:
      per_diff = abs((a - b) / float(a+1e-9)) * 100
      # 15 % threshold
      if per_diff <= 15:
        count += 1
    # note: terp gives a higher score to the worst candidate
    elif a < b:
      count += 1
    total += 1
  return count / total


def terp_eval(cand_file, ref_file):
  """
    Runs terp and extracts a list of scores for bleu and nist.
  """

  param_file = os.path.join(METRICS_DIR, 'terp', 'willie', 'params.param')
  res_file   = cand_file
  phrase_db = os.path.join(METRICS_DIR, 'terp', 'data', 'phrases.db')
  with open(param_file, 'w') as f:
      print(f, 'Phrase Database (filename)               : ' + phrase_db,file=sys.stderr)
      print(f, 'Reference File (filename)                : ' + ref_file,file=sys.stderr)
      print(f, 'Hypothesis File (filename)               : ' + cand_file,file=sys.stderr)
      print(f, 'Output Formats (list)                    : param nist pra',file=sys.stderr)
      print(f, 'Output Prefix (filename)                 : ' + res_file,file=sys.stderr)

  terpa = os.path.join(METRICS_DIR, 'terp', 'bin', 'terpa')

  # invoke terp
  cmd = '%s %s' % (terpa,param_file)
  status,output = getstatusoutput(cmd)

  # parse results
  scores = list()
  with open(res_file + '.seg.scr', 'r') as f:
    for line in f:
      scores.append(float(line.split()[3]))

  return scores


