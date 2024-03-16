import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    if len(corpus[page]) == 0:
        return dict.fromkeys(corpus.keys(), 1/len(corpus))
    else:
        A = dict.fromkeys(corpus.keys(), (1-damping_factor)/len(corpus))
        for x in corpus[page]:
            A[x] += damping_factor/len(corpus[page])
        return A


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    pagerank = dict.fromkeys(corpus, 0)
    nextpage = random.choice(list(corpus.keys()))
    pagerank[nextpage] += 1
    for i in range(n-1):
        A = transition_model(corpus, nextpage, damping_factor)
        x = random.uniform(0, 1)
        sump = 0
        page = 0
        for page in A:
            sump += A[page]
            if sump > x:
                break
        nextpage = page
        pagerank[page] += 1
    for page in pagerank:
        pagerank[page] /= n
    print(f"sample check : {sum(pagerank.values())}")
    return pagerank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n = len(corpus)
    pagerank = dict.fromkeys(corpus.keys(), 1/n)
    numlinks = {p:len(corpus[p]) for p in corpus}

    flag = True
    while flag:
        flag = False
        newrank = {}
        sump = 0
        for p in pagerank:
            newrank[p] = 1.0 * (1 - damping_factor) / n
        for p in pagerank:
            for v in corpus[p]:
                newrank[v] += 1.0 * damping_factor * pagerank[p] / numlinks[p]
            if numlinks[p] == 0:
                sump += damping_factor * pagerank[p]
        for p in pagerank:
            newrank[p] += sump / n
        for p in pagerank:
            if abs(newrank[p] - pagerank[p]) > 1e-3:
                flag = True
                break
        pagerank = newrank
    print(f"smaple check {sum(pagerank.values())}")
    return pagerank


if __name__ == "__main__":
    main()
