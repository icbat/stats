from api import stats
from time import time

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

def test_daily_when_empty():
    input = []

    actual = testObject.daily_totals(input)

    assert actual["data"] == []
    assert actual['labels'] == []

def test_daily_when_all_one_day():
    input = [{"timestamp": 111, "otherThing": "stillHere"}]

    actual = testObject.daily_totals(input)

    assert actual["data"] == [1]
    assert actual['labels'] == [0]

def test_daily_with_different_days():
    input = [{"timestamp": 111, "otherThing": "stillHere"}, {"timestamp": 86423, "otherThing": "stillHere"}]

    actual = testObject.daily_totals(input)

    assert actual["data"] == [1,1]
    assert actual['labels'] == [0, 86400]

def test_daily_groups_days_together():
    input = [{"timestamp": 111, "otherThing": "stillHere"}, {"timestamp": 123, "otherThing": "stillHere"}]

    actual = testObject.daily_totals(input)

    assert actual["data"] == [2]
    assert actual['labels'] == [0]

def test_daily_sorts():
    input = [{"timestamp": 86423, "otherThing": "stillHere"}, {"timestamp": 111, "otherThing": "stillHere"}, {"timestamp": 123, "otherThing": "stillHere"}]

    actual = testObject.daily_totals(input)

    assert actual["data"] == [2,1]
    assert actual['labels'] == [0, 86400]

def test_fromToday_filters_older_days():
    input = [{"timestamp": time(), "score": 3}, {"timestamp": 0, "score": 4}];

    actual = testObject.from_today(input)

    assert actual["data"][0]["score"] == 3
    assert len(actual["data"]) == 1
