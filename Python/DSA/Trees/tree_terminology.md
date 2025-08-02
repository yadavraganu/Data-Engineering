# Tree
A tree consist of  nodes/vertices & edges.If there are n nodes then there will be n-1 edges.
- __Root :__ First node which does not have any parent in tree is called root node.
- __Parent :__ A node is parent to its very next descendents.
- __Child :__ Node which are next descendents of parent are called child nodes.
- __Siblings :__ Nodes which have common parent are called siblings
- __Descendents :__ Descendents are all those node or set of nodes which can be reached from that node in downwards direction.
- __Ancesters :__ Nodes which are coming in way when moving from the node to root node in upwards direction are called ancester nodes.
- __Degree of Node :__ The min degree of a tree can be the number of max child a node is having in the tree.
- __Leaf/Terminal Nodes :__ Node which are having degree as 0 i.e. no child.
- __Non-leaf/Non-terminal Nodes :__ Node which are having degree greater than 0 i.e. having 1 or more child.
- __Level :__ Level of a tree starts from 1 & gets incresed by one as we move to child level then child of chils level & so on.
- __Height :__ Height of a tree starts from 0 & gets incresed by one as we move to child level then child of chils level & so on.
- __Forest :__ Collection of trees called forest

# Binary Tree
A tree with degree of 2 is called binary tree.So any node in binary tree can have 0,1,2 i.e. at most 2 childs
If we have n number of unlabled nodes we can have below variation of binary tree.
```
Number = (2n C n)/n+1
Where n C r = n! /r!*(n-r)!
If nodes are labeled then multiple above formula with n!.
```
If we have n number of nodes then how many binary tree with max height can we generated.
```
Number = 2**n-1 
```
