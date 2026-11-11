import copy

class Node:
    def __init__(self, startDate, endDate, cost, clientID):
        self.startDate = startDate
        self.endDate = endDate
        self.cost = cost

        self.clientID = clientID
        self.next = None
        self.incoming = set()
        self.opt = None
        self.maxRevenue = 0
    
class DAG:
    def __init__(self):
        self.Adjlist = []
        self.Clients = []
        self.optimal_val = 0
        self.clientsByID = {}
        self.Start = Node(0, 0, 0, 0)
        self.End = Node(0, 0, 0, -1)
        self.clientsByID[0] = self.Start
        self.clientsByID[-1] = self.End


    def add_vertex(self, Node): 
        self.Adjlist.append(Node)
        self.clientsByID[Node.clientID] = Node

    def add_edge(self, source, destination):
        newNode = copy.copy(destination)
        newNode.next = None
        temp = source

        while temp.next is not None:
            temp = temp.next

        temp.next = newNode

        destination.incoming.add(source.clientID)

    def build_adjlist(self): #come back and add start and end for DAG

        for i in range(len(self.Adjlist)):
            for j in range(len(self.Adjlist)):

                if i == j:
                    continue

                if self.Adjlist[i].endDate <= self.Adjlist[j].startDate:
                    self.add_edge(self.Adjlist[i], self.Adjlist[j])

        for client in self.Adjlist:

            if not client.incoming:
                self.add_edge(self.Start, client)

            if client.next is None:
                self.add_edge(client, self.End)

        if not self.Adjlist:
            self.add_edge(self.Start, self.End)

    def Source_Removal(self):
            vertices = [self.Start] + self.Adjlist + [self.End]
            indegree = {}
            queue = []
            topolist = []
            front = 0

            for v in vertices:
                indegree[v.clientID] = len(v.incoming)
            
            for v in vertices:
                if indegree[v.clientID] == 0:
                    queue.append(v)

            while front < len(queue):
                current = queue[front]
                front += 1
                topolist.append(current)
                neighbor = current.next
            
                while neighbor is not None:
                    indegree[neighbor.clientID] -= 1
            
                    if indegree[neighbor.clientID] == 0:
                        queue.append(self.clientsByID[neighbor.clientID])
            
                    neighbor = neighbor.next

            return topolist

    def optimal_rev(self):
        topolist = self.Source_Removal()

        for current in reversed(topolist):
            if current is self.End:
                current.maxRevenue = 0
                continue

            best_neighbor = None
            best_revenue = -1

            neighbor = current.next

            while neighbor is not None:
                original = self.clientsByID[neighbor.clientID]

                if original.maxRevenue > best_revenue:
                    best_revenue = original.maxRevenue
                    best_neighbor = original

                neighbor = neighbor.next

            current.opt = best_neighbor
            current.maxRevenue = current.cost + best_revenue

        self.optimal_val = self.Start.maxRevenue
        self.Clients = []
        current = self.Start.opt

        while current is not None and current is not self.End:
            self.Clients.append(current)
            current = current.opt

        return self.optimal_val


    def pr_clients(self): #fix buggy printing

        print("Clients contributing to this optimal revenue:", end=" ")

        for i, client in enumerate(self.Clients):
            if i > 0:
                print(", ", end="")

            print(client.clientID, end="")

        print()


graph = DAG() #this is global, I am sorry gill. I am lazy

        


def readFile(fileName):
    numClient = 0
    with open(fileName, "r", encoding="utf-8") as file:
        for line in file:
            numClient += 1
            startDate, endDate, cost = map(int, line.split())

            graph.add_vertex(Node(startDate, endDate, cost, numClient))

    return numClient





fileName = input('Enter the file to read data: ')

print()

numClients = readFile(fileName)

print('There are', numClients, 'clients in the file')

print()

graph.build_adjlist()

print('Optimal revenue earned is', graph.optimal_rev())

graph.pr_clients()

