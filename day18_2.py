from collections import deque
import heapq
def main(path):
    with open(path) as infile:
        lines = infile.read().split('\n')
    
    grid = list(map(list, lines))
    
    doors = dict()
    keys = dict()
    start = None

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            char = grid[y][x]
            if(char.isalpha()):
                if(char.isupper()):
                    doors[char] = (x,y)
                else:
                    keys[char] = (x,y)
            elif(char == '@'):
                start = (x,y)
    
    keyNames = sorted(keys.keys())
    keyIntDict = dict()
    
    for i in range(len(keyNames)):
        keyIntDict[keyNames[i]] = 1<<i;
    
    nodes = ['@', *doors.keys(), *keys.keys()]
    nodesLoc = dict()
    nodesLoc['@'] = start
    for key in keys:
        nodesLoc[key] = keys[key]
    for door in doors:
        nodesLoc[door] = doors[door]
    
    nodeDist = dict()
    for node in nodes:
        nodeDist[node] = dict()

    
    
    visited = [[False for x in range(len(grid[y]))] for y in range(len(grid))]
    toExplore = deque();
    
    dy = [-1, 0, 1, 0]
    dx = [0, 1, 0, -1]
    
    def inRange(x,y):
        return x>=0 and x<len(grid[0]) and y>= 0 and y<len(grid)

    for node in nodes:
        visited = [[False for x in range(len(grid[y]))] for y in range(len(grid))]
        
        startPos = nodesLoc[node]
        toExplore.append((startPos, 0))
        visited[startPos[1]][startPos[0]] = True
        while(len(toExplore) != 0):
            curPos, curDis = toExplore.popleft()
            curX, curY = curPos
            gridChar = grid[curY][curX]
            if(gridChar in nodes and gridChar != node):
                nodeDist[node][gridChar] = curDis
            else:
                for i in range(4):
                    newX = curX + dx[i]
                    newY = curY + dy[i]
                    if(inRange(newX, newY)):
                        if(grid[newY][newX]!='#'):
                            if(not visited[newY][newX]):
                                visited[newY][newX] = True
                                toExplore.append(((newX, newY), curDis+1))

    bfDist = dict()
    print(nodeDist)
    pq = [(0, 0, '@')]
    heapq.heapify(pq)
    bfDist[('@', 0)] = 0
    
    def isSmaller(newDist, node, intKeyMap):
        if((node, intKeyMap) not in bfDist):
            return True
        else:
            return newDist < bfDist[(node, intKeyMap)]
    fullKeys = (1<<len(keys))-1
    
    while(len(pq)!=0):
        curDist, curKeyMap, curNode = heapq.heappop(pq)
        print((curNode, curKeyMap))
        if(curKeyMap == fullKeys):   
            print(curDist)
            break

        for nextNode in nodeDist[curNode]:
            newDist = curDist + nodeDist[curNode][nextNode]
            nextKeyMap = curKeyMap
            if(nextNode.isupper()):
                if(keyIntDict[nextNode.lower()] & nextKeyMap == 0):
                    #No key
                    continue
            elif(nextNode.islower()):
                #Add key
                nextKeyMap |= keyIntDict[nextNode]
            if(isSmaller(newDist, nextNode, nextKeyMap)):
                    bfDist[(nextNode, nextKeyMap)] = newDist
                    heapq.heappush(pq, (newDist, nextKeyMap, nextNode))
            
    

    #----------------------------------PART 2-----------------------------------------#
    
    
                    
main("input_day18")