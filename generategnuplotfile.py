import sublime
import sublime_plugin
from os import path
from collections import OrderedDict


class GeneratePlotFileCommand(sublime_plugin.WindowCommand):
    global callOrder
    global sets
    global viewSet
    global outputName
    global fileName
    global labelMode
    global initialized
    global splits

    def run(self):
        self.labelMode = False
        self.sets = OrderedDict()
        self.callOrder = 0
        self.viewSet = []
        self.outputName = ""
        self.initialized = False
        self.splits = 0

        self.fileName = self.window.active_view().file_name()
        self.getListOfDataSets(self.fileName)

    def setOutputName(self, input):
        if("." not in input):
            self.outputName = input
        else:
            self.outputName = input.split(".")[0]

    def getListOfDataSets(self, fileName):
        with open(fileName) as f:
            lines = (line.rstrip() for line in f)
            dLines = list(lines)
            lines = list(dLines)  # hack to get 2 sets of lines
            dataLines = list(dLine for dLine in dLines if dLine.startswith('\t'))
            if len(dataLines) is 0:
                dataLines = list(dLine for dLine in dLines if dLine.startswith(' '))
            testString = dataLines[0].split()
            if(len(testString) > 2):
                self.labelMode = True
            lines = list(line for line in lines if line.startswith('#') and '(index' in line)
            f.close()

        nameDict = {}
        for line in lines:
            split = line.split()
            tmpSet = {}
            tmpSet["name"] = split[1]
            tmpSet["number"] = -1
            tmpSet["split"] = 0
            tmpSet["id"] = split[3][:-1]
            if "(inde" in tmpSet["id"]:
                tmpSet["id"] = split[4][:-1]
            if split[1] in self.sets:
                self.sets[split[1] + "-" + str(nameDict[split[1]])] = tmpSet
                nameDict[split[1]] = nameDict[split[1]] + 1
            else:
                self.sets[split[1]] = tmpSet
                nameDict[split[1]] = 1
        if(len(self.sets) > 0):
            self.initialized = True
        else:
            self.initialized = False
        self.askUser()
        return

    def askUser(self):
        if(self.initialized):
            self.viewSet[:] = []
            self.viewSet.append("Split")
            self.viewSet.append("Finish")
            # self.viewSet.append("all")
            self.viewSet.extend(self.getInactiveSets(self.sets))
            if(len(self.viewSet) is 2):
                self.generateOutput(self.sets)
            else:
                self.window.show_quick_panel(self.viewSet, self.on_done, 1, 2)
        else:
            sublime.error_message("Not Initialized")

    def on_done(self, index):
        if index is -1:
            return
        elif index is 0:
            # self.sets[(self.viewSet[index])]["number"] = self.callOrder
            # self.sets[(self.viewSet[index])]["split"] = self.splits
            # self.callOrder = self.callOrder + 1
            if self.splits < 8:
                self.splits = self.splits + 1
                self.askUser()
            else:
                self.generateOutput(self.sets)
                return
        elif index is 1:
            self.generateOutput(self.sets)
            return
        else:
            self.sets[(self.viewSet[index])]["number"] = self.callOrder
            self.sets[(self.viewSet[index])]["split"] = self.splits
            self.callOrder = self.callOrder + 1
            self.askUser()
        return

    def getInactiveSets(self, sets):
        keys = []
        for element in self.sets:
            if(int(self.sets[element]["number"]) is -1):
                keys.append(element)
        return keys

    def getActiveSets(self, sets):
        keys = []
        for element in self.sets:
            if(int(self.sets[element]["number"]) is not -1):
                keys.append(element)
        return keys

    def getSortetSets(self):
        names = []
        numbers = []
        for element in self.sets:
            if(int(self.sets[element]["number"]) is not -1):
                names.append(element)
                numbers.append(self.sets[element]["number"])
        keys = []
        for i in range(0, self.callOrder):
            keys.extend([names[int(numbers[i])]])
        return keys

    def addAllToSets(self):
        for element in self.sets:
            self.sets[element]["number"] = self.sets[element]["id"]
        return

    def colorMap(self, size):
        colors = {}
        for i in range(1, 14):
            colors[i] = []

        colors[1].extend(['#377eb8'])
        colors[2].extend(['#e41a1c', '#377eb8'])
        colors[3].extend(['#e41a1c', '#377eb8', '#4daf4a'])
        colors[4].extend(['#e41a1c', '#377eb8', '#4daf4a', '#984ea3'])
        colors[5].extend(['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00'])
        colors[6].extend(['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02'])
        colors[7].extend(['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02', '#a6761d'])
        colors[8].extend(['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02', '#a6761d', '#666666'])
        colors[9].extend(['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#C3C300', '#a65628',
                          '#f781bf', '#999999'])
        colors[10].extend(['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f',
                           '#ff7f00', '#cab2d6', '#6a3d9a'])
        colors[11].extend(['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f',
                           '#ff7f00', '#cab2d6', '#6a3d9a', '#C3C300'])
        colors[12].extend(['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f',
                           '#ff7f00', '#cab2d6', '#6a3d9a', '#C3C300', '#b15928'])
        colors[12].extend(['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f',
                           '#ff7f00', '#cab2d6', '#6a3d9a', '#C3C300', '#b15928'])
        colors[13].extend(['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f',
                           '#ff7f00', '#cab2d6', '#6a3d9a', '#C3C300', '#b15928', '#a6cee3', '#1f78b4',
                           '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f',
                           '#ff7f00', '#cab2d6', '#6a3d9a', '#C3C300', '#b15928'])
        if size == 0:
            sublime.error_message("No Data Found!!!")
            self.initialized = False
            return colors[13]
        if size > 12:
            sublime.error_message("Using BIG Map!!!")
            return colors[13]
        else:
            return colors[size]

    def generateOutput(self, sets):
        if(self.initialized is False):
            return
        else:
            v = self.window.new_file()
            v.set_syntax_file("gnuplot.tmLanguage")

            v.retarget(path.dirname(self.fileName) + "/" + path.basename(self.fileName).split(".")[0] + ".gnuplot")
            if self.splits is 0:
                snippet = self.generateGNUSnippet()
            else:
                snippet = self.generateGNUMultiSnippet()
            v.run_command('insert_snippet', {'contents': snippet})
            self.window.active_view().run_command('save')

    def generateGNUSnippet(self):
        snippet = ""
        snippet += "#!/usr/bin/gnuplot\n"
        snippet += "reset\n\n"
        snippet += "set border linewidth 1.5\n\n"
        snippet += "set encoding utf8\n"

        keys = self.getSortetSets()

        colors = []

        colors.extend(self.colorMap(self.callOrder))

        for i in range(0, self.callOrder):
            snippet += "set style line " + str(i + 1)
            if(i < 12):
                snippet += " lc rgb '" + str(colors[i]) + "' lt 1 lw 2 pt 7 ps 1.5 "
            else:
                snippet += " lc rgb '" + str(colors[i]) + "' lt 1 lw 2 pt 4 ps 1.5 "
            snippet += "# --- " + str(keys[i]) + "\n"

        snippet += "set style line " + str(i + 2) + " lc rgb '#000000' lt 2 lw 1 # -- Legend\n\n"

        snippet += "set xlabel '${1:xlabel}'\n"
        snippet += "set ylabel '${2:ylabel}'\n"
        snippet += "set title '${3:title}'\n"

        snippet += "set grid\n"
        if(self.labelMode is False):
            snippet += "${4:# }set xrange [-1:${5:100}]\n"
        snippet += "set yrange [0:100]\n\n"

        if(self.labelMode is False):
            snippet += "${4:# }set xtics   (${6:xachsenbeschriftung})\n"
        snippet += "set ytics 5\n"

        snippet += "set key right outside top\n"
        snippet += "set key box linestyle " + str(i + 2) + "\n\n"

        snippet += "set term pngcairo size 1024,768\n"
        snippet += "set output '${7:" + path.basename(self.fileName).split(".")[0] + "}.png'\n\n"
        snippet += "plot '" + path.basename(self.fileName) + "'"
        if(self.labelMode):
            snippet += " using 1:3:xtic(2) "
        else:
            snippet += " using 1:2:xtic(1) "
        snippet += " index " + str(self.sets[keys[0]]["id"]) + " with linespoints ls 1 title '" + str(keys[0])
        if(len(keys) is 1):
            snippet += "'\n\n"
        else:
            snippet += "', \\\n"
            for i in range(1, self.callOrder):
                snippet += "\t''\t"
                if(self.labelMode):
                    snippet += " using 1:3:xtic(2) "
                else:
                    snippet += " using 1:2:xtic(1) "
                snippet += " index " + str(self.sets[keys[i]]["id"]) + " with linespoints ls "
                snippet += str(i + 1) + " title '" + str(keys[i])
                if(i is self.callOrder - 1):
                    snippet += "'\n\n"
                else:
                    snippet += "', \\\n"

        snippet += "set term postscript eps noenhanced color\n"
        snippet += "set output '${7:" + path.basename(self.fileName).split(".")[0] + "}.eps'\n\n"

        snippet += "replot"

        return snippet

    def generateGNUMultiSnippet(self):
        snippet = ""
        snippet += "#!/usr/bin/gnuplot\n"
        snippet += "reset\n\n"
        snippet += "set border linewidth 1.5\n\n"
        snippet += "set encoding utf8\n"

        keys = self.getSortetSets()
        numPerPlot = int(self.callOrder / (self.splits + 1))

        colors = []
        colors.extend(self.colorMap(numPerPlot))

        for i in range(0, numPerPlot):
            snippet += "set style line " + str(i + 1)
            if(i < 12):
                snippet += " lc rgb '" + str(colors[i]) + "' lt 1 lw 2 pt 7 ps 1.5 "
            else:
                snippet += " lc rgb '" + str(colors[i]) + "' lt 1 lw 2 pt 4 ps 1.5 "
            snippet += "# --- " + str(keys[i]) + "\n"

        snippet += "set style line " + str(i + 2) + " lc rgb '#000000' lt 2 lw 1 # -- Legend\n\n"

        snippet += "set offsets\n"
        snippet += "set autoscale fix\n"
        snippet += "set size 1,1\n"
        snippet += "set nokey\n"
        snippet += "\n"
        snippet += "set key samplen 1\n\n"

        snippet += "set macros\n"

        if(self.splits is 1):
            snippet += 'TMARGIN = "set tmargin at screen 0.95; set bmargin at screen 0.12"\n'
        elif(self.splits is 2 or self.splits is 3):
            snippet += 'TMARGIN = "set tmargin at screen 0.95; set bmargin at screen 0.55"\n'
            snippet += 'BMARGIN = "set tmargin at screen 0.52; set bmargin at screen 0.12"\n'
        elif(self.splits is 4 or self.splits is 5):
            snippet += 'TMARGIN = "set tmargin at screen 0.95; set bmargin at screen 0.69"\n'
            snippet += 'MMARGIN = "set tmargin at screen 0.66; set bmargin at screen 0.40"\n'
            snippet += 'BMARGIN = "set tmargin at screen 0.38; set bmargin at screen 0.12"\n'
        elif(self.splits is 6 or self.splits is 7):
            snippet += 'TMARGIN = "set tmargin at screen 0.95; set bmargin at screen 0.76"\n'
            snippet += 'MTMARGIN = "set tmargin at screen 0.74; set bmargin at screen 0.55"\n'
            snippet += 'MBMARGIN = "set tmargin at screen 0.53; set bmargin at screen 0.34"\n'
            snippet += 'BMARGIN = "set tmargin at screen 0.32; set bmargin at screen 0.13"\n'

        snippet += 'LMARGIN = "set lmargin at screen 0.07; set rmargin at screen 0.47"\n'
        snippet += 'RMARGIN = "set lmargin at screen 0.50; set rmargin at screen 0.90"\n\n'

        snippet += "set grid\n"
        snippet += "set term pngcairo size 1024,768\n"
        snippet += "set output '${2:" + path.basename(self.fileName).split(".")[0] + "}.png'\n\n"

        snippet += "# set term postscript eps 10 enhanced color\n"
        snippet += "# set output '${2:" + path.basename(self.fileName).split(".")[0] + "}.eps'\n\n"

        snippet += "set multiplot layout "
        if(self.splits is 1):
            splits = 2
            snippet += "2"
            macros = ["@TMARGIN; @LMARGIN", "@TMARGIN; @RMARGIN"]
            ylabs = [0]
            xlabs = [0, 1]
        elif(self.splits is 2 or self.splits is 3):
            splits = 4
            snippet += "4"
            macros = ["@TMARGIN; @LMARGIN", "@TMARGIN; @RMARGIN",
                      "@BMARGIN; @LMARGIN", "@BMARGIN; @RMARGIN"]
            ylabs = [0, 2]
            xlabs = [2, 3]
        elif(self.splits is 4 or self.splits is 5):
            snippet += "6"
            splits = 6
            macros = ["@TMARGIN; @LMARGIN", "@TMARGIN; @RMARGIN",
                      "@MMARGIN; @LMARGIN", "@MMARGIN; @RMARGIN",
                      "@BMARGIN; @LMARGIN", "@BMARGIN; @RMARGIN"]
            ylabs = [0, 2, 4]
            xlabs = [4, 5]
        elif(self.splits is 6 or self.splits is 7):
            splits = 8
            snippet += "8"
            macros = ["@TMARGIN; @LMARGIN", "@TMARGIN; @RMARGIN",
                      "@MTMARGIN; @LMARGIN", "@MTMARGIN; @RMARGIN",
                      "@MBMARGIN; @LMARGIN", "@MBMARGIN; @RMARGIN",
                      "@BMARGIN; @LMARGIN", "@BMARGIN; @RMARGIN"]
            ylabs = [0, 2, 4, 6]
            xlabs = [6, 7]

        snippet += ", 2 title '${1:title}'\n\n"

        snippet += "YLABEL='${3:ylabel}'\n"
        snippet += "XLABEL='${4:xlabel}'\n\n"

        snippet += "set key at screen 0.99, 0.95\n"
        snippet += "set key box linestyle " + str(i + 2) + "\n\n"

        if(self.labelMode is False):
            snippet += "${5:# }set xrange [-1:${5:100}]\n"
        snippet += "set yrange [0:100]\n\n"

        index = 0
        for i in range(0, splits):
            snippet += "set title 'title' offset 0,-2\n"
            if i in ylabs:
                snippet += "set ylabel YLABEL\n"
                snippet += "set format y '%.0f'\n"
            else:
                snippet += "set ylabel ''\n"
                snippet += "set format y ''\n"

            if i in xlabs:
                snippet += "set xlabel XLABEL\n"
                snippet += "set format x '%.0f'\n"
            else:
                snippet += "set xlabel ''\n"
                snippet += "set format x ''\n"

            if i is not 0:
                snippet += "unset key\n\n"
            else:
                snippet += "\n\n"

            snippet += macros[i] + "\n"

            snippet += "plot '" + path.basename(self.fileName) + "'"
            if(self.labelMode):
                snippet += " using 1:3:xtic(2) "
            else:
                if i in xlabs:
                    snippet += " using 1:2:xtic(1) "
            snippet += " index " + str(self.sets[keys[index]]["id"]) + " with linespoints ls 1"
            if i is 0:
                snippet += " title '" + str(keys[index]) + "'"
            if(numPerPlot is 1):
                snippet += "\n\n"
            else:
                snippet += ", \\\n"
            for j in range(1, numPerPlot):
                snippet += "\t''\t"
                if(self.labelMode):
                    snippet += " using 1:3:xtic(2) "
                else:
                    if i in xlabs:
                        snippet += " using 1:2:xtic(1) "
                snippet += " index " + str(self.sets[keys[index + j]]["id"]) + " with linespoints ls "
                snippet += str(j + 1)
                if i is 0:
                    snippet += " title '" + str(keys[index + j]) + "'"
                if(j is numPerPlot - 1):
                    snippet += "\n\n"
                else:
                    snippet += ", \\\n"
            index = index + numPerPlot

        snippet += "unset multiplot\n"

        return snippet
