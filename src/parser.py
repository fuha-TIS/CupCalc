import xml.etree.ElementTree as ET

class Parser():
    """ Handles data parsing from XML.
        self.event_data - contains information about the Event
        self.runners_data - contains runner information
        self.class_count - pocet kategorii na behu"""

    def __init__(self, file):
        self._tree = ET.parse(file)
        self.root = self._tree.getroot()
        self.class_count = 0
        self.event_data  = {}
        self.runners_data = {}
        self.collect_event_data ()
        self.collect_runners_data()
        self.collect_runners_data()

    def collect_event_data(self):
        """ Collects the information about the event.
            Name, EventClassificationID, StartDate[Date, Clock]"""
        event = self.get_event()
        for child in event:
            if child.tag == 'Name':
                self.event_data['name'] = child.text
            elif child.tag == 'EventClassificationId':
                self.event_data['eventclassificationid'] = child.text
            elif child.tag == 'StartDate':
                self.parse_startdate(child)

    def get_event(self):
        """ Return the event tag, with info about the run."""
        for child in self.root:
            if child.tag == 'Event':
                event = child
        return event

    def parse_startdate(self, child):
        """ Add Date and Clock, to event information. """
        for time in child:
            if time.tag == 'Date':
                self.event_data ['date'] = time.text
            elif time.tag == 'Clock':
                self.event_data ['clock'] = time.text

    def collect_runners_data(self):
        """ Collect the data about the runners, from different,
            classes. """
        for child in self.root:
            if child.tag == 'ClassResult':
                self.handle_classresults(child)
                self.class_count += 1

    def handle_classresults(self, classresult_tag):
        """ Fills the classresults_data dictionaru.
            'class_name': 'person_01(dictionaty info about runner)', 'person_02';...
            """
        for child in classresult_tag:
            if child.tag == 'ClassShortName':
                csn = child.text
                self.runners_data[csn] = []
            elif child.tag == 'PersonResult':
                self.runners_data[csn].append(self.get_personresult(child))

    def get_personresult(self, classresult):
        """ Main handler for parsing data. Each tag is processed.
            Return the data about the runners. """
        person_info = {}
        for person_result in classresult:
            if person_result.tag == "Person":
                self.parse_person_tag(person_info ,person_result)
            elif person_result.tag == "Club":
                self.parse_club_tag(person_info, person_result)
            elif person_result.tag == 'Result':
                self.parse_result_tag(person_info, person_result)
        return person_info

    def parse_person_tag(self, person_info, person_result):
        """ Enters the PersonName tag, after that send the data,
            to collect_name... to add name & surname about runner"""
        for person in person_result:
            if person.tag == "PersonName":
                self.add_name_and_surname(person_info, person)

    def add_name_and_surname(self, person_info, person):
        """ Adds name and surname about the runner, to the dictionary. """
        for name in person:
            if name.tag == "Family":
                person_info['meno'] = name.text
            elif name.tag == "Given":
                person_info['priezvisko'] = name.text

    def parse_club_tag(self, person_info, person_result):
        """ Adds club name to person dictionary. """
        for club in person_result:
            if club.tag == 'ShortName':
                person_info['club'] = club.text

    def parse_result_tag(self, person_info, person_result):
        """ Handles parsing of Result tag. """
        for result in person_result:
            if result.tag == "CCard":
                self.add_ccard(person_info, result)
            elif result.tag == 'StartTime':
                self.add_starttime(person_info, result)
            elif result.tag == 'FinishTime':
                self.add_finishtime(person_info, result)
            elif result.tag == 'Time':
                person_info['time'] = result.text
            elif result.tag == 'ResultPosition':
                person_info['position'] = result.text
            elif result.tag == "CompetitorStatus":
                person_info['status'] = result.attrib['value']
            elif result.tag == "CourseLength":
                person_info['courselength'] = result.text
            elif result.tag == "SplitTime":
                self.add_splittime(person_info, result)

    def add_ccard(self, person_info, result):
        """ Adds ccard to person dictionary. """
        for ccard in result:
            person_info['ccard'] = ccard.text

    def add_starttime(self, person_info, result):
        """ Adds startime to person dictionary. """
        for starttime in result:
            person_info['starttime'] = starttime.text

    def add_finishtime(self, person_info, result):
        """ Adds finishtime to person dictionary. """
        for finishtime in result:
            person_info['finishtime'] = finishtime.text

    def add_splittime(self, person_info, result):
        """ Adds tuple(ControlCode, Time), to person dictionary under key
            splittime_seq_index. """
        controlcode, time = None, None
        for splittime in result:
            if splittime.tag == "ControlCode":
                controlcode = splittime.text
            elif splittime.tag == "Time":
                time = splittime.text
        person_info['splitime_seq_' + str(result.attrib['sequence'])] = (controlcode, time)

# Potrebuje vstupny parameter xml subor
Parser()
