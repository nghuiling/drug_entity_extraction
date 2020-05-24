from flask import Flask,url_for,render_template,request
import spacy
from spacy import displacy
import json
from waitress import serve


nlp = spacy.load('en_core_med7_lg')

HTML_WRAPPER = """<div style="overflow-x: auto">{}</div>"""

from flaskext.markdown import Markdown

app = Flask(__name__)
Markdown(app)



@app.route('/', methods=['GET','POST'])
def home():	
	return render_template('index.html')


@app.route('/extract',methods=['GET','POST'])
def extract():

	col_dict = {}
	seven_colours = ['#f58231', '#FF2828','#66D69C', '#ffe119', '#ffd8b1',  '#f032e6', '#42d4f4']
	for label, colour in zip(nlp.pipe_labels['ner'], seven_colours):
		col_dict[label] = colour
	options = {'ents': nlp.pipe_labels['ner'], 'colors':col_dict}

	raw_text = request.form['rawtext']
	docx = nlp(raw_text)
	html = displacy.render(docx,style="ent",options=options)
	html = html.replace("\n\n","\n")
	result = HTML_WRAPPER.format(html)

	return render_template('result.html',rawtext=raw_text,result=result)



if __name__ == '__main__':
   # app.run(debug=True)
   serve(app, host='0.0.0.0', port=8000)