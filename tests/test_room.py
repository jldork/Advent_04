from unittest import TestCase
from expects import expect, equal, be_true, be_false
from room import Room, validate

class TestRoom(TestCase):
    def test_can_break_name_to_parts(self):
        room = Room('aaaaa-bbb-z-y-x-1243[afdbxyz]')
        expect(room.name).to(equal('aaaaa-bbb-z-y-x'))
        expect(room.sector_id).to(equal(1243))
        expect(room.checksum).to(equal('afdbxyz'))

    def test_can_be_validated(self):
        expect(validate(Room('aaaaa-bbb-z-y-x-123[abxyz]'))).to(be_true)
        expect(validate(Room('a-b-c-d-e-f-g-h-987[abcde]'))).to(be_true)
        expect(validate(Room('not-a-real-room-404[oarel]'))).to(be_true)
        expect(validate(Room('totally-real-room-200[decoy]'))).to(be_false)