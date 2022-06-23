import unittest
import redis_testing

class TestListElements(unittest.TestCase):
    def setUp(self, N=100000, counter=1):
        self.N = N
        self.counter = counter

    def test_count_eq(self):
        outs = redis_testing.test(self.N, self.counter) 
        self.assertListEqual(outs[0], outs[1])
        self.assertListEqual(outs[2], outs[3])



if __name__ == "__main__":
    unittest.main()