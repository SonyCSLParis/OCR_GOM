from Bio import pairwise2

#https://github.com/microsoft/genalog/

MATCH_REWARD = 1
GAP_PENALTY = -0.5
GAP_EXT_PENALTY = -0.5
MISMATCH_PENALTY = -0.5
GAP_CHAR = "@"
ONE_ALIGNMENT_ONLY = False
SPACE_MISMATCH_PENALTY = 0.1

def _join_char_list(alignment_tuple):
    """ Post-process alignment results for unicode support """
    gt_char_list, noise_char_list, score, start, end = alignment_tuple
    return "".join(gt_char_list), "".join(noise_char_list), score, start, end

def match_reward_fn(x, y):
    if x == y:
        return MATCH_REWARD
    elif x == " " or y == " ":
        # mismatch of a character with a space get a stronger penalty
        return MISMATCH_PENALTY - SPACE_MISMATCH_PENALTY
    else:
        return MISMATCH_PENALTY

"""
def select_alignment_candidates(alignments, target_num_gt_tokens):
   for alignment in alignments:
      if len(alignment[0].split()) == target_num_gt_tokens:
         if len(alignment[0]) != len(alignment[1]):
            raise ValueError(f"Aligned strings are not equal in length: \naligned_gt: '{aligned_gt}'\naligned_noise '{aligned_noise}'\n")
            return alignment
   raise ValueError(f"No alignment candidates with {target_num_gt_tokens} tokens. Total candidates: {len(alignments)}")
"""

gt = open("kraken_data/ground_truth_30_39.txt").read()
noise = open("kraken_data/sample_30_39.txt").read()

alignments = pairwise2.align.globalcs(list(gt), list(noise),match_reward_fn, GAP_PENALTY, GAP_EXT_PENALTY, gap_char=[GAP_CHAR], one_alignment_only=ONE_ALIGNMENT_ONLY,)
alignments = list(map(_join_char_list, alignments))

n_toks_gt = len(gt.split())

alignment = select_alignment_candidates(alignments, n_toks_gt)