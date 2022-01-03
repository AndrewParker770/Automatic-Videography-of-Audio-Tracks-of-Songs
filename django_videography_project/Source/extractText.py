import yake
import sys

def returnKeyWords(text, numOfKeywords):
    
    #text_file = open(filename, "r")
    #lyrics = text_file.read()
    #text_file.close()
    
    language = "en"
    max_ngram_size = 1
    deduplication_thresold = 0.9
    deduplication_algo = 'seqm'
    windowSize = 2

    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(text)

    return keywords

if __name__ == "__main__":
    filename = sys.argv[1]
    returnKeyWords(filename)

    


