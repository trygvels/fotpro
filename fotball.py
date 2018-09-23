import numpy as np
from random import randint
from collections import Counter
import sys
# Parameters
sigma = 5.
Variance = 5.
# [Navn, vekting]
en   = np.loadtxt("keeper.txt",dtype=np.str)
to   = np.loadtxt("Vbekk.txt",dtype=np.str)
tre  = np.loadtxt("Hbekk.txt",dtype=np.str)
fire = np.loadtxt("Mbekk.txt",dtype=np.str)
fem  = np.loadtxt("linje.txt",dtype=np.str)
seks = np.loadtxt("Vving.txt",dtype=np.str)
syv  = np.loadtxt("Hving.txt",dtype=np.str)
navn=np.array([en, to, tre, fire, fem, seks, syv])
num_pos=len(navn)

# [Navn]
motstandere = np.loadtxt("motstandere.txt", dtype=np.str)
num_mot=len(motstandere)

#print "en:", en
#print len(en),len(to),len(tre),len(fire),len(fem),len(seks),len(syv)

# Lengde av hver gruppe
lens = [len(en),len(to),len(tre),len(fire),len(fem),len(seks),len(syv)]
#print "lens", lens

en_ranks   = np.zeros(lens[0])
to_ranks   = np.zeros(lens[1])
tre_ranks  = np.zeros(lens[2])
fire_ranks = np.zeros(lens[3])
fem_ranks  = np.zeros(lens[4])
seks_ranks = np.zeros(lens[5])
syv_ranks  = np.zeros(lens[6])

# assigned ranking to each player
ranks=np.array([en_ranks, to_ranks, tre_ranks, fire_ranks, fem_ranks, seks_ranks, syv_ranks])


# Rank all players in groups between 1 and num_mot
l = 0
for i in lens:
  for j in range(i):
    ranks[l][j] = 1.+((num_mot-1.)/(i-1.))*j
  l+=1

"""
# TESTING MIN AND MAX IN GRP
adding_min=0
adding_max=0
for i in range(len(ranks)):
  adding_min+=ranks[i][0]
  adding_max+=ranks[i][-1]
print adding_min/num_pos, adding_max/num_pos
"""

likemangekamper=False
while likemangekamper==False:  # run until each player has played approximately the same number of games
    likemangekamper=True

    kamper=np.zeros((len(motstandere),7)) # Matrix of each match setup

    for i in range(len(motstandere)): # Generate matchup per opponent
        lol=False
        while lol==False: # Run untill rank of team matches opponent
            pos1=randint(0,lens[0]-1) # Generate random player
            pos2=randint(0,lens[1]-1)
            pos3=randint(0,lens[2]-1)
            pos4=randint(0,lens[3]-1)
            pos5=randint(0,lens[4]-1)
            pos6=randint(0,lens[5]-1)
            pos7=randint(0,lens[6]-1)

            # check if same player is chosen twice
            nms=[navn[0][pos1],navn[1][pos2],navn[2][pos3],navn[3][pos4],navn[4][pos5],navn[5][pos6],navn[6][pos7]]
            if max(Counter(nms).values()) > 1.:
                continue

            vals=[ranks[0][pos1],ranks[1][pos2],ranks[2][pos3],ranks[3][pos4],ranks[4][pos5],ranks[5][pos6],ranks[6][pos7]]

            #print "Values of suggested team: ", vals
            #print "Sum of suggested team: ", sum(vals)/num_pos

            # Check if generated team matches opponent rank
            if sum(vals)/num_pos > i - sigma and sum(vals)/num_pos < i + sigma:
                lol = True
                kamper[i]=[pos1,pos2, pos3, pos4, pos5, pos6, pos7] # save generated team
                #print "using team", kamper[i]
                #print "with value", sum(vals)/num_pos, " against ", motstandere[i], " with value", i



    # Making list of player names
    spillere=[]
    for j in range(num_mot):
        for i in range(7):
            spillere.append(navn[i][int(kamper[j,i])])

    # Check if players have played similar number of games
    if np.var(Counter(spillere).values())>Variance:
        likemangekamper=False
    else:
        print "Variance: ", np.var(Counter(spillere).values())
        print "Players: ", Counter(spillere).values()

# Output match setups
for j in range(num_mot):
    print "--------"
    for i in range(7):
        print navn[i][int(kamper[j,i])]
    print "spiller mot", motstandere[j]


print kamper
