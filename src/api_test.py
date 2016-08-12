from api import stats

testObject = stats(["abcd"])
ignoredUUID = testObject.ignoredUUIDs[0]
removedField = testObject.removedField

def test_cleanse_when_empty():
    assert testObject.cleanse([]) == []

def test_cleanse_when_other_uuids_present():
    assert testObject.cleanse([{"uuid": "1234"}]) == [{"uuid": "1234"}]

def test_cleanse_when_bad_uuids_present():
    assert testObject.cleanse([{"uuid": ignoredUUID}, {"uuid": "abcdefg"}, {"uuid": ignoredUUID}]) == [{"uuid": "abcdefg"}]

def test_cleanse_removes_ids():
    assert testObject.cleanse([{removedField: "should be removed", "anything else": "should stay", "uuid": "1234"}]) == [{"anything else": "should stay", "uuid": "1234"}]

def test_cleanse_doesNot_harm_input():
    expected = {removedField: "should still be on original", "anything else": "should also stay", "uuid": ignoredUUID}
    input = [{removedField: "should still be on original", "anything else": "should also stay", "uuid": ignoredUUID}]
    assert expected == input[0]

    testObject.cleanse(input)

    assert expected == input[0]
