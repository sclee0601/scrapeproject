import json


class Bill():
    bill_pk = ""
    bill_number = ""
    bill_title = ""
    chamber_intro = ""
    summary = ""
    chief_patron = ""
    district = ""
    house_patrons = ""
    senate_patrons = ""
    fulltext_i = ""
    fulltext_p = ""
    session = ""

    def __init__(self, bill_pk, bill_number, bill_title, chamber_intro, summary, chief_patron, district, house_patrons, senate_patrons,fulltext_i,fulltext_p, session):
        self.bill_pk = bill_pk
        self.bill_number = bill_number
        self.bill_title = bill_title
        self.chamber_intro = chamber_intro
        self.summary = summary
        self.chief_patron = chief_patron
        self.district = district
        self.house_patrons = house_patrons
        self.senate_patrons = senate_patrons
        self.fulltext_i = fulltext_i
        self.fulltext_p = fulltext_p
        self.session = session

    def __str__(self):
        return "Bill Number: " + self.bill_number

    def __init__(self, dictionary):
        self.__dict__.update(dictionary)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


