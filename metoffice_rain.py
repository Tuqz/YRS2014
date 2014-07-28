import constants, urllib.request
import xml.etree.ElementTree as XMLParser

def url_gen(delta_time): #return a URL and time if successful, or False if not
	if(delta_time < 0 or delta_time > 36):
		return False
	if(delta_time % 3):
		lower = (delta_time // 3)*3
		upper = lower + 3
		if(delta_time > (lower + upper)/2):
			delta_time = upper
		else:
			delta_time = lower
	
	response = urllib.request.urlopen("http://datapoint.metoffice.gov.uk/public/data/layer/wxfcs/all/xml/capabilities?key={0}".format(constants.key))
	data = response.read()
	xml = data.decode('utf-8')
	root = XMLParser.fromstring(xml)
	
	baseURL = root[0].text
	layer_name = root[1][0][0].text
	image_format = root[1][0][1].text
	default_time = root[1][0][2].attrib['defaultTime']
	URL = baseURL.format(LayerName=layer_name, ImageFormat=image_format, DefaultTime=default_time, Timestep=delta_time, key=constants.key)
	return (URL, default_time)


print(url_gen(0))
