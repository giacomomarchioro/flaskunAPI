from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World!'

@app.route('/unapi')
def unapi():
	el_id = request.args.get('id',None)
	el_format = request.args.get('format',None)
	import xml.etree.ElementTree as ET

	root = ET.Element('formats')
	child = ET.SubElement(root, 'format')
	child.set("name","oai_dc") 
	child.set("type","application/xml")
	child.set("docs","http://www.openarchives.org/OAI/2.0/oai_dc.xsd")
	# add your data to the root node in the format you want
	return app.response_class(b"""<?xml version="1.0" encoding="UTF-8"?>"""+ET.tostring(root), mimetype='application/xml')

if __name__  == '__main__':
	app.run(debug=True)