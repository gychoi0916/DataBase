from konlpy.tag import Mecab 
from pymongo import MongoClient 

stop_word = dict()
DBname = "db20141591"
conn = MongoClient('localhost')
db = conn[DBname]
db.authenticate(DBname,DBname)

def make_stop_word():
    f = open('wordList.txt','r')
    while True:
        line = f.readline()
        if not line:
            break
        stop_word[line.strip()] = True
    f.close()
def p0():
    """
    TODO:
    CopyData news to news_freq
    """
    col1 = db['news']
    col2 = db['news_freq']

    col2.drop()

    for doc in col1.find():
        contentDic = dict()
        for key in doc.keys():
            if key != "_id":
                contentDic[key] = doc[key]
        col2.insert(contentDic)
def p1():
    """
    TODO:
    Morph news and update news
    """
    for doc in db['news_freq'].find():
        doc['morph'] = morphing(doc['content'])
        db['news_freq'].update({"_id": doc['_id']},doc)
    
def morphing(content):
    mecab = Mecab()
    morphList = []
    for word in mecab.nouns(content):
        if word not in stop_word:
            morphList.append(word)
    return morphList
def p2():
    """
    TODO:
    output: news morphs of db.news_freq.findOne()
    """
    pass
def p3():
    col1 = db['news_freq']
    col2 = db['news_wordset']
    col2.drop()
    for doc in col1.find():
        new_doc = dict()
        new_set = set()
        for w in doc['morph']:
            new_set.add(w)
        new_doc['word_set'] = list(new_set)
        new_doc['news_freq_id'] = doc['_id']
        col2.insert(new_doc)

def p4():
    """
    TODO:
    output: news wordset of db.news_wordset.findOne()
    """
    pass
def p5(length):
    """
    TODO:
    make frequent item_set
    and insert new collection (candidate_L +"length")
    ex) 1-th frequent item set collection name = candidate_L1
    """
    pass

def p6(length):
    """
    TODO:
    make strong association rule
    and print all of strong rules
    by length-th frequent item set
    """
    pass
def printMenu():
    print("0. CopyData")
    print("1. Morph")
    print("2. print morphs")
    print("3. print wordset")
    print("4. frequent item set")
    print("5. association rule")

if __name__ == "__main__":
    make_stop_word()
    printMenu()
    selector = int(input())
    if selector == 0:
        p0()
    elif selector == 1:
        p1()
        p3()
    elif selector == 2:
        p2()
    elif selector == 3:
        p4()
    elif selector == 4:
        print("input length of the frequent item:")
        length = int(input())
        p5(length)
    elif selector == 5:
        print("input length of the frequent item:")
        length = int(input())
        p6(length)

