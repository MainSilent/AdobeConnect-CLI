import xml.etree.ElementTree as ET
from datetime import datetime

class Program:
	def __init__(self):
		# if school_program.xml does not exist, create it based on sample.xml
		file = "school_program.xml"
		try: 
			with open(file, "r", encoding="utf-8") as f:
				self.data = ET.fromstring(f.read())
		except: 
			with open(file, "w", encoding="utf-8") as f, open("lib/sample.xml", "r", encoding="utf-8") as sample:
   				data = sample.read()
   				self.data = ET.fromstring(data); f.write(data)

	def today(self):
		exist = False
		now = datetime.now()
		for day in self.data:
			if day.attrib["name"] == now.strftime("%a"):
				exist = True
				lessons = [lesson.attrib for lesson in day]
				break

		if not exist: 
			input("Can't find this day.")
			return

		return lessons