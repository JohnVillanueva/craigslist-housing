from bs4 import BeautifulSoup
import requests

source = requests.get('https://sfbay.craigslist.org/d/apartments-housing-for-rent/search/sfc/apa').text
soup = BeautifulSoup(source,'lxml')
neighborhood_html = soup.find('ul', class_="list").find_all('label')
sf_neighborhoods = [neighborhood.text.strip() for neighborhood in neighborhood_html]

 #-----------------------------------------------------------------------
    
from rapidfuzz.string_metric import levenshtein
from difflib import SequenceMatcher

def longestSubstringFinder(string1, string2):
    match = SequenceMatcher(None, string1.lower(), string2.lower()).find_longest_match(0, len(string1), 0, len(string2))
    return string1[match.a: match.a + match.size]

def Neighborhood_Relabel(nbhd, real_nbhds=sf_neighborhoods):
    
    if not isinstance(nbhd, str):
        return 'Other/Unlisted'
    
    if nbhd in real_nbhds:
        return nbhd
    
    lev_distances = []
    abs_lev_dists = []
    cmn_substr_len = []
    
    for sf_nbhd in real_nbhds:
        
        lev_dist = levenshtein(nbhd.lower(), sf_nbhd.lower())
        str_len_diff = abs(len(nbhd) - len(sf_nbhd))
        longest_substr = longestSubstringFinder(nbhd, sf_nbhd)
        
        lev_distances.append(lev_dist)
        abs_lev_dists.append(lev_dist - str_len_diff)
        cmn_substr_len.append(len(longest_substr))
    
    # Close Match Relabeling of Neighborhood Labels
    # Metric Cutoffs are best arbitrary approximation
    if min(lev_distances) == min(abs_lev_dists):
        index = lev_distances.index(min(abs_lev_dists))
        return real_nbhds[index]
    elif max(cmn_substr_len) >= 11:
        index = cmn_substr_len.index(max(cmn_substr_len))
        return real_nbhds[index]
    elif min(abs_lev_dists) == 0:
        index = lev_distances.index(min(lev_distances))
        return real_nbhds[index]
    else:
        return 'Other/Unlisted'