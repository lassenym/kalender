from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from datetime import date
import functools

class Eintrag:
    def __init__(self, titel, zeit, tag):
        self.titel = titel
        self.zeit = zeit
        self.tag = tag

filepath = "/home/lasse/Dokumente/Code/Kalender/savefile.txt"
event_liste = []
today = str(date.today()).split("-")

def read_txt_file(filepath):
    with open(filepath, 'r') as file:
        lines = file.read()
    return lines

def import_list():
    text = read_txt_file(filepath)
    text = text.split(";")
    text.pop()
    
    for event in text:
        event = event.split("%")
        neuer_eintrag = Eintrag(event[0], event[1], event[2])
        event_liste.append(neuer_eintrag)
        event_liste.sort(key=lambda x: x.tag)


def export_list():
    export = ""
    for event in event_liste:
        export += event.titel + "%" + event.zeit + "%" + event.tag + ";"
    with open(filepath, 'w') as file:
        file.writelines(export)
    

def sort_list():
    for event in event_liste:
        if int(event.tag) < int(today[0] + today[1] + today[2]) or event.titel == "":
            event_liste.remove(event)

    event_liste.sort(key=lambda x: x.tag)

def delete_event(i, self):
    del event_liste[i]
    export_list()
    update_list(self)


def update_list(self):

    list = self.list3
    list.setRowCount(len(event_liste))

    for i, event in enumerate(event_liste):
        list.setRowHeight(i, 80)  

        zeit_item = QTableWidgetItem(event.titel)
        font = zeit_item.font()
        font.setPointSize(14)
        zeit_item.setFont(font)

        list.setItem(i, 2, zeit_item)
        list.setItem(i, 3, QTableWidgetItem(event.zeit))
        list.setItem(i, 1, QTableWidgetItem(event.tag[6:] + "." + event.tag[4:6] + "." + event.tag[0:4]))

        delete_btn = QPushButton("Del", list)
        delete_btn.clicked.connect(functools.partial(delete_event, i, self))
        list.setCellWidget(i, 0, delete_btn)

import_list()

class Fenster(QWidget):
    def __init__(self, parent=None):
        super(Fenster, self).__init__(parent)
        self.gui()
        self.setFixedSize(self.size())
        self.setWindowIcon(QIcon('/home/lasse/Dokumente/Code/Kalender/icon.png'))
        self.setWindowTitle('SuperCal')
        self.tag.setCurrentIndex(int(today[2])-1)
        self.monat.setCurrentIndex(int(today[1])-1)
        self.jahr.setCurrentIndex(int(today[0])-2024)
        update_list(self)

    def onSelectionChanged(self):
            selected_date = self.cal.selectedDate()
            temp = selected_date.getDate()
            self.tag.setCurrentIndex(temp[2]-1)
            self.monat.setCurrentIndex(temp[1]-1)
            self.jahr.setCurrentIndex(temp[0]-2024)

    def gui(self):
        self.w1 = self
        self.w1.setAutoFillBackground(True)
        self.w1.setWindowTitle("")
        self.w1.resize(1300, 800)
        palette = self.w1.palette()
        palette.setColor(self.w1.backgroundRole(), QColor(62, 62, 62, 255))
        self.w1.setPalette(palette)
        self.w1.setCursor(Qt.ArrowCursor)
        self.w1.setToolTip("")
        self.frame1 = QWidget(self.w1)
        self.frame1.setAutoFillBackground(True)
        self.frame1.setWindowTitle("")
        self.frame1.move(20, 30)
        self.frame1.resize(380, 330)
        palette = self.frame1.palette()
        palette.setColor(self.frame1.backgroundRole(), QColor(49, 49, 49, 255))
        self.frame1.setPalette(palette)
        self.frame1.setCursor(Qt.ArrowCursor)
        self.frame1.setToolTip("")
        self.titel_input = QPlainTextEdit(self.w1)
        self.titel_input.setPlainText("")
        self.titel_input.move(120, 90)
        self.titel_input.resize(260, 50)
        self.titel_input.setCursor(Qt.ArrowCursor)
        self.titel_input.setToolTip("")
        self.label1 = QLabel(self.w1)
        self.label1.setText("Neues Event:")
        self.label1.move(150, 40)
        self.label1.resize(200, 49)
        self.label1.setFont(QFont("MS Shell Dlg 2", 20))
        palette = self.label1.palette()
        palette.setColor(self.label1.foregroundRole(), QColor(191, 191, 191, 255))
        self.label1.setPalette(palette)
        self.label1.setCursor(Qt.ArrowCursor)

        self.labelt = QLabel(self.w1)
        self.labelt.setText(str(today[2]) + "." + str(today[1]) + "." + str(today[0]))
        self.labelt.move(463, 60)
        self.labelt.resize(200, 49)
        self.labelt.setFont(QFont("MS Shell Dlg 2", 20))
        palette = self.labelt.palette()
        palette.setColor(self.labelt.foregroundRole(), QColor(240, 240, 240, 255))
        self.labelt.setPalette(palette)
        self.labelt.setCursor(Qt.ArrowCursor)
        self.labelt.setToolTip("")
        self.labeltx = QLabel(self.w1)
        self.labeltx.setText("Heute:")
        self.labeltx.move(463, 30)
        self.labeltx.resize(200, 49)
        self.labeltx.setFont(QFont("MS Shell Dlg 2", 20))
        palette = self.labeltx.palette()
        palette.setColor(self.labeltx.foregroundRole(), QColor(240, 240, 240, 255))
        self.labeltx.setPalette(palette)
        self.labeltx.setCursor(Qt.ArrowCursor)
        self.labeltx.setToolTip("")


        self.label3 = QLabel(self.w1)
        self.label3.setText("Titel")
        self.label3.move(60, 100)
        self.label3.resize(50, 22)
        self.label3.setFont(QFont("MS Shell Dlg 2", 14))
        palette = self.label3.palette()
        palette.setColor(self.label3.foregroundRole(), QColor(255, 255, 255, 255))
        self.label3.setPalette(palette)
        self.label3.setCursor(Qt.ArrowCursor)
        self.label3.setToolTip("")
        self.label4 = QLabel(self.w1)
        self.label4.setText("Zeit/\nNotizen")
        self.label4.move(40, 170)
        self.label4.resize(180, 62)
        self.label4.setFont(QFont("MS Shell Dlg 2", 14))
        palette = self.label4.palette()
        palette.setColor(self.label4.foregroundRole(), QColor(255, 255, 255, 255))
        self.label4.setPalette(palette)
        self.label4.setCursor(Qt.ArrowCursor)
        self.label4.setToolTip("")
        self.zeit_input = QPlainTextEdit(self.w1)
        self.zeit_input.setPlainText("")
        self.zeit_input.move(120, 160)
        self.zeit_input.resize(260, 90)
        self.zeit_input.setCursor(Qt.ArrowCursor)
        self.zeit_input.setToolTip("")
        self.event_neu = QToolButton(self.w1)
        self.event_neu.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.event_neu.setText("Event hinzufügen")
        self.event_neu.move(120, 300)
        self.event_neu.resize(260, 42)
        self.event_neu.setCursor(Qt.ArrowCursor)
        self.event_neu.setToolTip("")
        self.event_neu.clicked.connect(self.on_button1)
        self.tag = QComboBox(self.w1)
        self.tag.addItem("01")
        self.tag.addItem("02")
        self.tag.addItem("03")
        self.tag.addItem("04")
        self.tag.addItem("05")
        self.tag.addItem("06")
        self.tag.addItem("07")
        self.tag.addItem("08")
        self.tag.addItem("09")
        self.tag.addItem("10")
        self.tag.addItem("11")
        self.tag.addItem("12")
        self.tag.addItem("13")
        self.tag.addItem("14")
        self.tag.addItem("15")
        self.tag.addItem("16")
        self.tag.addItem("17")
        self.tag.addItem("18")
        self.tag.addItem("19")
        self.tag.addItem("20")
        self.tag.addItem("21")
        self.tag.addItem("22")
        self.tag.addItem("23")
        self.tag.addItem("24")
        self.tag.addItem("25")
        self.tag.addItem("26")
        self.tag.addItem("27")
        self.tag.addItem("28")
        self.tag.addItem("29")
        self.tag.addItem("30")
        self.tag.addItem("31")
        self.tag.move(120, 260)
        self.tag.resize(50, 22)
        self.tag.setCursor(Qt.ArrowCursor)
        self.tag.setToolTip("")
        self.monat = QComboBox(self.w1)
        self.monat.addItem("Januar (01)")
        self.monat.addItem("Februar (02)")
        self.monat.addItem("Marz (03)")
        self.monat.addItem("April (04)")
        self.monat.addItem("Mai (05)")
        self.monat.addItem("Juni (06)")
        self.monat.addItem("Juli (07)")
        self.monat.addItem("August (08)")
        self.monat.addItem("September (09)")
        self.monat.addItem("Oktober (10)")
        self.monat.addItem("November (11)")
        self.monat.addItem("Dezember (12)")
        self.monat.move(180, 260)
        self.monat.resize(130, 22)
        self.monat.setCursor(Qt.ArrowCursor)
        self.monat.setToolTip("")
        self.jahr = QComboBox(self.w1)
        self.jahr.addItem("2024")
        self.jahr.addItem("2025")
        self.jahr.addItem("2026")
        self.jahr.addItem("2027")
        self.jahr.addItem("2028")
        self.jahr.addItem("2029")
        self.jahr.addItem("2030")
        self.jahr.move(320, 260)
        self.jahr.resize(60, 22)
        self.jahr.setCursor(Qt.ArrowCursor)
        self.jahr.setToolTip("")
        self.table3 = QTableWidget(self.w1)
        self.table3.move(20, 380)
        self.table3.resize(640, 400)
        self.table3.setCursor(Qt.ArrowCursor)
        self.table3.setToolTip("")
        self.list3 = QTableWidget(self.w1)
        self.list3.move(670, 20)
        self.list3.resize(620, 760)
        self.list3.setCursor(Qt.ArrowCursor)
        self.list3.setToolTip("")
        self.list3.setColumnCount(4)
        self.list3.setColumnWidth(0, 65)
        self.list3.setColumnWidth(1, 110)
        self.list3.setColumnWidth(2, 175)
        self.list3.setColumnWidth(3, 255)
        self.list3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.list3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        column_headers = ["Löschen", "Datum", "Titel", "Zeit/Notizen"]
        self.list3.setHorizontalHeaderLabels(column_headers)
        self.list3.verticalHeader().setVisible(False)

        self.cal = QCalendarWidget(self)
        self.cal.move(20, 380)
        self.cal.resize(640, 400)
        self.cal.setGridVisible(True)
        self.cal.selectionChanged.connect(self.onSelectionChanged)

        return self.w1

    def on_w1(self):
        print('on_w1')

    def on_button1(self):
        titel_temp = str(self.titel_input.toPlainText())
        zeit_temp = str(self.zeit_input.toPlainText())
        monat_temp = str(self.monat.currentText().split('(')[1][0:2])
        
        neuer_eintrag = Eintrag(titel_temp,zeit_temp , str(self.jahr.currentText()) + monat_temp + str(self.tag.currentText()))
        print(neuer_eintrag.titel)
        event_liste.append(neuer_eintrag)
        sort_list()
        update_list(self)
        export_list()



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    a = Fenster()
    a.show()
    sys.exit(app.exec_())