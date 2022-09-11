from .viewer import Viewer
from PyQt5 import QtWidgets, QtCore
import datetime


class MySessions(Viewer):
    def __init__(self, database, handlersql, models):
        Viewer.__init__(self)
        self.database = database
        self.sessionslist = []
        self.newsession = []
        self.changedsession = []
        self.handlersql = handlersql
        self.models = models
        self.makeWidget()

    def makeWidget(self):
        Viewer.makeWidget(self)
        if self.checkSessionsList():
            self.setSessionListView()
        else:
            label = QtWidgets.QLabel('Sessions List is empty')
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.vbox.addWidget(label)
            self.setSessionsEditButton()

    def checkSessionsList(self):
        sessions_count = False
        querystr = "select id, model_id from Sessions"
        conn, query = self.handlersql.connectBase(self.database)
        query.exec(querystr)
        # print(query.isSelect())
        if query.isActive():
            query.first()
            while query.isValid():
                self.sessionslist.append((query.value('id'), query.value('model_id')))
                query.next()
        if len(self.sessionslist):
            sessions_count = True
            print("Valid")
            print("Start sessionslist:\n", self.sessionslist)
        else:
            print("not valid")
        conn.close()
        return sessions_count

    def setSessionListView(self):
        query = """select s.id, m.name, s.location_desc, s.equipment, s.session_date
        from Sessions s inner join Models m on s.model_id = m.id"""
        names = [(1, 'Модель'), (2, 'Локация'), (3, 'Оборудование'), (4, 'Дата')]
        columns = [(1, 250), (2, 450), (3, 250), (4, 90)]
        Viewer.setListView(self, query, names, self.database, self.handlersql, columns)
        self.setSessionsEditButton()

    def setSessionsEditButton(self):
        for i, f in (('AddSession', self.addSession), ('ChangeSession', self.changeSession),
                     ('DeleteSession', self.deleteSession)):
            btn = QtWidgets.QPushButton(i)
            btn.clicked.connect(f)
            self.hbox.addWidget(btn)

    def addSession(self, a, new=('', '', '', '', ''), flag=None):  # разобраться с id в ...лист.апенд
        def getName():
            value1 = cb_modelsname.currentIndex()
            value2 = lE_location.text()
            value3 = le_equipment.text()
            value4 = calendar.text()
            if value2 == '':
                QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Нет локации')
            else:
                if flag == 1:
                    txt = 'Изменена сессия от: '
                    self.changedsession = [new[0], self.models[value1][0], value2, value3, value4]
                    print("Changed session:\n", self.changedsession)
                    self.sessionslist.pop(int(new[0]) - 1)
                    self.sessionslist.insert(int(new[0]) - 1, (int(new[0]), self.models[value1][0]))
                    self.saveChangedSession()
                else:
                    txt = 'Добавлено сессия от: '
                    if self.sessionslist:
                        self.sessionslist.append(
                            (self.sessionslist[-1][0] + 1, self.models[value1][0]))  # adedd(id, model_id)
                    else:
                        self.sessionslist.append((1, self.models[value1][0]))
                    self.newsession = [self.models[value1][0], value2, value3, value4]
                    print("Newsession:\n", self.newsession)
                    self.saveSession()
                QtWidgets.QMessageBox.information(None, 'Инфо', txt + value4)
                self.clear()
                self.setSessionListView()
                tladd_photo.close()

        if not [i[1] for i in self.models]:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Отсутствуют модели для связи с фото.\n' +
                                          'Добавте моделей!')
            return
        tladd_photo = QtWidgets.QWidget(parent=None, flags=QtCore.Qt.Window)
        tladd_photo.setWindowTitle('Добавить')
        # tladd_photo.setWindowModality(QtCore.Qt.WindowModal)
        # tladd_photo.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        cb_modelsname = QtWidgets.QComboBox()
        cb_modelsname.addItems([i[1] for i in self.models])
        lE_location = QtWidgets.QLineEdit()
        le_equipment = QtWidgets.QLineEdit()
        calendar = QtWidgets.QDateEdit()
        calendar.setCalendarPopup(True)
        calendar.setDisplayFormat("dd.MM.yyyy")
        calendar.setDate(datetime.date.today())
        btn_add = QtWidgets.QPushButton('Добавить')
        btn_close = QtWidgets.QPushButton('Закрыть')
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(btn_add)
        hbox.addWidget(btn_close)
        form = QtWidgets.QFormLayout()
        for i, n in (zip((lE_location, le_equipment), (new[2], new[3]))):
            i.setText(n)
        if flag == 1:
            tladd_photo.setWindowTitle('Изменить')
            cb_modelsname.setCurrentText(new[1])
            datelist = new[-1].split('.')
            calendar.setDate(QtCore.QDate(int(datelist[2]), int(datelist[1]), int(datelist[0])))
        form.addRow('Имя модели:', cb_modelsname)
        form.addRow('Описание локации:', lE_location)
        form.addRow('Оборудование:', le_equipment)
        form.addRow('Дата съёмки:', calendar)
        form.addRow(hbox)
        btn_add.clicked.connect(getName)
        btn_close.clicked.connect(tladd_photo.close)
        tladd_photo.setLayout(form)
        tladd_photo.show()

    def saveSession(self):
        self.handlersql.insertQuery(self.database, "Sessions", [":model_id", ":location_desc", ":equipment",
                                                                ":session_date"], self.newsession)

    def changeSession(self):
        nameslist = ['Имя модели', 'Описание локации', 'Оборудование', 'Дата съёмки']
        result, row = Viewer.change(self, self.sessionslist, nameslist, 5)
        if result == 16384:
            self.addSession(None, row, 1)
        else:
            return

    def saveChangedSession(self):
        self.handlersql.updateQuery(self.database, "Sessions",
                                    ["model_id", "location_desc", "equipment", "session_date",
                                     "id"], self.changedsession[1:] + self.changedsession[:1])

    def deleteSession(self):
        nameslist = ['Имя модели', 'Описание локации', 'Оборудование', 'Дата съёмки']
        result, row = Viewer.change(self, self.sessionslist, nameslist, 5, flag='delete')
        if result == 16384:
            self.handlersql.deleteQuery(self.database, "Sessions", "id", row[0])
            self.clear()
            self.setSessionListView()
        else:
            return
