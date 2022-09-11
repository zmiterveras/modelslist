#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtSql
import sqlite3


class HandleSql:

    def connectBase(self, basename):
        conn = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        conn.setDatabaseName(basename)
        conn.open()
        query = QtSql.QSqlQuery()
        return conn, query

    def insertQuery(self, basename, tablename, alies, args):
        strquery = "insert into %s values (null" % tablename
        conn, query = self.connectBase(basename)
        for a in alies:
            strquery += ", %s" % a
        strquery += ")"
        query.prepare(strquery)
        for a, arg in zip(alies, args):
            query.bindValue(a, arg)
        query.exec_()
        conn.close()

    def updateQuery(self, basename, tablename, alias, args):
        strquery = "update %s set" % tablename
        conn, query = self.connectBase(basename)
        for al in alias[:-1]:
            strquery += " %s=:%s," % (al, al)
        strquery = strquery[:-1]
        strquery += " where %s=:%s" % (alias[-1], alias[-1])
        query.prepare(strquery)
        for (al, arg) in zip(alias, args):
            query.bindValue(":" + al, arg)
        query.exec_()
        conn.close()

    def deleteQuery(self, basename, tablename, alias, arg):
        strquery = "delete from %s where %s=:%s" % (tablename, alias, alias)
        conn, query = self.connectBase(basename)
        query.prepare(strquery)
        query.bindValue(":" + alias, arg)
        query.exec_()
        conn.close()






