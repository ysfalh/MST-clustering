def find(parent, i): 
	if parent[i] == i: 
		return i 
	return find(parent, parent[i]) 

# returns dict mapping nodes to their root parent
def ancestor(parent):
	acstor = {key : find(parent, key) for key in parent.keys()}
	return acstor

def union(parent, rank, x, y): 
	xp = find(parent, x) 
	yp = find(parent, y) 

	if rank[xp] < rank[yp]: 
		parent[xp] = yp
	elif rank[xp] > rank[yp]: 
		parent[yp] = xp
	else : 
		parent[yp] = xp
		rank[xp] += 1
