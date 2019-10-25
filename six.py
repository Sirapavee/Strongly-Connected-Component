#-------------------------------init adj matrix---------------------------
f = open('Ex3.txt', 'r')

l = []
for line in f:
    coor = line.strip().split()
    l.append(coor)

vertex = int(l[0][0])
l.remove(l[0])
graph = [[0 for x in range(vertex)] for y in range(vertex)]

for e in l:
    p1 = int(e[0])-1
    p2 = int(e[1])-1
    graph[p1][p2] = 1

f.close()
#-------------------------------------------------------------------------

#vertex class
class vertX:
    def __init__(self, id):
        self.id = id
        self.pre = None
        self.color = 'white'
        self.d = 0
        self.f = 0

#DFS
def DFS(vertexList):
    for vx in vertexList:
        vx.color = 'white'

finL = [] #topo sort list
time = 0
#find max vertex
def visitDFS(vxx):
    global time
    time += 1
    vxx.d = time
    vxx.color = 'gray'
    for i in range(vertex):
        if graph[vxx.id][i] == 1 and vList[i].color == 'white':
            vList[i].pre = vxx
            visitDFS(vList[i])
    vxx.color = 'black'
    time += 1
    vxx.f = time
    finL.append(vxx)

#init vertex
vList = []
for i in range(vertex):
    vtt = vertX(i)
    vList.append(vtt)

#let's get start
for vt in vList:
    if vt.color == 'white':
        visitDFS(vt) 

#transpose
t_graph = [[graph[j][i] for j in range(len(graph))] for i in range(len(graph[0]))]
#reverse topo sort
bfinL = [finL[i] for i in range(len(finL)-1, -1, -1)] 

#reset color of vertices
DFS(bfinL)

#call visitDFS again but only for add scc in sccl list
sccl = [[] for g in range(vertex)]
def findMaxV(v, cnt):
    v.color = 'gray'
    for j in range(vertex):
        if t_graph[v.id][j] == 1 :
            for vtx in bfinL:
                if vtx.id == j and vtx.color == 'white':
                    findMaxV(vtx, cnt)
    v.color = 'black'
    sccl[cnt].append(v)

#init 2nd DFS to find scc
index = 0
for vxxx in bfinL:
    if vxxx.color == 'white':
        findMaxV(vxxx, index)
        index += 1

#find max scc vertices
maxLen = 0
for t in sccl:
    if maxLen<len(t):
        maxLen=len(t)

#print max scc vertices
print(f'Max vertices : {maxLen}')
#get rid of empty list from scc
cleanerSccl = list(filter(None, sccl))
#init component tree
tree = [[0 for x in range(len(cleanerSccl))]for y in range(len(cleanerSccl))]
#add edge to tree
for i in range(len(cleanerSccl)):
    for j in cleanerSccl[i]:
        for k in range(len(cleanerSccl)):
            if (k!=i):
                for l in cleanerSccl[k]:
                    if(graph[j.id][l.id]==1):
                        tree[i][k] = 1
                        break

#least edge to add in tree in order to acheive V vertex cycle
cnt = 0
maxx = 0
def leastEdgeToGetNVertexInSCC(ind):
    global cnt, maxx
    for p in range(len(tree)):
        if(tree[ind][p]==1):
            cnt += 1
            leastEdgeToGetNVertexInSCC(p)
            if(maxx<cnt):
                maxx = cnt
            cnt-=1
leastEdgeToGetNVertexInSCC(0)
print(f'Need to add at least {len(tree)-maxx} edge(s)')