import argparse
from main_acc import saeyoon_ga
from class_def import Node, Route
import numpy as np
from pre_process import preprocess

parser = argparse.ArgumentParser()
parser.add_argument('filename')

parser.add_argument("-p1", "--population1", type = int, help="population of the GA for the sub-instances")
parser.add_argument("-m1", "--mutationrate1", type = int,help="mutation rate of the GA for the sub-instances")
parser.add_argument("-g1", "--generation1", type = int,help="generation to run for the GA for the sub-instances")

parser.add_argument("-n", "--slice", type = int,help="number of slice per axis, gives n*n grids")

parser.add_argument("-p2", "--population2", type = int,help="population of the GA for the full-route")
parser.add_argument("-m2", "--mutationrate2", type = int,help="mutation rate of the GA for the full-route")
parser.add_argument("-g2", "--generation2", type = int,help="generation to run for the GA for the full-route")

args = parser.parse_args()

nodearray = preprocess(args.filename)


p1 = 30
m1 = 0.1
g1 = 20

n = int(np.sqrt(len(nodearray) / 2.72015))

p2 = 200
m2 = 0.5
g2 = 20


if args.population1:
    p1 = args.population1
if args.mutationrate1:
    m1 = args.mutationrate1
if args.generation1:
    g1 = args.generation1

if args.slice:
    n = args.slice

if args.population2:
    p2 = args.population2
if args.mutationrate2:
    m2 = args.mutationrate2
if args.generation2:
    g2 = args.generation2



final= saeyoon_ga(nodearray, p1, m1, g1, n, p2, m2, g2)
print("final distance: " + str(final.distance()))
route = final.route 
f = open("solution.csv", "w")
for e in route:
    f.write(str(e.seq) +"\n")
f.close()