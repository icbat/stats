from api import stats

testObject = stats(["abcd"])

def test_remove_ignored_uuids_when_empty():
    assert testObject.remove_ignored_uuids([]) == []

def test_remove_ignored_uuids_when_other_uuids_present():
    assert testObject.remove_ignored_uuids([{"uuid": "1234"}]) == [{"uuid": "1234"}]

def test_remove_ignored_uuids_when_bad_uuids_present():
    assert testObject.remove_ignored_uuids([{"uuid": "abcd"}, {"uuid": "abcdefg"}, {"uuid": "abcd"}]) == [{"uuid": "abcdefg"}]

def test_remove_internal_ids_when_empty():
    assert testObject.remove_internal_ids([]) == []

def test_remove_internal_ids_removes_ids():
    assert testObject.remove_internal_ids([{"_id": "should be removed", "anything else": "should stay"}]) == [{"anything else": "should stay"}]

def test_remove_internal_ids_doesNot_harm_input():
    expected = {"_id": "should still be on original", "anything else": "should also stay"}
    input = [{"_id": "should still be on original", "anything else": "should also stay"}]
    assert expected == input[0]

    testObject.remove_internal_ids(input)

    assert expected == input[0]
