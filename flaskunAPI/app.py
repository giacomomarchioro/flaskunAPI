from flask import Flask, request,url_for
from flask.templating import render_template
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World!'

responde = """
<rdf:RDF
 xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
 xmlns:res="http://purl.org/vocab/resourcelist/schema#"
 xmlns:z="http://www.zotero.org/namespaces/export#"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:bibo="http://purl.org/ontology/bibo/"
 xmlns:address="http://schemas.talis.com/2005/address/schema#"
 xmlns:foaf="http://xmlns.com/foaf/0.1/">
    <z:UserItem rdf:about="http://zotero.org/users/local/ptD7P9CK/items/C6WTTNN3">
        <res:resource rdf:resource="ark:23412"/>
        <z:repository>scaffale desrea</z:repository>
        <dcterms:rights>Diritti aperti</dcterms:rights>
    </z:UserItem>
    <bibo:Manuscript rdf:about="ark:23412">
        <dcterms:title>brevitate vite</dcterms:title>
        <dcterms:date>1234</dcterms:date>
        <dcterms:language>latino</dcterms:language>
        <z:repository>Fondo manoscritti che non ci sono</z:repository>
        <dcterms:source>[vii ]</dcterms:source>
        <bibo:lccn>XVVii</bibo:lccn>
        <bibo:uri>ark:23412</bibo:uri>
        <z:extra>Code: brevitate vite
Publication Title: brevitate vite
Reporter: brevitate vite</z:extra>
        <dcterms:publisher>
            <foaf:Organization>
               <address:localityName>verona</address:localityName>
            </foaf:Organization>
        </dcterms:publisher>
        <bibo:numPages>342</bibo:numPages>
        <dcterms:type>manuscript</dcterms:type>
        <dcterms:creator rdf:nodeID="n15"/>
        <bibo:authorList>
           <rdf:Seq><rdf:li rdf:nodeID="n15"/></rdf:Seq>
        </bibo:authorList>
    </bibo:Manuscript>
    <foaf:Person rdf:nodeID="n15">
        <foaf:givenName>agostino</foaf:givenName>
        <foaf:surname>ippona</foaf:surname>
    </foaf:Person>
</rdf:RDF>
"""

database = {
"urn:isbn:123456789X" : {'title':'test book'}}

database = {
"urn:isbn:123456789X" : responde,
"urn:isbn:123456789B" : responde,
"urn:isbn:123456789C" : responde,
}

@app.route('/unapi')
def unapi():
	el_id = request.args.get('id',None)
	el_format = request.args.get('format',None)
	if el_id is not None:
		obj = database[el_id]
		return app.response_class(obj, mimetype='application/xml')
	
	import xml.etree.ElementTree as ET
	root = ET.Element('formats')
	child = ET.SubElement(root, 'format')
	child.set("name","oai_dc") 
	child.set("type","application/xml")
	child.set("docs","http://www.openarchives.org/OAI/2.0/oai_dc.xsd")
	rdf = ET.SubElement(root, 'format')
	rdf.set("name","rdf_bibliontology") 
	rdf.set("type","application/xml")
	rdf.set("docs","https://raw.githubusercontent.com/structureddynamics/Bibliographic-Ontology-BIBO/master/bibo.owl")
	# add your data to the root node in the format you want
	return app.response_class(b"""<?xml version="1.0" encoding="UTF-8"?>"""+ET.tostring(root), mimetype='application/xml')

@app.route('/example1')
def example1():
	return render_template('example_1.html')

@app.route('/many_ID')
def many_ID():
	return render_template('many_ID.html')

if __name__  == '__main__':
	app.run(debug=True)