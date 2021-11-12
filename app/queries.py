#! /usr/bin/env python3

from app import db
from app.models import Activitie
import sys

class Node():

    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

    def set_next(self, node):
        self.next = node 

    def set_prev(self, prev_node):
        self.prev = prev_node 

    def get_next(self):
        if self.next:
            return self.next

    def get_prev(self):
        if self.prev:
            return self.prev

class circularList():

    def __init__(self):
        self.head = None 
        self.tail = None


    def get_by_id(self, id):

        current_node = self.head
        while current_node.data.id != id:
            current_node = current_node.get_next()

        return current_node

    def insert_at_end(self, node):

        if self.head == None and self.tail == None:
            self.head = self.tail = node

        node.set_prev(self.tail)
        self.tail.set_next(node)
        self.tail = node
        self.tail.set_next(self.head)
        self.head.set_prev(self.tail)

    def print(self):
        current_node = self.head
        circular_counter = 0
        while current_node:
            print(current_node.data.header)
            current_node = current_node.get_next()


    def mark_as_done(self, node):
        node.data.status = 'done'



    def delete(self, node):
        previous = node.get_prev()
        next = node.get_next()
        next_next = node.get_next().get_next()

        previous.set_next(next_next)



    def populate(self, db_model):

        item = db_model.query.get(1)
        id = 1

        if item is None:
            raise ValueError('No such id')

        while item is not None:
            self.insert_at_end(Node(item))
            id += 1
            item = db_model.query.get(id)


if __name__ == "__main__":

    links = circularList()
    links.populate(Activitie)

    links.print_list()

