import unittest
from unittest import TestCase


class Node(object):
    key = None
    value = None
    next = None

    def __init__(self, key=None, value=None, next=None):
        self.key = key
        self.value = value
        self.next = next


class LinkedHashTable(object):
    """
    By having each bucket contain a linked list of elements that are hashed to that bucket. 
    """
    _empty = None

    def __init__(self, size=11):
        self.size = size
        self._len = 0
        self._table = [self._empty] * size

    def put(self, key, value):
        hash_ = self.hash(key)
        node_ = self._table[hash_]
        if node_ is self._empty:
            self._table[hash_] = Node(key, value)
            self._len += 1
            return
        while node_.next is not None:
            if node_.key == key:
                node_.value = value
                return
            node_ = node_.next
        node_.next = Node(key, value)
        self._len += 1

    def get(self, key):
        hash_ = self.hash(key)
        node_ = self._table[hash_]
        while node_ is not self._empty:
            if node_.key == key:
                return node_.value
            node_ = node_.next
        return None

    def del_(self, key):
        hash_ = self.hash(key)
        node_ = self._table[hash_]
        pre_node = None
        while node_ is not None:
            if node_.key == key:
                if pre_node is None:
                    self._table[hash_] = node_.next
                else:
                    pre_node.next = node_.next
                self._len -= 1
            pre_node = node_
            node_ = node_.next

    def hash(self, key):
        return hash(key) % self.size

    def __len__(self):
        return self._len

    def __getitem__(self, key):
        return self.get(key)

    def __delitem__(self, key):
        return self.del_(key)

    def __setitem__(self, key, value):
        self.put(key, value)


class TestLinkedHashTable(TestCase):
    def test_one_entry(self):
        m = LinkedHashTable(10)
        m.put(1, '1')
        self.assertEqual('1', m.get(1))

    def test_two_entries_with_same_hash(self):
        m = LinkedHashTable(10)
        m.put(1, '1')
        m.put(11, '11')
        self.assertEqual('1', m.get(1))
        self.assertEqual('11', m.get(11))

    def test_len_trivial(self):
        m = LinkedHashTable(10)
        self.assertEqual(0, len(m))
        for i in range(10):
            m.put(i, i)
            self.assertEqual(i + 1, len(m))

    def test_len_after_deletions(self):
        m = LinkedHashTable(10)
        m.put(1, 1)
        self.assertEqual(1, len(m))
        m.del_(1)
        self.assertEqual(0, len(m))
        m.put(11, 42)
        self.assertEqual(1, len(m))

    def test_delete_key(self):
        m = LinkedHashTable(10)
        for i in range(5):
            m.put(i, i**2)
        m.del_(1)
        self.assertEqual(None, m.get(1))
        self.assertEqual(4, m.get(2))

    def test_delete_key_and_reassign(self):
        m = LinkedHashTable(10)
        m.put(1, 1)
        del m[1]
        m.put(1, 2)
        self.assertEqual(2, m.get(1))

    def test_add_entry_bigger_than_table_size(self):
        m = LinkedHashTable(10)
        m.put(11, '1')
        self.assertEqual('1', m.get(11))

    def test_get_none_if_key_missing_and_hash_collision(self):
        m = LinkedHashTable(10)
        m.put(1, '1')
        self.assertEqual(None, m.get(11))


if __name__ == '__main__':
    unittest.main()
