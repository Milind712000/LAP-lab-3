import PySimpleGUI as sg
import os
from statHelper import getStats, extractSentences, plotFrequency


def getTxt(fpath):
    if(fpath == ''):
        # do checks to see if file path is valid
        sg.popup_annoying('Given file path is invalid')
        return ''
    ltxt = ''
    with open(fpath, "r", encoding="utf-8") as fh:
        ltxt = fh.read()
    return ltxt


def getAvoidDict(fpath):
    avoidWords = set(open(fpath, "r", encoding="utf-8").read().split())
    return avoidWords


# filepicker 1
fp1 = [
    sg.Text("Main File", size=(20, 1)),
    sg.In(key="-mainFile-"),
    sg.FileBrowse(target="-mainFile-"),
    sg.Button("Analyse", size=(10, 1))
]

# filepicker 2
fp2 = [
    sg.Text("Keywords File", size=(20, 1)),
    sg.In(key="-keyFile-"),
    sg.FileBrowse(target="-keyFile-"),
    sg.Button("Extract", size=(10, 1))
]

statBox = [
    sg.Text("Statistics", size=(20, 1)),
    sg.Multiline(key='-bigblob-', size=(100, 10))
]

grepBox = [
    sg.Text("Extracted Sentences", size=(20, 1)),
    sg.Multiline(key='-grep-', size=(100, 10))
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
    statBox,
    [sg.HSeparator()],
    fp2,
    grepBox
]

layout = [
    topControls,
    [
        sg.HSeparator()
    ],
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
avoidWords = ''
keyText = ''
stats = ''
extSnts = ''
blankFig = os.path.join(baseDir, 'img', 'blankFig.png')
histoFig = os.path.join(baseDir, 'img', 'histogram.png')
plotPath = blankFig

window = sg.Window('Text Analyze', layout, finalize=True, font="Helvetica 10")
window['-PLOT-'].Update(plotPath)

while True:  # The Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Analyse' or event == 'Refresh':
        # update txt
        ltxt = getTxt(values['-mainFile-'])
        # update avoid list
        avoidWords = getAvoidDict("words_to_avoid.txt")
        # update stats
        stats = getStats(ltxt, avoidWords)
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
