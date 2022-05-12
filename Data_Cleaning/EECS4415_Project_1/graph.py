import argparse
import os

parser = argparse.ArgumentParser(description='Put data file name')
parser.add_argument("file", type=str)
args = parser.parse_args()
datafile = args.file
# Receive input file from user

# Check if the file path is valid
if os.path.isfile(datafile):
    f = open(datafile)
    lines = f.readlines()
    # Read every line in the file and store as list

    if len(lines) == 0:
        print('The file is empty')
        # if there is nothing to read in the file

    else:
        for i in range(0, len(lines)):
            lines[i] = lines[i].strip('\n')
            # Remove \n from the back side of every line

        vertices = {}
        # To store in format of {vertex: adjacent vertices' list}

        for i in range(0, len(lines)):
            v = lines[i].strip().split(' ')
            v1 = v[0]
            v2 = v[1]
            # 2 vertices from each line

            if v1 not in vertices:
                vertices[v1] = {v2: 0}
                # If the vertex is not in vertices dictionary, add it with adjacent vertex
                # Adjacent vertex key's default value is 0
            else:
                if v2 not in vertices[v1]:
                    vertices[v1][v2] = 0
                    # If the vertex is already in vertices list, add only adjacent vertex with default value 0.

            if v2 not in vertices:
                vertices[v2] = {v1: 0}
            else:
                if v1 not in vertices[v2]:
                    vertices[v2][v1] = 0
            # The same logic with v1 computation above

        numOfV = len(vertices)
        # vertices list length = the number of vertices

        totalDegree = 0
        # To count the total degree

        for i in vertices:
            totalDegree += len(vertices[i])
        # Count all edges = total degree of graph

        avgOfDeg = totalDegree / len(vertices)
        line2 = str(round(avgOfDeg, 2)) + '\n'
        # Average of degree = total degree / the number of vertices

        totalDegree /= 2
        line1 = str(numOfV) + ' ' + str(int(totalDegree)) + '\n'
        # Number of edges = total degree / 2

        vertexList = list(vertices.keys())
        count = 0
        # Vertices list to count components of graph

        while len(vertexList) > 0:
            root = vertexList.pop(0)
            queue = [root]
            while len(queue) > 0:
                first = queue.pop(0)
                edges = vertices[first]
                for i in edges:
                    if i not in queue and i in vertexList:
                        queue.append(i)
                        vertexList.remove(i)
            count += 1
        line3 = str(count) + '\n'
        # BFS to check components of graph
        # From the vertices list, pop the first element and add to queue.
        # And, add all adjacent vertices and, after that, remove from the queue
        # and also remove from the list to prevent to be added in the queue again by other vertex's adjacent vertex
        # If queue is empty, it means checked every adjacent vertices of the item popped from the list
        # So, count 1. If the list is not empty, it means there is other components that is not counted yet
        # So, repeat it until list is empty

        vertexList = list(vertices.keys())
        count = 0
        # Vertices list to count triangles(a-b, b-c, c-a relationship) of graph

        while len(vertexList) > 0:
            first = vertexList.pop(0)
            firstEdges = vertices[first]
            for second in firstEdges:
                secondEdges = vertices[second]
                for third in secondEdges:
                    if third != first:
                        thirdEdges = vertices[third]
                        for lastNode in thirdEdges:
                            if lastNode == first:
                                count += 1
        line4 = str(int(count/6))
        # first(popped item) -(first edge) second(adjacent vertex of first) -(second edges) third(adjacent vertex of
        # second except for first) -(last node) <= in the last node, if they have first as adjacent vertex, it means
        # first, second, third vertices makes triangle relationship.
        # But, since triangle is counted in every vertex(3 vertex in triangle)
        # and 2 times per vertex( e.g) a-b-c-a, a-c-b-a),
        # divide total count by 3*2=6 to get total triangles

        w = open('Q4.out', 'w')
        w.write(line1 + line2 + line3 + line4)
        w.close()
        # Open file to write information and write them and close

else:
    print("File path is not valid")
    # if the file path is not valid
