
from unittest import TestCase

from pydantic import ValidationError

from days.day_4.pt_2.app import Passport


class TestPassportValidation(TestCase):

    def test_passport_validation(self):
        valid = {"pid": "087499704", "hgt": "74in", "ecl": "grn", "iyr": "2012", "eyr": "2030", "byr": "1980", "hcl": "#623a2f"}

        Passport(**valid)

        valid = {"eyr": "2029", "ecl": "blu", "cid": "129", "byr": "1989", "iyr": "2014", "pid": "896056539", "hcl": "#a97842", "hgt": "165cm"}

        Passport(**valid)

        invalid = [
            # byr
            {"eyr": "2029", "ecl": "blu", "cid": "129", "byr": "2003", "iyr": "2014", "pid": "896056539",
             "hcl": "#a97842", "hgt": "165cm"},

            # hgt - in
            {"eyr": "2029", "ecl": "blu", "cid": "129", "byr": "1989", "iyr": "2014", "pid": "896056539",
             "hcl": "#a97842", "hgt": "190in"},

            # hgt
            {"eyr": "2029", "ecl": "blu", "cid": "129", "byr": "1989", "iyr": "2014", "pid": "896056539",
             "hcl": "#a97842", "hgt": "190"},

            # hcl
            {"eyr": "2029", "ecl": "blu", "cid": "129", "byr": "1989", "iyr": "2014", "pid": "896056539",
             "hcl": "#123abz", "hgt": "165cm"},

            # hcl
            {"eyr": "2029", "ecl": "blu", "cid": "129", "byr": "1989", "iyr": "2014", "pid": "896056539",
             "hcl": "123abc", "hgt": "165cm"},

            # ecl
            {"eyr": "2029", "ecl": "wat", "cid": "129", "byr": "2002", "iyr": "2014", "pid": "896056539",
             "hcl": "#a97842", "hgt": "165cm"},

            # pid
            {"eyr": "2029", "ecl": "brn", "cid": "129", "byr": "2002", "iyr": "2014", "pid": "0123456789",
             "hcl": "#a97842", "hgt": "165cm"},
        ]

        for inv in invalid:
            with self.assertRaises(ValidationError):
                Passport(**inv)
