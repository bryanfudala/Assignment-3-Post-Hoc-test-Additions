# BRYAN FUDALA - This was my first attempt, i had no idea what i was doing.  Please see "BF_TEST.PY" for my rework
import pytest
import commands
#import barky
from database import DatabaseManager


db = DatabaseManager('bookmarks.db')

# test adding bookmark


def AddBookMarkTest():
    expecteddata = {'title': 'Mock Title',
                    'url': 'Mock Url', 'notes': 'Mock Notes'}
    db.add('bookmarks', expecteddata)
    assert db.add.bookmark('Mock Title') > 0


# test removing bookmark

def RemoveBookMarkTest():
    expecteddata = {'title': 'Mock Title',
                    'url': 'Mock Url', 'notes': 'Mock Notes'}
    db.add('bookmarks', expecteddata)
    RemoveRecord = {'title': 'Mock Title'}
    db.delete('bookmarks_Test', RemoveRecord)
    assert db.bookmark('Mock Title') < 0

# test to validate list by title (in progress)
# def ListBookMarkTest():
  # db.select(commands.ListBookmarksCommand {'id': 3}
    #assert expecteddata == pulleddata
