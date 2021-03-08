# BRYAN FUDALA - REWORK OF ASSIGNMENT 3
import pytest
import commands
from database import DatabaseManager

import os
from datetime import datetime
import sqlite3


@pytest.fixture
def db() -> DatabaseManager:
    filename = "bookmark_table_test.db"
    dbm = DatabaseManager(filename)
    yield dbm
    dbm.__del__()
    # I have been turning this on and off below in order to to run manual tests to validate my automated tests....
    os.remove(filename)


def test_create_table(db):
    db.create_table(
        "bookmarks",
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null",
        },
    )

    conn = db.connection
    cursor = conn.cursor()

    cursor.execute(
        ''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='bookmarks' ''')

    assert cursor.fetchone()[0] == 1


def test_add_record(db):
    db.create_table(
        "add_bookmark_test",
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null",
        },
    )

    data = {
        "title": "this is only a test",
        "url": "http://google.com",
        "notes": "i need to take better notes",
        "date_added": datetime.utcnow().isoformat()}
    db.add("add_bookmark_test", data)

    conn = db.connection
    cursor = conn.cursor()
    cursor.execute(
        ''' SELECT * FROM add_bookmark_test WHERE title="this is only a test" ''')
    assert cursor.fetchone()[0] > 0


def test_delete_record(db):
    db.create_table(
        "delete_bookmark_test",
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null",
        },
    )
    data = {
        "title": "this is a test to delete",
        "url": "http://delete.com",
        "notes": "i would like to delete this record",
        "date_added": datetime.utcnow().isoformat()}
    db.add("delete_bookmark_test", data)

    x = {"title": "this is a test to delete"}
    db.delete("delete_bookmark_test", x)

    conn = db.connection
    cursor = conn.cursor()

    cursor.execute(
        ''' SELECT count(title) FROM "delete_bookmark_test" WHERE title='this is a test to delete' ''')

    assert cursor.fetchone()[0] == 0


def test_select_record(db):
    db.create_table(
        "select_bookmark_test",
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null",
        },
    )

    data = {
        "title": "please select this record",
        "url": "http://pickme.com",
        "notes": "i would like to select this record",
        "date_added": datetime.utcnow().isoformat()}
    db.add("select_bookmark_test", data)

    x = {"title": "please select this record"}
    y = x["title"]

    select_x = db.select("select_bookmark_test", x).fetchone()[1]
    assert select_x == y


def test_edit_record(db):
    db.create_table(
        "edit_bookmark_test",
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null",
        },
    )
    data = {
        "title": "please edit this record",
        "url": "http://edit.com",
        "notes": "i would like to edit this record",
        "date_added": datetime.utcnow().isoformat()}
    db.add("edit_bookmark_test", data)

    x = {"title": "please edit this record"}

    conn = db.connection
    cursor = conn.cursor()
    cursor.execute(
        ''' UPDATE 'edit_bookmark_test' SET notes ="record is now updated" WHERE title='please edit this record' ''')
    conn.commit()

    cursor.execute(
        ''' SELECT count(title) FROM "edit_bookmark_test" WHERE title='please edit this record' and notes='record is now updated' ''')
    assert cursor.fetchone()[0] > 0
