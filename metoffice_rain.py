import constants, urllib2

response = urllib2.urlopen("http://datapoint.metoffice.gov.uk/public/data/layer/wxfcs/all/xml/capabilities?key={0}".format(constants.key))
xml = response.read()

print(xml)
