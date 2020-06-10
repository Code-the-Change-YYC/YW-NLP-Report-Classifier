import spacy,re
import pandas as pd 
import numpy as np 
from spacy import displacy
from spacy.util import minibatch, compounding
from spacy.lang.en.stop_words import STOP_WORDS

import matplotlib.pyplot as plt 



#load the stystem
nlp = spacy.load('en_core_web_lg')

#load the csv file 
ywca_pd = pd.read_csv("data/data-processed.csv",encoding='iso-8859-1')

#save description columns
ywca_pd_dis_origin =[re.sub(r"\{\{[^\{\}]+\}\}\w?","someone",str1) for str1 in ywca_pd["DESCRIPTION"]]

clean_up_discription = [nlp(str1) for str1 in ywca_pd_dis_origin]

#get rid of stop words
ywca_pd_discription=[]
for doc in clean_up_discription:
    str1 = ' '.join([w.text for w in doc if not nlp.vocab[w.text].is_stop])
    ywca_pd_discription.append(str1)
    

# show we have 

print(ywca_pd_discription[:2])

#save INCIDENT_TYPE_1 for labels for logistic regression, classify any Medical emergency be 1 and  rest to be 0 
ywca_pd_types = [1 if t == 'Medical emergency' else 0 for t in ywca_pd["INCIDENT_TYPE_1"] ]

merged_data = list(zip(ywca_pd_discription,ywca_pd_types))


#functions from spacy documentation
# 
def load_data(limit=0, split=0.8):
    #the data set to be used 
    train_data = merged_data
    
    #random initials
    np.random.shuffle(train_data)
    train_data = train_data[-limit:]

    
    texts, labels = zip(*train_data)

    cats = [{'POSITIVE': bool(y)} for y in labels]
    split = int(len(train_data) * split)
    return (texts[:split], cats[:split]), (texts[split:], cats[split:])

## doc
def evaluate(tokenizer, textcat, texts, cats):
    docs = (tokenizer(text) for text in texts)
    tp = 1e-8  # True positives
    fp = 1e-8  # False positives
    fn = 1e-8  # False negatives
    tn = 1e-8  # True negatives
    for i, doc in enumerate(textcat.pipe(docs)):
        gold = cats[i]
        for label, score in doc.cats.items():
            if label not in gold:
                continue
            if score >= 0.5 and gold[label] >= 0.5:
                tp += 1.
            elif score >= 0.5 and gold[label] < 0.5:
                fp += 1.
            elif score < 0.5 and gold[label] < 0.5:
                tn += 1
            elif score < 0.5 and gold[label] >= 0.5:
                fn += 1
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f_score = 2 * (precision * recall) / (precision + recall)
    return {'textcat_p': precision, 'textcat_r': recall, 'textcat_f': f_score}

#("Number of texts to train")
n_texts=len(ywca_pd_types )

#("Number of training iterations")
n_iter=20

# train pipeline of textcat
if 'textcat' not in nlp.pipe_names:

    # set textcat to implement bag of words the default is CNN(concolutional neutral network)
    textcat = nlp.create_pipe('textcat',config={"architecture":"bow"})
    # textcat = nlp.create_pipe('textcat')
    nlp.add_pipe(textcat, last=True)
else:
    textcat = nlp.get_pipe('textcat')

textcat.add_label('POSITIVE')

print("Loading YWCA data....")
(train_texts, train_cats), (dev_texts, dev_cats) = load_data(limit=n_texts)
print("Using {} examples ({} training, {} evaluation)".format(n_texts, len(train_texts), len(dev_texts)))

train_data = list(zip(train_texts,[{'cats': cats} for cats in train_cats]))


other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'textcat']

with nlp.disable_pipes(*other_pipes):  # only train textcat
    optimizer = nlp.begin_training()
    print("Training the model...")
    print('{:^5}\t{:^5}\t{:^5}\t{:^5}'.format('LOSS', 'P', 'R', 'F'))
    for i in range(n_iter):
        losses = {}
        # batch up the examples using spaCy's minibatch
        batches = minibatch(train_data, size=compounding(1., 32., 1.001))
        for batch in batches:
            texts, annotations = zip(*batch)
            nlp.update(texts, annotations, sgd=optimizer, drop=0.2,
                       losses=losses)
        with textcat.model.use_params(optimizer.averages):
            # evaluate on the dev data split off in load_data()
            scores = evaluate(nlp.tokenizer, textcat, dev_texts, dev_cats)
        print('{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}'  # print a simple table
              .format(losses['textcat'], scores['textcat_p'],
                      scores['textcat_r'], scores['textcat_f']))


# save model to current directory 
# output_dir = "C:\\Users\\dongb\\Documents\\YWCA data\\Spacy\\med_class"
# nlp.to_disk(output_dir)

#testing 

# test1 = ywca_pd_discription[1]
# doc = nlp(test1)
# print(doc.cats)






