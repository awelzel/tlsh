import unittest
import threading
import time
import statistics

import tlsh

class TlshCase(unittest.TestCase):

    def setUp(self):
        self.h1 = "a" * 70
        self.h2 = "b" * 70

    def test_tlsh_diff__arg1_error(self):
        with self.assertRaisesRegex(ValueError, "not a TLSH hex string"):
            tlsh.diff("a", self.h2)

    def test_tlsh_diff__arg2_error(self):
        with self.assertRaisesRegex(ValueError, "not a TLSH hex string"):
            tlsh.diff(self.h1, "b")

    def test_tlsh_diff__arg1_type(self):
        with self.assertRaisesRegex(TypeError, "must be str"):
            tlsh.diff(1, self.h2)

    def test_tlsh_diff__arg2_type(self):
        with self.assertRaisesRegex(TypeError, "must be str"):
            tlsh.diff(self.h1, 1)

    def test_tlsh_diffxlen__arg1_error(self):
        with self.assertRaisesRegex(ValueError, "not a TLSH hex string"):
            tlsh.diffxlen("a", self.h2)

    def test_tlsh_diffxlen__arg2_error(self):
        with self.assertRaisesRegex(ValueError, "not a TLSH hex string"):
            tlsh.diffxlen(self.h1, "b")

    def test_tlsh_diffxlen__arg1_type(self):
        with self.assertRaisesRegex(TypeError, "must be str"):
            tlsh.diffxlen(1, self.h2)

    def test_tlsh_diffxlen__arg2_type(self):
        with self.assertRaisesRegex(TypeError, "must be str"):
            tlsh.diffxlen(self.h1, 1)

    def test_tlsh_diff__same(self):
        diff = tlsh.diff(self.h1, self.h1)
        self.assertEqual(0, diff)

    def test_tlsh_diff__different(self):
        diff = tlsh.diff(self.h1, self.h2)
        self.assertEqual(271, diff)

    def test_tlsh_diffxlen__same(self):
        diff = tlsh.diffxlen(self.h1, self.h1)
        self.assertEqual(0, diff)

    def test_tlsh_diffxlen__diff(self):
        diff = tlsh.diffxlen(self.h1, self.h2)
        self.assertEqual(67, diff)

    def test_threaded(self):
        """
        Run a threads for 1 second and count the number of calls made.
        """
        tc = self
        class Cruncher(threading.Thread):

            def run(self):
                self.done = 0
                start = time.time()
                while True:
                    if (self.done % 100) == 0:
                        if time.time() - start > 2.0:
                            break

                    tlsh.diff(tc.h1, tc.h2)
                    tlsh.diffxlen(tc.h1, tc.h2)
                    self.done += 2

        print()
        for n in [1, 2, 4, 8]:
            threads = [Cruncher() for _ in range(n)]
            start = time.time()
            [t.start() for t in threads]
            join_start = time.time()
            [t.join() for t in threads]
            end = time.time()
            counts = [t.done for t in threads]
            mean = statistics.mean(counts)
            stdev = statistics.stdev(counts) if len(counts) > 1 else 0
            print(("avg {} tlsh.diff() calls per thread (stddev={:.1f}/{:.1f}% threads={})"
                   " {:.3f}s Thread.start() {:.3f}s Thread.join()").format(
                mean, stdev, stdev / mean * 100, len(threads),
                join_start - start, end - join_start))
