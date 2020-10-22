import PySimpleGUI as sg
import os
from statHelper import getStats, extractSentences, plotFrequency

def getTxt(fpath):
	if(fpath == ''):
		# do checks to see if file path is valid
		sg.popup_annoying('Given file path is invalid')
		return ''
	ltxt = ''
	with open(fpath) as fh:
		ltxt = fh.read()
	return ltxt

# filepicker 1
fp1 = [
	sg.Text("Main File"),
	sg.In(key="-mainFile-"),
	sg.FileBrowse(target="-mainFile-"),
	sg.Button("Analyse")
]

# filepicker 2
fp2 = [
	sg.Text("Keywords File"),
	sg.In(key="-keyFile-"),
	sg.FileBrowse(target="-keyFile-"),
	sg.Button("Extract")
]

statBox = [
	sg.Text("Statistics"),
	sg.Multiline(key='-bigblob-', size=(100, 5))
]

grepBox = [
	sg.Text("Extracted Sentences"),
	sg.Multiline(key='-grep-', size=(100, 5))
]

topControls = [
	sg.Button('Refresh'), 
	sg.Button('Reset'), 
	sg.Exit()
]

histoPlot = [
	[sg.Text("Histogram")],
	[sg.Image(key="-PLOT-")]
]

leftCol = [
	fp1,
	fp2,
	statBox,
	grepBox
]

layout = [
	topControls,
	[
		sg.Column(leftCol),
		sg.VSeperator(),
		sg.Column(histoPlot)
	]
]


baseDir = os.path.dirname(os.path.realpath(__file__))
# DATA
# txt from input file
ltxt = ''
keyText = ''
stats = ''
extSnts = ''
blankFig = os.path.join(baseDir, 'img', 'blankFig.png')
histoFig = os.path.join(baseDir, 'img', 'histogram.png')
plotPath = blankFig

window = sg.Window('Text Analyze', layout, finalize=True)
window['-PLOT-'].Update(plotPath)

while True: # The Event Loop
	event, values = window.read() 
	if event == sg.WIN_CLOSED or event == 'Exit':
		break

	if event == 'Analyse' or event == 'Refresh':
		# update txt
		ltxt = getTxt(values['-mainFile-'])
		# update stats
		stats = getStats(ltxt)
		# update plot
		plotFrequency(ltxt, histoFig)
		plotPath = histoFig
	
	if event == 'Reset':
		ltxt = ''
		keyText = ''
		stats = ''
		extSnts = ''
		window['-mainFile-'].Update('')
		window['-keyFile-'].Update('')
		plotPath = blankFig

	if event == 'Extract' or event == 'Refresh':
		keyText = getTxt(values['-keyFile-'])
		extSnts = extractSentences(ltxt, keyText)

	window['-bigblob-'].Update(stats)
	window['-grep-'].Update(extSnts)
	window['-PLOT-'].Update(plotPath)
	

window.close()