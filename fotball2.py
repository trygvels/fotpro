import numpy as np
from random import randint, choice
from collections import Counter
import sys

# Parameters
if len(sys.argv) < 10:
    print "You are using it wrong. Try:"
    print "fotball.py [sigma, f.ex. 2.0] [opponents.txt] [pos1.txt] [pos2.txt] [pos3.txt] [pos4.txt] [pos5.txt] [pos6.txt] [pos7.txt]"
    sys.exit()

sigma = float(sys.argv[1]) # 2.
variance=2.
num_pos= 7
num_team=14


# Loading player names and lengths of groups
names=[]
lens=[]
for i in range(7):
    txt=np.loadtxt(str(sys.argv[i+3]),dtype=np.str)
    names.append(txt)                # nested list of names
    lens.append(len(txt))           # create list of group lengths
# Opponent team
opponents = np.loadtxt(sys.argv[2], dtype=np.str)
lens = [x for pair in zip(lens,lens) for x in pair] # Fix lengths array for 14 players
num_opp=len(opponents)
names = np.asarray(names)

def makenames(matchi):
    # Making array of names
    a = np.chararray((num_team,num_opp),itemsize=30)
    for i in range(num_team):
        k = i
        if i >= num_pos:
            k = i-num_pos
        for j in range(num_opp):
            a[i,j] = names[k][int(matchi[i,j])]
    return a

# Order in team setups from best to worst
def make_index_matrix(dim, max_values):
    assert len(max_values) == dim[0]
    out = np.zeros(dim)
    j = 0
    for k, mv in enumerate(max_values):
        assert mv > 0
        a = np.arange(mv).repeat(np.floor(dim[1]/mv))

        if len(a) < dim[1]:
            r = np.arange(mv)
            a = np.concatenate((a, r))

        out[k,:] = a[:dim[1]]

    return out

"""
Generate teams in increasing order
If variance is way off, retry.
"""
matches = make_index_matrix((num_team,num_opp),lens)
matches=matches[:,np.argsort(np.sum(matches,axis=0))] # sort by sum of columns
# Creating stabdard tean setyo
matches[num_pos:,:]= matches[:num_pos,:]+1
ma = np.max(matches[:num_pos,:]) # Highest actual player index
matches[np.where(matches==ma+1)]=randint(0,ma-1) #Making sure we dont add unexisting players
matches=matches[:,np.argsort(np.sum(matches,axis=0))] # sort by sum of columns

dups=True
while dups == True:

    a = makenames(matches)

    # Check for duplpicate names
    for i in range(num_opp):
        lol1 = np.max(Counter(a[:,i]).values())
        if lol1==1:
            continue

        newmatch1 = np.zeros_like(matches)
        newmatch1[:,:] = matches[:,:] # new team proposal
        j = randint(0,num_team-1) # Try to swap a random position
        #print matches[j,:]
        newmatch1[j,i]=choice(matches[j,:])

        newnames = makenames(newmatch1)
        oldnames = makenames(matches)


        vals1 = Counter(newnames[:,i]).values()
        vals2 = Counter(oldnames[:,i]).values()
        lol1 = np.max(vals1)
        lol2 = np.max(vals2)
        lol11 = sum(x > 1 for x in vals1)
        lol22 = sum(x > 1 for x in vals2)
        #print lol11, lol22

        if lol1<lol2 or lol11<lol22:
            matches[:,:] = newmatch1[:,:]

    dups = False
    for i in range(num_opp):
        lol1 = np.max(Counter(a[:,i]).values())
        if lol1>1:
            #print Counter(a[:,i])
            dups=True

    #if np.var(Counter(a.flatten()).values())>num_opp/2.: # Account for variance
    #    dups=True

matches=matches[:,np.argsort(np.sum(matches,axis=0))] # sort by sum of columns
print "******************"
print "ORIGINAL MATCHES"
print matches


newmatch = np.zeros_like(matches)
count = 0
convergence = False
rankss = np.linspace(0, np.max(matches)*num_team, len(matches[i,:]))


while convergence==False:
    i = randint(0,num_team-1) # pick random position
    a = randint(0,len(matches[i,:])-1) # Pick random player in that position
    b = randint(0,len(matches[i,:])-1) # pick random player in that position
    # Not same indices
    if a == b:
        continue

    newmatch[:,:] = matches[:,:] # new team proposal

    player_b = matches[i, b] # Switch position
    player_a = matches[i, a] # Switch position
    newmatch[i, a] = player_b
    newmatch[i, b] = player_a

    # If no change skip
    if False not in (matches==newmatch):
        continue

    rank_a = np.sum(newmatch[:,a]) # rank of new game a
    rank_b = np.sum(newmatch[:,b]) # rank of new game b

    # the rank of each opponent team is 0 to num_opp
    if rank_a > (rankss[a] - sigma) and rank_a < (rankss[a]+sigma):
        if rank_b > (rankss[b] - sigma) and rank_b < (rankss[b] + sigma):

            newnames = makenames(newmatch)
            oldnames = makenames(matches)

            # Check for duplicate names
            dups=False
            lessdups=False
            for i in range(num_opp):
                lol1 = np.max(Counter(newnames[:,i]).values())
                lol2 = np.max(Counter(oldnames[:,i]).values())
                if lol1>1:
                    dups=True
                if lol1<lol2:
                    lessdups=True


            if dups==False or lessdups==True: # np.max(Counter(a[:,i]).values())<2 and nonduplicates==True:
                matches[:,:] = newmatch[:,:]
            else:
                continue

    newnames = makenames(matches)
    dups=False
    for i in range(num_opp):
        lol1 = np.max(Counter(newnames[:,i]).values())
        if lol1>1:
            dups=True

    if count>100000 and dups==False:
        convergence = True
    #print count
    count+=1

matches=matches[:,np.argsort(np.sum(matches,axis=0))] # sort by sum of columns
print "******************"
print "FINAL MATCHES"
print matches

# Making final array of names
a = makenames(matches)

# Removing ".txt"
positions=[sys.argv[3:]][0]
for i in range(len(positions)):
    lol = str(positions[i])
    if lol.endswith('.txt'):
        positions[i] = lol[:-4]


# OUTPUT
text_file = open("Output.txt", "w")
for i in range(num_opp):
    print "----- Playing against " + str(opponents[i]) + "-------"
    text_file.write("----- Playing against " + str(opponents[i]) + "-------")
    for j in range(num_pos):
        print "             " + str(positions[j]) + ""
        print a[j,i]
        print a[j+7,i]
        text_file.write("             " + str(positions[j]) + "")
        text_file.write(a[j,i])
        text_file.write(a[j+7,i])

print Counter(a.flatten())
text_file.write(str(Counter(a.flatten())))


text_file.close()
