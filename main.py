import sys, time
from functools import partial
import xml.etree.ElementTree as ET
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QUrl, Qt
from pyfirmata import Arduino, util

class Finestra(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("pantalles/principal.ui", self)
        self.botoGit.clicked.connect(self.github)
        self.botoAplicacio.clicked.connect(self.app)
        self.MontarPorts()

    def MontarPorts(self):
        tree = ET.parse('ports.xml')
        self.root = tree.getroot()
        self.rPort_0.setText(self.root[0][0].text)
        self.rPort_1.setText(self.root[0][1].text)
        self.rPort_2.setText(self.root[0][2].text)
        self.rPort_3.setText(self.root[0][3].text)
        self.rPort_4.setText(self.root[0][4].text)

    def github(self):
        QDesktopServices.openUrl(QUrl("https://github.com/joseprplana/ArduinoPy.git"))

    def app(self):
        port = ""
        if self.rPort_0.isChecked(): port = self.root[0][0].text
        elif self.rPort_1.isChecked(): port = self.root[0][1].text
        elif self.rPort_2.isChecked(): port = self.root[0][2].text
        elif self.rPort_3.isChecked(): port = self.root[0][3].text
        elif self.rPort_4.isChecked(): port = self.root[0][4].text
        self.appNano = AplicacioNano(port)
        self.appNano.exec_()

class AplicacioNano(QDialog):
    def __init__(self, port):
        self.marxa = QPixmap('imatges/verd.png')
        self.paro = QPixmap('imatges/vermell.png')
        QDialog.__init__(self)
        uic.loadUi("pantalles/appNano.ui", self)
        self.etqPort.setText("Port: " + port)
        self.botoConectar.clicked.connect(partial(self.Conecta, port = port))
        self.Inicials()
        self.Conexions()

    def Conecta(self, port):
        marxa = QPixmap('imatges/verd.png')
        paro = QPixmap('imatges/vermell.png')
        try:
            if self.botoConectar.text() == "Conecta la Placa":
                self.board = Arduino(port)
                if self.board != "":
                    time.sleep(0.5)
                    self.etqOnOff.setPixmap(marxa)
                    self.etqEstat.setText("Estat: Conectat")
                    self.botoConectar.setText("Desconecta la Placa")
            else:
                self.board.exit()
                self.etqOnOff.setPixmap(paro)
                self.etqEstat.setText("Estat: Desconectat")
                self.botoConectar.setText("Conecta la Placa")
                self.etqEstat.setText("Estat: Desconectat")
        except Exception as e:
            QMessageBox.information(self, "Avis", "Placa no Trobada", QMessageBox.Ok)

    def Conexions(self):
        self.desa_2.clicked.connect(partial(self.DesaPin, estat = self.root[1][2].text), canal = 'pin2')

    def Inicials(self):
        self.tree = ET.parse('ports.xml')
        self.root = self.tree.getroot()

        if self.root[1][2].text == 'i':
            self.etq_2.setText('Entrada')
            self.boto_2.setEnabled(False)
        elif self.root[1][2].text == 'o':
            self.etq_2.setText('Sortida')
            self.boto_2.setEnabled(True)

    def DesaPin(self, estat, canal):
        self.desarSimple = DesarSimple(estat, canal)
        self.desarSimple.exec_()

    def Boto2(self):
        marxa = QPixmap('imatges/verd.png')
        paro = QPixmap('imatges/vermell.png')

    def  closeEvent(self,event):
        try:
            self.board.exit()
            event.accept()
        except Exception as e:
            self.board.exit()
            event.accept()

class DesarSimple(QDialog):
    def __init__(self, estat, canal):
        QDialog.__init__(self)
        uic.loadUi("pantalles/appDesarSimple.ui", self)
        if estat == 'i': self.r_IN.setChecked(True)
        elif estat == 'o': self.r_OUT.setChecked(True)
        self.desa.clicked.connect(partial(self.Desa, identificador = canal))

    def Desa(self,identificador):
        tree = ET.parse('ports.xml')
        root = tree.getroot()
        valor = ''
        resposta = QMessageBox.information(self, "Avis", "Aixo REINICIARÀ la placa !!", QMessageBox.Ok | QMessageBox.Cancel)
        if resposta == QMessageBox.Ok:
            if self.r_IN.isChecked(): valor = 'i'
            elif self.r_OUT.isChecked(): valor = 'o'
            for elem in root.iter(identificador): elem.text = valor
            tree.write('ports.xml', encoding='utf8')
            finestra.appNano.board.exit()
            finestra.appNano.botoConectar.setText("Conecta la Placa")
            finestra.appNano.etqOnOff.setPixmap(QPixmap('imatges/vermell.png'))
            finestra.appNano.Inicials()
            self.close()

        if resposta == QMessageBox.Cancel:
            self.close()

app = QApplication(sys.argv)
finestra = Finestra()
finestra.show()
app.exec_()