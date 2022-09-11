from .viewer import Viewer
from PyQt5 import QtWidgets, QtCore


class MyModels(Viewer):
    def __init__(self, database, handlersql):
        Viewer.__init__(self)
        # self.root_path = root_path
        # self.database = os.path.join(self.root_path, 'bases/models.sqlite')
        self.database = database
        self.modelslist = []
        self.newmodel = []
        self.changedmodel = []
        self.handlersql = handlersql
        self.makeWidget()

    def makeWidget(self):
        Viewer.makeWidget(self)
        if self.checkModelsList():
            self.setModelListView()
        else:
            label = QtWidgets.QLabel('Models List is empty')
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.vbox.addWidget(label)
            self.setModelsEditButton()

    def checkModelsList(self):
        models_count = False
        querystr = "select id, name from Models"
        conn, query = self.handlersql.connectBase(self.database)  # connectBase(self.database)
        query.exec(querystr)
        # print(query.isSelect())
        if query.isActive():
            query.first()
            while query.isValid():
                self.modelslist.append((query.value('id'), query.value('name')))
                query.next()
        if len(self.modelslist):
            models_count = True
            print("Valid")
            print("Start modellist:\n", self.modelslist)
        else:
            print("not valid")
        conn.close()
        return models_count

    def setModelListView(self):
        query = """select m.id, m.name, m.origin, m.ed_work, c.phone, c.email, c.ref_s 
        from Models m inner join Contacts c on m.id = c.model_id"""
        names = [(1, 'Имя'), (2, 'Откуда'), (3, 'Образование/Работа'), (4, 'Phone'), (5, 'Email'), (6, 'References')]
        columns = [(1, 220), (2, 130), (3, 250), (4, 120), (5, 165), (6, 165)]
        Viewer.setListView(self, query, names, self.database, self.handlersql, columns)
        self.setModelsEditButton()

    def setModelsEditButton(self):
        for i, f in (('AddModel', self.addModel), ('ChangeModel', self.changeModel), ('DeleteModel', self.deleteModel)):
            btn = QtWidgets.QPushButton(i)
            btn.clicked.connect(f)
            self.hbox.addWidget(btn)

    def addModel(self, a, new=('', '', '', '', '', '', ''), flag=None):
        def getName():
            value1 = lE_name.text()
            value2 = lE_origin.text()
            value3 = lE_ed_work.text()
            value4 = lE_phone.text()
            value5 = lE_email.text()
            value6 = lE_references.text()
            if value1 == '':
                QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не введено имя')
            else:
                if value1 in list([i[1] for i in self.modelslist]) and not flag:
                    result = QtWidgets.QMessageBox.question(None, 'Предупреждение',
                                                            'Модель с похожим именем есть в списке.\n' +
                                                            'Хотите продолжить?',
                                                            buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                            defaultButton=QtWidgets.QMessageBox.No)
                    if result == 16384:
                        pass
                    else:
                        return
                if flag == 1:
                    txt = 'Изменена запись о модели: '
                    self.changedmodel = [new[0], value1, value2, value3, value4, value5, value6]
                    print("Changed model:\n", self.changedmodel)
                    self.modelslist.pop(int(new[0]) - 1)
                    self.modelslist.insert(int(new[0]) - 1, (int(new[0]), value1))
                    self.saveChangedModel()
                else:
                    txt = 'Добавлена модель: '
                    if self.modelslist:
                        self.modelslist.append((self.modelslist[-1][0] + 1, value1))  # adedd(id, name)
                    else:
                        self.modelslist.append((1, value1))
                    self.newmodel = [value1, value2, value3, value4, value5, value6]
                    print("Newmodel:\n", self.newmodel)
                    self.saveModel()
                print("Refreshed modelslist:\n", self.modelslist)
                QtWidgets.QMessageBox.information(None, 'Инфо', txt + value1)
                self.clear()
                self.setModelListView()
                tladd_model.close()

        tladd_model = QtWidgets.QWidget(parent=None, flags=QtCore.Qt.Window)
        tladd_model.setWindowTitle('Добавить')
        tladd_model.setWindowModality(QtCore.Qt.WindowModal)
        tladd_model.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        lE_name = QtWidgets.QLineEdit()
        lE_origin = QtWidgets.QLineEdit()
        lE_ed_work = QtWidgets.QLineEdit()
        lE_phone = QtWidgets.QLineEdit()
        lE_email = QtWidgets.QLineEdit()
        lE_references = QtWidgets.QLineEdit()
        btn_add = QtWidgets.QPushButton('Добавить')
        btn_close = QtWidgets.QPushButton('Закрыть')
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(btn_add)
        hbox.addWidget(btn_close)
        form = QtWidgets.QFormLayout()
        k = 1
        for i in (lE_name, lE_origin, lE_ed_work, lE_phone, lE_email, lE_references):
            i.setText(new[k])
            k += 1
        if flag == 1:
            tladd_model.setWindowTitle('Изменить')

        form.addRow('Имя модели:*', lE_name)
        form.addRow('Откуда:', lE_origin)
        form.addRow('Учеба/Работа:', lE_ed_work)
        form.addRow('Телефон:', lE_phone)
        form.addRow('Email:', lE_email)
        form.addRow('Ссылки:', lE_references)
        form.addRow(hbox)
        btn_add.clicked.connect(getName)
        btn_close.clicked.connect(tladd_model.close)
        tladd_model.setLayout(form)
        tladd_model.show()

    def changeModel(self):
        nameslist = ['Имя', 'Откуда', 'Учеба/Работа', 'Телефон', 'Email', 'Ссылки']
        result, row = Viewer.change(self, self.modelslist, nameslist, 7)
        if not row: return
        if result == 16384:
            self.addModel(None, row, 1)
        else:
            return

    def saveModel(self):
        self.handlersql.insertQuery(self.database, "Models", [":name", ":origin", ":ed_work"], self.newmodel[:3])
        args = self.newmodel[3:]
        args.insert(0, self.modelslist[-1][0])
        self.handlersql.insertQuery(self.database, "Contacts", [":model_id", ":phone", ":email", ":ref_s"], args)

    def saveChangedModel(self):
        self.handlersql.updateQuery(self.database, "Models", ["name", "origin", "ed_work", "id"],
                                    self.changedmodel[1:4] + self.changedmodel[:1])
        self.handlersql.updateQuery(self.database, "Contacts", ["phone", "email", "ref_s", "model_id"],
                                    self.changedmodel[4:] + self.changedmodel[:1])

    def deleteModel(self):
        nameslist = ['Имя', 'Откуда', 'Учеба/Работа', 'Телефон', 'Email', 'Ссылки']
        result, row = Viewer.change(self, self.modelslist, nameslist, 7, flag='delete')
        if result == 16384:
            self.handlersql.deleteQuery(self.database, "Contacts", "model_id", row[0])
            self.handlersql.deleteQuery(self.database, "Models", "id", row[0])
            self.modelslist.remove((row[0], row[1]))
            self.clear()
            self.setModelListView()
        else:
            return

    def test(self):
        print('test')
