"""
This file implements the data structures that are used in the project
"""

# Imports
import random as rng

# Textbook Node implementation for linked list nodes
class Node:

    def __init__(self, initial_data):
        self.data = initial_data
        self.next = None
        self.prev = None

    def get_next(self):
        return self.next
    
    def get_prev(self):
        return self.prev
    
    def get_data(self):
        return self.data
    
    def set_next(self,new_next):
        self.next = new_next

    def set_prev(self,new_prev):
        self.prev = new_prev

# Textbook class implementation of linked list
class LinkedList:

    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, new_node):

        if self.head == None:
            self.head = new_node
            self.tail = new_node

        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def prepend(self, new_node):

        if self.head == None:
            self.head = new_node
            self.tail = new_node

        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def insert_after(self, current_node, new_node):

        if self.head is None:
            self.head = new_node
            self.tail = new_node

        elif current_node is self.tail:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

        else:
            successor_node = current_node.next
            new_node.next = successor_node
            new_node.prev = current_node
            current_node.next = new_node
            successor_node.prev = new_node
   
    def remove(self, current_node):

        successor_node = current_node.next
        predecessor_node = current_node.prev

        if successor_node is not None:
            successor_node.prev = predecessor_node

        if predecessor_node is not None:
            predecessor_node.next = successor_node

        if current_node is self.head:
            self.head = successor_node

        if current_node is self.tail:
            self.tail = predecessor_node

def clear_linkedlist(linkedlist): # Removes every node of the linked list, emptying it

    curnode = linkedlist.head
    while curnode != None:
        next = curnode.next
        linkedlist.remove(curnode)
        curnode = next

def is_in_linkedlist(linkedlist,datavalue): # Predicate function that determines if datavalue is in the linked list

    curnode = linkedlist.head
    while curnode != None:

        if curnode.get_data() == datavalue:
            return True
        
        curnode = curnode.next

    return False

def shuffle_and_fill(stack, new_contents): # Pushes all items from new_contents into stack in random order

    while new_contents != []:
        item = rng.choice(new_contents)
        new_contents.remove(item)
        stack.push(item)

class Stack:
    # Initializes the stack. If the optional_max_length argument is omitted or 
    # negative, the stack is unbounded. If optional_max_length is non-negative, 
    # the stack is bounded.

    def __init__(self, optional_max_length = -1):
        self.stack_list = []
        self.max_length = optional_max_length
    
    # Gets the length of the stack
    def __len__(self):
        return len(self.stack_list)
    
    # Pops and returns the stack's top item.
    def pop(self):
        return self.stack_list.pop()
    
    # Pushes an item, provided the push doesn't exceed bounds. Does nothing otherwise. Returns True if the push occurred, False otherwise.
    def push(self, item):
        # If at max length, return false
        if len(self.stack_list) == self.max_length:
            return False
        
        # If unbounded, or bounded and not yet at max length, then push
        self.stack_list.append(item)
        return True
    
    # Predicate function, checking if stack is empty
    def is_empty(self):

        if self.stack_list == []:
            print("IK it is empty")
            return True
        
        print(self.stack_list)
        return False