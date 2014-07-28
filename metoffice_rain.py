import constants, urllib.request, datetime
import xml.etree.ElementTree as XMLParser

def url_gen(desired_date): #return a URL if successful, or False if not
	response = urllib.request.urlopen("http://datapoint.metoffice.gov.uk/public/data/layer/wxfcs/all/xml/capabilities?key={0}".format(constants.key))
	data = response.read()
	xml = data.decode('utf-8')
	root = XMLParser.fromstring(xml)
	
	baseURL = root[0].text
	layer_name = root[1][0][0].text
	image_format = root[1][0][1].text
	default_time = root[1][0][2].attrib['defaultTime']
	
	xml_gen = datetime.datetime(int(default_time[:4]), int(default_time[5:7]), int(default_time[8:10]), int(default_time[11:13]), int(default_time[14:16]), int(default_time[17:19]))
	delta_time = desired_date - xml_gen
	delta_time = delta_time.seconds//3600 + delta_time.days*24
	if(delta_time < 0 or delta_time > 36):
		return False
	if(delta_time % 3):
		lower = (delta_time//3)*3
		upper = lower + 3
		if(delta_time > (lower + upper)/2):
			delta_time = upper
		else:
			delta_time = lower
	
	URL = baseURL.format(LayerName=layer_name, ImageFormat=image_format, DefaultTime=default_time, Timestep=0, key=constants.key)
	return URL

