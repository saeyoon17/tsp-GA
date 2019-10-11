# This is the main accumulator for genetic algorithm

from pre_process import preprocess
from sub_prob import run_sub_prob
from full_prob import run_full_prob
from class_def import Route

# connects the answer using the subsequence
def connect(subseq, new_answer):

    initial_sample = []
    for e in subseq:

        temp = new_answer[e]
        if type(temp) != list:
            temp = temp.tolist()
        initial_sample += temp
    return Route(initial_sample)

# subsequence for vertical travel
def vertical_subseq(slice_num):

    ret_lst = []
    for i in range(slice_num):
        for j in range(slice_num):
            if (i%2 == 0):
                ret_lst.append(i + slice_num*j)
            else:
                ret_lst.append(i + slice_num*(slice_num-1-j))
    
    return ret_lst

#subsequence for horizontal travel
def horizontal_subseq(slice_num):

    ret_lst = []
    for i in range(slice_num):
        for j in range(slice_num):
            if (i%2 == 0):
                ret_lst.append(j + slice_num*i)
            else:
                ret_lst.append((slice_num-1-j) + slice_num * i)
    return ret_lst

# for each node, extract the routes
def make_new_answer(answer):
    
    new_answer = []
    for e in answer:
        if e == []:
            new_answer.append([])
        else:
            new_answer.append(e.route)
    return new_answer

# My GA!
def saeyoon_ga(nodearray, population1, m_rate1, generation1, slice_num, population2, m_rate2, generation2):

    (horizontal, vertical) = run_sub_prob(nodearray, slice_num, population1, m_rate1, generation1)
    
    horizontal = make_new_answer(horizontal)
    vertical = make_new_answer(vertical)

    h_subseq = horizontal_subseq(slice_num)
    v_subseq = vertical_subseq(slice_num)

    h_using_h = connect(h_subseq, horizontal)
    print("horizontal travel using horizontal subsequence! " + str(h_using_h.distance()))
    v_using_v = connect(v_subseq, vertical)
    print("vertical travel using vertical subsequence! " + str(v_using_v.distance()))
    h_using_v = connect(v_subseq, horizontal)
    print("horizontal travel using vertical subsequence! " + str(h_using_v.distance()))
    v_using_h = connect(h_subseq, vertical)
    print("vertical travel using horizontal subsequence! " + str(v_using_h.distance()))

    initial_sample = sorted([h_using_h, h_using_v, v_using_h, v_using_v], key= lambda route : route.length)[0]

    answer = run_full_prob(initial_sample, population2, m_rate2, generation2)

    return answer