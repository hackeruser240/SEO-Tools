import os
import sys
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
import random

from functions import get_wordnet_pos, replace_synonyms, rewrite_sentence, rewrite_article

if __name__ == "__main__": # This ensures the code only runs when the script is executed directly
    # --- Test rewrite_article ---
    print("--- Testing rewrite_article ---")
    sample_article = input("Enter your sentence: \n")
    #print(f"Original: {sample_article}")
    try:
        rewritten_article = rewrite_article(sample_article)
        print(f"\n Rewritten: {rewritten_article}")
    except Exception as e:
        print(f"Error rewriting article: {e}")


    print("-" * 30)