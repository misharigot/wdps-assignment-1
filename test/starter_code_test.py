from starter_code import Executor


def test_end_to_end():
    executor = Executor()
    data = executor.execute("/app/assignment/data/sample.warc.gz", max_iterations=5)
    assert data.size > 0
