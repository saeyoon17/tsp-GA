import numpy as np
from class_def import Node


# preprocess takes the name of the input_instance and provides a
# numpy array with the nodes inside.
def preprocess(input_instance):

    f = open(input_instance, 'r')
    # throw away unnecessary parts of the tsp instance
    for i in range(6):
        f.readline()

    nodelst = []

    for line in f:
        temp = line.strip().split()

        # if EOF
        if len(temp) == 1:
            break
        if temp[1][-4] == "e":
            seq = temp[0]
            x = float(temp[1][:-4])
            exp_x = int(temp[1][-2:])
            real_x = x * 10**exp_x

            y = float(temp[2][:-4])
            exp_y = int(temp[2][-2:])
            real_y = y * 10**exp_y
        else:
            seq = temp[0]
            real_x = float(temp[1])
            real_y = float(temp[2])

        nodelst.append(Node(seq, real_x, real_y))

    return np.array(nodelst)


# returns a list that slices the whole nodearray and outputs
# np.array that is divided into slice_num * slice_num grids
def grid_alize(nodearray, slice_num):
    
    x_max = 0
    x_min = nodearray[0].x
    y_max = 0
    y_min = nodearray[0].y

    # get max, min of x, y
    for e in nodearray:
        if e.x > x_max:
            x_max = e.x
        elif e.x < x_min:
            x_min = e.x
            
        if e.y > y_max:
            y_max = e.y
        elif e.y < y_min:
            y_min = e.y
            
    x_diff = (x_max - x_min) / slice_num
    y_diff = (y_max - y_min) / slice_num
    
    cheat_sheet = []

    # append range to list (will pop the range after)
    for i in range(slice_num):
        for j in range(slice_num):
            cheat_sheet.append([(x_min + x_diff * (j+1) , y_min + y_diff * (i+1))])
    
    # fit the nodes to list
    for e in nodearray:
        for sheet in cheat_sheet:
            if e.x <= sheet[0][0] and e.y <= sheet[0][1]:
                sheet.append(e)
                break

    # pop the range (to just keep nodes)
    for sheet in cheat_sheet:
        sheet.pop(0)
        
    check = 0
    for e in cheat_sheet:
        check += len(e)
        
    return np.array(cheat_sheet)

