import constants, urllib.request, datetime
import xml.etree.ElementTree as XMLParser

class MetOffice:
	def __init__(self):
		response = urllib.request.urlopen("http://datapoint.metoffice.gov.uk/public/data/layer/wxfcs/all/xml/capabilities?key={0}".format(constants.key))
		data = response.read()
		self.xml = data.decode('utf-8')
		default_time = root[index][0][2].attrib['defaultTime']
		self.xml_time = datetime.datetime(int(default_time[:4]), int(default_time[5:7]), int(default_time[8:10]), int(default_time[11:13]), int(default_time[14:16]), int(default_time[17:19]))
		self.keys = [1, 4]
	
	def update(self):
		response = urllib.request.urlopen("http://datapoint.metoffice.gov.uk/public/data/layer/wxfcs/all/xml/capabilities?key={0}".format(constants.key))
		data = response.read()
		self.xml = data.decode('utf-8')
		self.xml_time = datetime.datetime(int(default_time[:4]), int(default_time[5:7]), int(default_time[8:10]), int(default_time[11:13]), int(default_time[14:16]), int(default_time[17:19]))
	
	def url_gen(time, forecast): #Take a datetime for the desired time and a forecast type - 0 for rain, 1 for temperature
		root = XMLParser.fromstring(self.xml)
		
		baseURL = root[0].text
		index = self.keys[forecast]
		layer_name = root[index][0][0].text
		image_format = root[index][0][1].text
		default_time = root[index][0][2].attrib['defaultTime']
		delta_time = time - self.xml_time
		delta_time = (delta_time.days * 24) + (delta_time.seconds//3600)
		if(delta_time < 0 or delta_time > 36):
			return False
		if(time % 3):
			lower = (delta_time//3)*3
			upper = lower + 3
			if(delta_time > (lower + upper)/2):
				delta_time = upper
			else:
				delta_time = lower
	
		URL = baseURL.format(LayerName=layer_name, ImageFormat=image_format, DefaultTime=default_time, Timestep=time, key=constants.key)
		return URL

