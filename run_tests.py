
# ==========================================
# BIGMAN — CENTRAL TEST RUNNER
# ==========================================

import unittest
import sys


def run_all_tests():

    print("=" * 50)
    print("       BIGMAN SYSTEM TEST RUNNER")
    print("=" * 50)

    loader = unittest.TestLoader()

    test_suite = loader.discover(
        start_dir="tests",
        pattern="test_*.py"
    )

    runner = unittest.TextTestRunner(
        verbosity=2
    )

    result = runner.run(test_suite)

    print("\n" + "=" * 50)
    print("             TEST SUMMARY")
    print("=" * 50)

    print("Tests executed:", result.testsRun)
    print("Failures:", len(result.failures))
    print("Errors:", len(result.errors))

    if result.wasSuccessful():
        print("\nBIGMAN TEST STATUS: ALL TESTS PASSED")
        return 0

    print("\nBIGMAN TEST STATUS: TESTS FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
