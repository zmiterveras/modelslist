from .viewer import Viewer
from PyQt5 import QtWidgets, QtCore


class LocAppHandler(Viewer):
    def __init__(self, database, handlersql, alias):
        Viewer.__init__(self)
        self.database = database
        self.handlersql = handlersql
        self.alias = alias
        self.newitem = []
        self.changeditem = []
        self.app_list = []
        self.loc_list = []
        self.getLocApp(self.handlersql, self.database)
        self.makeWidget()

    def makeWidget(self):
        Viewer.makeWidget(self)
        self.setLocAppListView(self.alias)

    def setLocAppListView(self, alias):
        if alias == "Application":
            query = "select id, name from Application"
            names = [(1, "Приложение")]
        else:
            query = "select id, name from Location"
            names = [(1, "Тип локации")]
        columns = [(1, 150)]
        Viewer.setListView(self, query, names, self.database, self.handlersql, columns)
        self.setEditButton()

    def setEditButton(self):
        for i, f in (('Add', self.addItem), ('Change', self.changeItem), ('Delete', self.deleteItem)):
            btn = QtWidgets.QPushButton(i)
            btn.clicked.connect(f)
            self.hbox.addWidget(btn)

    def addItem(self, a, new=('', ''), flag=None):
        def getName():
            value1 = lE_name.text()
            if value1 == '':
                QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не введено имя')
            else:
                if self.alias == "Application":
                    if value1 in [x[1] for x in self.app_list]:
                        QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Данное приложение уже существует')
                        return
                else:
                    if value1 in [x[1] for x in self.loc_list]:
                        QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Данная локация уже существует')
                        return
                if flag == 1:
                    txt = 'Изменена запись о ' + self.alias + ': '
                    self.changeditem = [new[0], value1]
                    print("Changed:\n", self.changeditem)
                    if self.alias == "Application":
                        self.app_list.pop(int(new[0]) - 1)
                        self.app_list.insert(int(new[0]) - 1, (int(new[0]), value1))
                    else:
                        self.loc_list.pop(int(new[0]) - 1)
                        self.loc_list.insert(int(new[0]) - 1, (int(new[0]), value1))
                    self.saveChangedItem()
                else:
                    txt = 'Добавлено ' + self.alias + ': '
                    if self.alias == "Application":
                        self.app_list.append((self.app_list[-1][0] + 1, value1))
                    else:
                        self.loc_list.append((self.loc_list[-1][0] + 1, value1))
                    self.newitem = [value1]
                    print("Newitem:\n", self.newitem)
                    self.saveItem()
                # print("Refreshed modelslist:\n", self.modelslist)
                # print("Refreshed modelnames:\n", self.modelnames)
                QtWidgets.QMessageBox.information(None, 'Инфо', txt + value1)
                self.clear()
                self.setLocAppListView(self.alias)
                tladd_model.close()

        tladd_model = QtWidgets.QWidget(parent=None, flags=QtCore.Qt.Window)
        tladd_model.setWindowTitle('Добавить')
        tladd_model.setWindowModality(QtCore.Qt.WindowModal)
        tladd_model.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        lE_name = QtWidgets.QLineEdit()
        btn_add = QtWidgets.QPushButton('Добавить')
        btn_close = QtWidgets.QPushButton('Закрыть')
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(btn_add)
        hbox.addWidget(btn_close)
        form = QtWidgets.QFormLayout()
        lE_name.setText(new[1])
        if flag == 1:
            tladd_model.setWindowTitle('Изменить')
        form.addRow('Имя:*', lE_name)
        form.addRow(hbox)
        btn_add.clicked.connect(getName)
        btn_close.clicked.connect(tladd_model.close)
        tladd_model.setLayout(form)
        tladd_model.show()

    def saveItem(self):
        if self.alias == "Application":
            self.handlersql.insertQuery(self.database, "Application", [":name"], self.newitem)
        else:
            self.handlersql.insertQuery(self.database, "Location", [":name"], self.newitem)

    def changeItem(self):
        if self.alias == "Application":
            nameslist = ['Приложение']
            item_list = self.app_list
        else:
            nameslist = ['Локация']
            item_list = self.loc_list
        result, row = Viewer.change(self, item_list, nameslist, 2)
        if result == 16384:
            self.addItem(None, row, 1)
        else:
            return
        pass

    def saveChangedItem(self):
        if self.alias == "Application":
            self.handlersql.updateQuery(self.database, "Application", ["name", "id"], self.changeditem[1:] +
                                        self.changeditem[:1])
        else:
            self.handlersql.updateQuery(self.database, "Location", ["name", "id"], self.changeditem[1:] +
                                        self.changeditem[:1])

    def deleteItem(self):
        if self.alias == "Application":
            nameslist = ['Приложение']
            item_list = self.app_list
        else:
            nameslist = ['Локация']
            item_list = self.loc_list
        result, row = Viewer.change(self, item_list, nameslist, 2, flag='delete')
        if result == 16384:
            self.handlersql.deleteQuery(self.database, self.alias, "id", row[0])
            self.clear()
            self.setLocAppListView(self.alias)
        else:
            return
