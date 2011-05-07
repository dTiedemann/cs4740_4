#!/usr/bin/env python
from combine import *
import init
import chunker
import mlpy
import check_answers
import align
from packer import pack
from sequence_length import       seq_length  
from punctuation_location import  punc_loc            
from apposition import question_apposition, rewrite_apposition  
from question_rewrite import literal_question_distance, literal_rewrite_distance, align_question_distance, align_rewrite_distance
from pos import                   pos_test
from bag_of_words import   vector_bag,  bag_of_words        
from novelty_factor import novelty_bool, novelty_count       
import cache_chunkers
from math import floor
import question_type

question_dict = dict(read_questions.read_questions_no_answers())
def get_question(q_id):
    return question_dict[str(q_id)]

def cache_file(q_id):
    base=int(10*floor(q_id/10))
    low=base+1
    high=base+10
    name='chunks/'+str(low)+'-'+str(high)+'.txt'
    return name

DIST_CUTOFF = 50
SCORE_CUTOFF = 5

def question_candidates(q_id):
    '''Select some useful subset of the candidates for a particular question.
    Return them in a list.
    '''
    init.get_corpus(qNum=q_id)
    foo=cache_file(q_id)
    candidate = cache_chunkers.uncache_chunks(open(foo))[q_id]
    new_l = []
    for c in candidate:
        if (c[3] == "NP"):
            dist = align_question_distance(get_question(q_id), c)
            if dist[0] < DIST_CUTOFF and dist[1] > SCORE_CUTOFF:
                new_l.append(c)
    align.save_cache()
    print len(new_l)
    return new_l

def question_learning_data(evaluators,q_ids):
    x=[]
    y=[]
    print q_ids
    for q_id in q_ids:
        cand=question_candidates(q_id)
        x=x+run_evaluators(cand,evaluators)
        y=y+map(lambda a:check_answers.check_answer(q_id,a),cand)
    return y,x

def question_prediction_data(q_id,candidate,evaluators):
    x=run_evaluators([candidate],evaluators)
    return x[0],candidate

def run_question_predictions(evaluators,trained_model,q_ids):
    answers=[]
    for q_id in q_ids:
        y_hat=[]
        for candidate in question_candidates(q_id):
            x_test,candidate= question_prediction_data(q_id,candidate,evaluators)
            y_hat.append( ( test(trained_model,x_test) , candidate ) )
        y_hat = sorted(y_hat, key=lambda (s,_): s,reverse=True)
        y_hat = map(lambda a:(a[0],a[1][0]),y_hat)
        for i in range(0,5):
            answers.append((q_id,pack(y_hat, 50)[0]))
    return answers

def answerLine(answer):
        return str(answer[0])+' OVER9000 '+answer[1]

def answerFile(answers):
        return "\n".join(map(answerLine,answers))

def writeAnswers(stuff,filename='tmp-answers.txt'):
        answersHandle=open(filename,'w')
        answersHandle.write(stuff)
        answersHandle.close()

def main():
    align.load_cache()
    #foo=map(int,question_type.classify_questions(1)['Where'])
    #Where questions
    foo=[202, 211, 223, 226, 227, 243, 245, 249, 258, 266, 272, 283, 304, 306, 317, 318, 356, 359, 368, 369, 373, 385, 393]
    evaluatorCombinationID=9000
#    trainIDs=foo[:-6]
#    validationIDs=foo[-6:]
    trainIDs=foo
    validationIDs=[10025,10026]

    evaluator_combinations=[
    [punc_loc,novelty_bool],
    [punc_loc],
    [novelty_bool]

#Don't use because they're weird
#    vector_bag,
#     [seq_length]
#    [punc_loc]
    ]
    for evaluators in evaluator_combinations:
        y_train,x_train = question_learning_data(evaluators,trainIDs)
#        print y_train
        trained=train(mlpy.Srda,y_train,x_train)
        results=run_question_predictions(evaluators,trained,validationIDs)
        writeAnswers(answerFile(results),'results/combination'+str(evaluatorCombinationID)+'.txt')
        evaluatorCombinationID=evaluatorCombinationID+1
    align.load_cache()
    align.save_cache()
    
if __name__ == '__main__':
    main()
    question_candidates (243)
