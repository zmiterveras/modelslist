from PyQt5 import QtWidgets, QtCore, QtSql


class Viewer(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self, parent=None)

    def makeWidget(self):
        self.top_box = QtWidgets.QVBoxLayout()
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox = QtWidgets.QHBoxLayout()
        self.top_box.addLayout(self.vbox)
        self.top_box.addLayout(self.hbox)
        self.setLayout(self.top_box)

    def clear(self):
        for i in reversed(range(self.vbox.count())):
            wt = self.vbox.itemAt(i).widget()
            wt.setParent(None)
            wt.deleteLater()
        for i in reversed(range(self.hbox.count())):
            wb = self.hbox.itemAt(i).widget()
            wb.setParent(None)
            wb.deleteLater()

    def setSorting(self, buttons):
        self.sort_box = QtWidgets.QGroupBox('Сортировать по')
        self.sort_box.setAlignment(QtCore.Qt.AlignHCenter)
        self.buttons_box = QtWidgets.QHBoxLayout()
        self.buttons = []
        for i in buttons:
            rbtn = QtWidgets.QRadioButton(i)
            self.buttons_box.addWidget(rbtn)
            self.buttons.append(rbtn)
        self.buttons[0].setChecked(True)
        self.sort_box.setLayout(self.buttons_box)
        self.vbox.addWidget(self.sort_box)

    def setListView(self, query, names, database, handlersql, columns):
        # self.clear()
        print("QUERY:\n", query)
        handlersql.connectBase(database)
        self.stm = QtSql.QSqlQueryModel(parent=None)
        self.stm.setQuery(query)
        for (i, n) in names:
            self.stm.setHeaderData(i, QtCore.Qt.Horizontal, n)
        self.tv = QtWidgets.QTableView()
        self.tv.setModel(self.stm)
        self.tv.hideColumn(0)
        for i, n in columns:
            self.tv.setColumnWidth(i, n)
        self.vbox.addWidget(self.tv)

    def getRow(self, col):
        row_number = self.tv.currentIndex().row()
        row = []
        for i in range(col):
            index = self.stm.index(row_number, i)
            row.append(self.stm.data(index))
        print('Selected row: ', row)
        return row

    def change(self, datalist, nameslist, col, flag='change'):
        if not datalist:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Отсутствуют данные для изменения')
            return
        row = self.getRow(col)
        if None in row:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не выбраны данные для изменения')
            return 1, row
        if flag == 'change':
            text = 'Вы действительно хотите изменить запись:\n'
        else:
            text = 'Вы действительно хотите удалить запись:\n'
        for name, data in zip(nameslist, row[1:]):
            text += name + ": " + data + "\n"
        result = QtWidgets.QMessageBox.question(None, 'Предупреждение', text,
                                                buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                defaultButton=QtWidgets.QMessageBox.No)
        return result, row

    def getLocApp(self, handlersql, database):
        query_loc = "select * from Location"
        query_app = "select * from Application"
        conn, query = handlersql.connectBase(database)  # connectBase(self.database)
        query.exec(query_loc)
        if query.isActive():
            query.first()
            while query.isValid():
                self.loc_list.append((query.value('id'), query.value('name')))
                query.next()
        query.clear()
        query.exec(query_app)
        if query.isActive():
            query.first()
            while query.isValid():
                self.app_list.append((query.value('id'), query.value('name')))
                query.next()
        conn.close()
        print("App: ", self.app_list)
        print("Loc: ", self.loc_list)
