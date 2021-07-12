import unittest, os, ast

argList1 = ["Resources/courses.csv", "Resources/marks.csv", "Resources/students.csv", "Resources/tests.csv",
            "output_test.json"]
argList2 = ["Resources/courses.csv", "Resources/marks.csv", "Resources/students.csv", "Resources/tests1.csv",
            "output_test.json"]


# test1 has a problem with the sum of weights

class TestSum(unittest.TestCase):
    def test_output(self):
        out = os.popen('python main.py {}'.format(" ".join(argList1))).read().rstrip()
        out = ast.literal_eval(out)
        out2 = os.popen('python main.py {}'.format(" ".join(argList2))).read().rstrip()
        out2 = ast.literal_eval(out2)
        self.assertEqual(out, {'students': [{'id': 1, 'name': 'A', 'totalAverage': 72.03, 'courses': [
            {'id': 1, 'name': 'Biology', 'teacher': 'Mr. D', 'courseAverage': 90.1},
            {'id': 2, 'name': 'History', 'teacher': 'Mrs. P', 'courseAverage': 51.8},
            {'id': 3, 'name': 'Math', 'teacher': 'Mrs. C', 'courseAverage': 74.2}]},
                                            {'id': 2, 'name': 'B', 'totalAverage': 62.15, 'courses': [
                                                {'id': 1, 'name': 'Biology', 'teacher': 'Mr. D', 'courseAverage': 50.1},
                                                {'id': 3, 'name': 'Math', 'teacher': 'Mrs. C', 'courseAverage': 74.2}]},
                                            {'id': 3, 'name': 'C', 'totalAverage': 72.03, 'courses': [
                                                {'id': 1, 'name': 'Biology', 'teacher': 'Mr. D', 'courseAverage': 90.1},
                                                {'id': 2, 'name': 'History', 'teacher': 'Mrs. P',
                                                 'courseAverage': 51.8}, {'id': 3, 'name': 'Math', 'teacher': 'Mrs. C',
                                                                          'courseAverage': 74.2}]}]})
        self.assertEqual(out2, {'error': 'Invalid course weights'})


if __name__ == '__main__':
    unittest.main()
