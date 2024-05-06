from flask import Flask, render_template, request, redirect, url_for
from LastTenKAnalyzer import getData

app = Flask(__name__)

stockticker = "PFE"
# Get the data for both companies
finalData = getData()

@app.route('/', methods=["POST","GET"])
def base_page():
	"""
	This function displays the base page of the web app that asks the user to input
	either $PFE or $ZM to view the company's financial information.
	"""
	if request.method == "POST":
		stockticker = request.form["stockticker"]
		if stockticker == "$PFE":
			return redirect(url_for("pfe_page"))
		elif stockticker == "$ZM":
			return redirect(url_for("zm_page"))
		else:
			return render_template('index.html', error=True)
	return render_template('index.html')
	
	
@app.route('/$PFE')
def pfe_page():
	"""
	This function displays the page containing the financial information of Pfizer
	and the associated analysis.
	"""
	# Display data and analysis for Pfizer
	PFERev = finalData["PFERev"]
	# Collect revenue data for Pfizer in a list of tuples to be used in Chart JS
	data = [(k, v) for k, v in PFERev.items()]
	labels = [row[0] for row in data]
	values = [row[1] for row in data]
	# Collect net income data for Pfizer in a list of tuples to be used in Chart JS
	PFENet = finalData["PFENet"]
	data2 = [(k, v) for k, v in PFENet.items()]
	labels2 = [row[0] for row in data2]
	values2 = [row[1] for row in data2]
	PFEAnalysis = finalData["PFEResponse"]
	PFEAnalysis = PFEAnalysis.replace("*", "")
	PFEAnalysis = PFEAnalysis.replace("#", "")
	return render_template("testing.html", labels=labels, values=values, labels2=labels2, values2=values2, analysis=PFEAnalysis)

@app.route('/$ZM')
def zm_page():
	"""
	This function displays the page containing the financial information of Zoom
	and the associated analysis.
	"""
	# Display data and analysis for Zoom
	ZMRev = finalData["ZMRev"]
	# Collect revenue data for Zoom in a list of tuples to be used in Chart JS
	data = [(k, v) for k, v in ZMRev.items()]
	labels = [row[0] for row in data]
	values = [row[1] for row in data]
	ZMNet = finalData["ZMNet"]
	# Collect net income data for Zoom in a list of tuples to be used in Chart JS
	data2 = [(k, v) for k, v in ZMNet.items()]
	labels2 = [row[0] for row in data2]
	values2 = [row[1] for row in data2]
	ZMAnalysis = finalData["ZMResponse"]
	ZMAnalysis = ZMAnalysis.replace("*", "")
	ZMAnalysis = ZMAnalysis.replace("# #", "")
	ZMAnalysis = ZMAnalysis.replace("#", "")
	return render_template("testing2.html", labels=labels, values=values, labels2=labels2, values2=values2, analysis=ZMAnalysis)

if __name__ == "__main__":
	app.run(debug=True)
