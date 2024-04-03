# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////
import csv

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import datetime  # 时间
import xlsxwriter  # 写xlsx
import xlrd  # 读xlsx
import re  # 正则表达式
import sqlite3  # python内置数据库


class CustomGrip(QWidget):
    def __init__(self, parent, position, disable_color=False):

        # SETUP UI
        QWidget.__init__(self)
        self.parent = parent
        self.setParent(parent)
        self.wi = Widgets()

        # SHOW TOP GRIP
        if position == Qt.TopEdge:
            self.wi.top(self)
            self.setGeometry(0, 0, self.parent.width(), 10)
            self.setMaximumHeight(10)

            # GRIPS
            top_left = QSizeGrip(self.wi.top_left)
            top_right = QSizeGrip(self.wi.top_right)

            # RESIZE TOP
            def resize_top(event):
                delta = event.pos()
                height = max(self.parent.minimumHeight(), self.parent.height() - delta.y())
                geo = self.parent.geometry()
                geo.setTop(geo.bottom() - height)
                self.parent.setGeometry(geo)
                event.accept()

            self.wi.top.mouseMoveEvent = resize_top

            # ENABLE COLOR
            if disable_color:
                self.wi.top_left.setStyleSheet("background: transparent")
                self.wi.top_right.setStyleSheet("background: transparent")
                self.wi.top.setStyleSheet("background: transparent")

        # SHOW BOTTOM GRIP
        elif position == Qt.BottomEdge:
            self.wi.bottom(self)
            self.setGeometry(0, self.parent.height() - 10, self.parent.width(), 10)
            self.setMaximumHeight(10)

            # GRIPS
            self.bottom_left = QSizeGrip(self.wi.bottom_left)
            self.bottom_right = QSizeGrip(self.wi.bottom_right)

            # RESIZE BOTTOM
            def resize_bottom(event):
                delta = event.pos()
                height = max(self.parent.minimumHeight(), self.parent.height() + delta.y())
                self.parent.resize(self.parent.width(), height)
                event.accept()

            self.wi.bottom.mouseMoveEvent = resize_bottom

            # ENABLE COLOR
            if disable_color:
                self.wi.bottom_left.setStyleSheet("background: transparent")
                self.wi.bottom_right.setStyleSheet("background: transparent")
                self.wi.bottom.setStyleSheet("background: transparent")

        # SHOW LEFT GRIP
        elif position == Qt.LeftEdge:
            self.wi.left(self)
            self.setGeometry(0, 10, 10, self.parent.height())
            self.setMaximumWidth(10)

            # RESIZE LEFT
            def resize_left(event):
                delta = event.pos()
                width = max(self.parent.minimumWidth(), self.parent.width() - delta.x())
                geo = self.parent.geometry()
                geo.setLeft(geo.right() - width)
                self.parent.setGeometry(geo)
                event.accept()

            self.wi.leftgrip.mouseMoveEvent = resize_left

            # ENABLE COLOR
            if disable_color:
                self.wi.leftgrip.setStyleSheet("background: transparent")

        # RESIZE RIGHT
        elif position == Qt.RightEdge:
            self.wi.right(self)
            self.setGeometry(self.parent.width() - 10, 10, 10, self.parent.height())
            self.setMaximumWidth(10)

            def resize_right(event):
                delta = event.pos()
                width = max(self.parent.minimumWidth(), self.parent.width() + delta.x())
                self.parent.resize(width, self.parent.height())
                event.accept()

            self.wi.rightgrip.mouseMoveEvent = resize_right

            # ENABLE COLOR
            if disable_color:
                self.wi.rightgrip.setStyleSheet("background: transparent")

    def mouseReleaseEvent(self, event):
        self.mousePos = None

    def resizeEvent(self, event):
        if hasattr(self.wi, 'container_top'):
            self.wi.container_top.setGeometry(0, 0, self.width(), 10)

        elif hasattr(self.wi, 'container_bottom'):
            self.wi.container_bottom.setGeometry(0, 0, self.width(), 10)

        elif hasattr(self.wi, 'leftgrip'):
            self.wi.leftgrip.setGeometry(0, 0, 10, self.height() - 20)

        elif hasattr(self.wi, 'rightgrip'):
            self.wi.rightgrip.setGeometry(0, 0, 10, self.height() - 20)


class Widgets(object):
    def top(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        self.container_top = QFrame(Form)
        self.container_top.setObjectName(u"container_top")
        self.container_top.setGeometry(QRect(0, 0, 500, 10))
        self.container_top.setMinimumSize(QSize(0, 10))
        self.container_top.setMaximumSize(QSize(16777215, 10))
        self.container_top.setFrameShape(QFrame.NoFrame)
        self.container_top.setFrameShadow(QFrame.Raised)
        self.top_layout = QHBoxLayout(self.container_top)
        self.top_layout.setSpacing(0)
        self.top_layout.setObjectName(u"top_layout")
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_left = QFrame(self.container_top)
        self.top_left.setObjectName(u"top_left")
        self.top_left.setMinimumSize(QSize(10, 10))
        self.top_left.setMaximumSize(QSize(10, 10))
        self.top_left.setCursor(QCursor(Qt.SizeFDiagCursor))
        self.top_left.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.top_left.setFrameShape(QFrame.NoFrame)
        self.top_left.setFrameShadow(QFrame.Raised)
        self.top_layout.addWidget(self.top_left)
        self.top = QFrame(self.container_top)
        self.top.setObjectName(u"top")
        self.top.setCursor(QCursor(Qt.SizeVerCursor))
        self.top.setStyleSheet(u"background-color: rgb(85, 255, 255);")
        self.top.setFrameShape(QFrame.NoFrame)
        self.top.setFrameShadow(QFrame.Raised)
        self.top_layout.addWidget(self.top)
        self.top_right = QFrame(self.container_top)
        self.top_right.setObjectName(u"top_right")
        self.top_right.setMinimumSize(QSize(10, 10))
        self.top_right.setMaximumSize(QSize(10, 10))
        self.top_right.setCursor(QCursor(Qt.SizeBDiagCursor))
        self.top_right.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.top_right.setFrameShape(QFrame.NoFrame)
        self.top_right.setFrameShadow(QFrame.Raised)
        self.top_layout.addWidget(self.top_right)

    def bottom(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        self.container_bottom = QFrame(Form)
        self.container_bottom.setObjectName(u"container_bottom")
        self.container_bottom.setGeometry(QRect(0, 0, 500, 10))
        self.container_bottom.setMinimumSize(QSize(0, 10))
        self.container_bottom.setMaximumSize(QSize(16777215, 10))
        self.container_bottom.setFrameShape(QFrame.NoFrame)
        self.container_bottom.setFrameShadow(QFrame.Raised)
        self.bottom_layout = QHBoxLayout(self.container_bottom)
        self.bottom_layout.setSpacing(0)
        self.bottom_layout.setObjectName(u"bottom_layout")
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_left = QFrame(self.container_bottom)
        self.bottom_left.setObjectName(u"bottom_left")
        self.bottom_left.setMinimumSize(QSize(10, 10))
        self.bottom_left.setMaximumSize(QSize(10, 10))
        self.bottom_left.setCursor(QCursor(Qt.SizeBDiagCursor))
        self.bottom_left.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.bottom_left.setFrameShape(QFrame.NoFrame)
        self.bottom_left.setFrameShadow(QFrame.Raised)
        self.bottom_layout.addWidget(self.bottom_left)
        self.bottom = QFrame(self.container_bottom)
        self.bottom.setObjectName(u"bottom")
        self.bottom.setCursor(QCursor(Qt.SizeVerCursor))
        self.bottom.setStyleSheet(u"background-color: rgb(85, 170, 0);")
        self.bottom.setFrameShape(QFrame.NoFrame)
        self.bottom.setFrameShadow(QFrame.Raised)
        self.bottom_layout.addWidget(self.bottom)
        self.bottom_right = QFrame(self.container_bottom)
        self.bottom_right.setObjectName(u"bottom_right")
        self.bottom_right.setMinimumSize(QSize(10, 10))
        self.bottom_right.setMaximumSize(QSize(10, 10))
        self.bottom_right.setCursor(QCursor(Qt.SizeFDiagCursor))
        self.bottom_right.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.bottom_right.setFrameShape(QFrame.NoFrame)
        self.bottom_right.setFrameShadow(QFrame.Raised)
        self.bottom_layout.addWidget(self.bottom_right)

    def left(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        self.leftgrip = QFrame(Form)
        self.leftgrip.setObjectName(u"left")
        self.leftgrip.setGeometry(QRect(0, 10, 10, 480))
        self.leftgrip.setMinimumSize(QSize(10, 0))
        self.leftgrip.setCursor(QCursor(Qt.SizeHorCursor))
        self.leftgrip.setStyleSheet(u"background-color: rgb(255, 121, 198);")
        self.leftgrip.setFrameShape(QFrame.NoFrame)
        self.leftgrip.setFrameShadow(QFrame.Raised)

    def right(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(500, 500)
        self.rightgrip = QFrame(Form)
        self.rightgrip.setObjectName(u"right")
        self.rightgrip.setGeometry(QRect(0, 0, 10, 500))
        self.rightgrip.setMinimumSize(QSize(10, 0))
        self.rightgrip.setCursor(QCursor(Qt.SizeHorCursor))
        self.rightgrip.setStyleSheet(u"background-color: rgb(255, 0, 127);")
        self.rightgrip.setFrameShape(QFrame.NoFrame)
        self.rightgrip.setFrameShadow(QFrame.Raised)


# 自定义QPlainTextEdit类，包含了自定义的右键菜单
class CustomPlainTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super(CustomPlainTextEdit, self).__init__(parent)

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        selectAllAction = menu.addAction("全选")
        copyAction = menu.addAction("复制")
        clearAction = menu.addAction("清空")
        findAction = menu.addAction("查找")

        selectAllAction.triggered.connect(self.selectAll)
        copyAction.triggered.connect(self.copy)
        clearAction.triggered.connect(self.clear)
        # findAction 需要你自己定义查找的逻辑，这里只是一个占位符
        findAction.triggered.connect(self.findText)

        # 调用exec_()显示菜单
        menu.exec_(event.globalPos())

    def findText(self):
        dialog = FindDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            searchText = dialog.getText()
            if not searchText:
                QMessageBox.information(self, "查找", "查找内容不能为空！")
                return

            self.moveCursor(QTextCursor.Start)
            found = self.find(searchText)  # 默认不带查找标志

            if not found:
                QMessageBox.information(self, "查找", "没有找到匹配的文本。")

    def highlightText(self, cursor):
        color = QColor("yellow")
        fmt = QTextCharFormat()
        fmt.setBackground(color)
        cursor.mergeCharFormat(fmt)


# 自定义QDialog类，用于提示QPlainTextEdit的查找结果
class FindDialog(QDialog):
    def __init__(self, parent=None):
        super(FindDialog, self).__init__(parent)
        self.setWindowTitle("查找")
        self.layout = QVBoxLayout(self)

        self.label = QLabel("输入查找内容:", self)
        self.lineEdit = QLineEdit(self)
        self.findButton = QPushButton("查找", self)
        self.findButton.clicked.connect(self.accept)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.findButton)

    def getText(self):
        return self.lineEdit.text()


# 自定义的QLineEdit类，包含了自定义的右键菜单，以及xlsx文件拖入功能
class DraggableLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(DraggableLineEdit, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e: QDragEnterEvent):
        if e.mimeData().hasUrls():
            # 检查所有拖入的文件是否为.xlsx文件
            all_xlsx = all(url.toLocalFile().endswith('.xlsx') for url in e.mimeData().urls())
            if all_xlsx:
                e.accept()
            else:
                e.ignore()
        else:
            e.ignore()

    def dropEvent(self, e: QDropEvent):
        urls = e.mimeData().urls()
        if urls:
            # 收集所有.xlsx文件的路径
            xlsx_paths = [url.toLocalFile() for url in urls if url.toLocalFile().endswith('.xlsx')]
            # 将这些路径连接成一个字符串，并设置到QLineEdit中
            # 这里使用"; "作为文件路径之间的分隔符
            self.setText("; ".join(xlsx_paths))

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        # 添加自定义操作
        clearAction = menu.addAction("清空")
        clearAction.triggered.connect(self.clear)

        # 显示菜单
        menu.exec_(event.globalPos())


class CustomMessageBox:
    def __init__(self, window_title, text, icon, YN):
        self.box = QMessageBox()
        self.setText(window_title, text)
        self.setStyle(icon, YN)
        # self.show()

    def setText(self, window_title, text):
        self.box.setWindowTitle(window_title)
        self.box.setText(text)

    def setStyle(self, icon, YN):
        '''
        :param icon: 图标 0:QMessageBox.Information,1:QMessageBox.Question,2:QMessageBox.Warning
        :param YN: 有几个按钮 0:无参数，即只有一个OK按钮,1:一个yes一个no，QMessageBox.Yes | QMessageBox.No
        :return:
        '''
        self.box.setStyleSheet("""
            QMessageBox {
                background-color: #282c34;
                color: rgb(255, 255, 255);
                border-radius: 5px;
                selection-color: rgb(255, 255, 255);
                selection-background-color: rgb(255, 121, 198);
                font-family: Smiley Sans;
                font-size: 18px;
            }
            QLabel {
                background-color: rgb(27, 29, 35);
                color: rgb(255, 255, 255);
                border-radius: 5px;
                selection-color: rgb(255, 255, 255);
                selection-background-color: rgb(255, 121, 198);
            }
            QPushButton {
                background-color: rgb(52, 59, 72);
                color: #ffffff;  /* 设置按钮文本颜色为白色 */
                padding: 5px;  /* 设置按钮内边距 */
                border-radius: 5px;
                font-family: Smiley Sans;
                font-size: 18px;
                width: 100px;
                border: 2px solid rgb(52, 59, 72);
            }
            QPushButton:hover {
                border: 2px solid rgb(64, 71, 88);
            }
            """)
        if YN == 0:
            if icon == 0:
                self.box.setIcon(QMessageBox.Information)
            elif icon == 1:
                self.box.setIcon(QMessageBox.Question)
            elif icon == 2:
                self.box.setIcon(QMessageBox.Warning)
            else:
                print("无Icon!!!")
        elif YN == 1:
            if icon == 0:
                self.box.setIcon(QMessageBox.Information)
            elif icon == 1:
                self.box.setIcon(QMessageBox.Question)
            elif icon == 2:
                self.box.setIcon(QMessageBox.Warning)
            else:
                print("无Icon!!!")
            self.box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        else:
            print("设置按钮个数错误!!!")

    def show(self):
        # 显示消息框并返回用户的选择
        return self.box.exec_()


class RecordDialog(QDialog):
    def __init__(self, record_id, row_data, function, parent=None):
        super(RecordDialog, self).__init__(parent)
        self.record_id = record_id
        self.row_data = row_data
        self.new_data = row_data
        self.initUI()
        if function == 'edit':
            self.loadData()

    def initUI(self):
        self.setWindowTitle("修改记录")
        # self.resize(400, 300)  # 宽度400px，高度300px

        # 使用Form布局来自动管理标签和输入框
        form_layout = QFormLayout()

        # 创建文本输入框，并用标签标识它们
        self.idLineEdit = QLineEdit(self)
        self.idLineEdit.setReadOnly(True)  # 设置序号为只读
        self.idLineEdit.setText(self.record_id)
        self.nameLineEdit = QLineEdit(self)
        self.specLineEdit = QLineEdit(self)
        self.unitLineEdit = QLineEdit(self)
        self.priceLineEdit = QLineEdit(self)
        self.manufacturerLineEdit = QLineEdit(self)

        # 添加文本输入框到表单布局
        form_layout.addRow("序号:", self.idLineEdit)
        form_layout.addRow("药品名称:", self.nameLineEdit)
        form_layout.addRow("规格:", self.specLineEdit)
        form_layout.addRow("单位:", self.unitLineEdit)
        form_layout.addRow("单价:", self.priceLineEdit)
        form_layout.addRow("生产厂家:", self.manufacturerLineEdit)

        # 创建按钮并连接信号
        self.saveButton = QPushButton("保存", self)
        self.saveButton.clicked.connect(self.saveRecord)
        self.cancelButton = QPushButton("取消", self)
        self.cancelButton.clicked.connect(self.reject)

        # 水平布局放置按钮
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.saveButton)
        buttons_layout.addWidget(self.cancelButton)

        # 垂直布局来放置表单和按钮布局
        layout = QVBoxLayout(self)
        layout.addLayout(form_layout)
        layout.addLayout(buttons_layout)

        self.setStyleSheet("""
                    QLineEdit {
                        background-color: rgb(27, 29, 35);
                        color: rgb(255, 255, 255);
                        border-radius: 5px;
                        selection-color: rgb(255, 255, 255);
                        selection-background-color: rgb(255, 121, 198);
                        font-family: Smiley Sans;
                        font-size: 18px;
                        height: 30px;
                    }
                    QDialog {
                        background-color: #282c34;
                        color: rgb(255, 255, 255);
                        border-radius: 5px;
                        selection-color: rgb(255, 255, 255);
                        selection-background-color: rgb(255, 121, 198);
                        font-family: Smiley Sans;
                        font-size: 18px;
                    }
                    QLabel {
                        color: rgb(255, 255, 255);
                        border-radius: 5px;
                        selection-color: rgb(255, 255, 255);
                        selection-background-color: rgb(255, 121, 198);
                        font-family: Smiley Sans;
                        font-size: 18px;
                    }
                    QPushButton {
                        background-color: rgb(52, 59, 72);
                        color: #ffffff;  /* 设置按钮文本颜色为白色 */
                        padding: 5px;  /* 设置按钮内边距 */
                        border-radius: 5px;
                        font-family: Smiley Sans;
                        font-size: 18px;
                        width: 100px;
                        border: 2px solid rgb(52, 59, 72);
                    }
                    QPushButton:hover {
                        border: 2px solid rgb(64, 71, 88);
                    }
                    """)
        self.setLayout(layout)

    def loadData(self):
        data = self.row_data
        self.nameLineEdit.setText(data['药品名称'])
        self.specLineEdit.setText(data['规格'])
        self.unitLineEdit.setText(data['单位'])
        self.priceLineEdit.setText(str(data['单价']))
        self.manufacturerLineEdit.setText(data['生产厂家'])

    def saveRecord(self):
        try:
            # 收集数据
            self.new_data = {
                '序号': int(self.record_id),
                '药品名称': self.nameLineEdit.text(),
                '规格': self.specLineEdit.text(),
                '单位': self.unitLineEdit.text(),
                '单价': float(self.priceLineEdit.text()),
                '生产厂家': self.manufacturerLineEdit.text(),
            }
            self.accept()
        except Exception as e:
            CustomMessageBox("警告", f"数据类型错误！：{e}", 2, 0).show()

    def getNewData(self):
        return self.new_data


class CustomTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super(CustomTableWidget, self).__init__(parent)
        self.now_table = ''
        self.now_select_text = ''
        self.data = []
        self.drug_db = None
        # ...其他初始化代码...

    def setDrugDB(self, drug_db):
        self.drug_db = drug_db

    def setNowTable(self, now_table):
        self.now_table = now_table

    def setNowSelectText(self, now_select_text):
        self.now_select_text = now_select_text

    def setData(self):
        if self.drug_db is not None and self.now_table != '':
            self.data = self.drug_db.search_table(self.now_table, self.now_select_text)
        else:
            CustomMessageBox("警告", "未对tableWidget_drug设置数据库属性！", 2, 0).show()

    def contextMenuEvent(self, event):
        self.menu = QMenu(self)

        copyAction = self.menu.addAction("复制")
        modifyAction = self.menu.addAction("修改")
        deleteAction = self.menu.addAction("删除")
        clearAction = self.menu.addAction("清空")

        action = self.menu.exec_(self.mapToGlobal(event.pos()))

        if action == clearAction:
            self.clearContents()  # 清空表格内容
        elif action == modifyAction:
            self.modify_record()  # 修改记录
        elif action == deleteAction:
            self.delete_record()  # 删除记录
        elif action == copyAction:
            self.copy_selection()  # 复制选中的行

    # 修改记录
    def modify_record(self):
        selected_items = self.selectedItems()
        if not selected_items:
            CustomMessageBox("警告", "请先选择要修改的记录", 2, 0).show()
            return
        # 假设第一列是ID或某个可以唯一标识记录的字段
        record_id = int(selected_items[0].text())
        try:
            cursor = self.drug_db.conn.cursor()
            cursor.execute(f"SELECT * FROM '{self.now_table}' WHERE 序号 = ?", (record_id,))
            row_data = cursor.fetchone()  # 假设只有一条记录与record_id匹配
            # 弹出修改窗口并传入选中的记录ID
            dialog = RecordDialog(record_id, row_data, 'edit', self)
            if dialog.exec_() == QDialog.Accepted:
                # 如果修改成功，重新加载或更新表格数据
                new_data = dialog.getNewData()
                cursor = self.drug_db.conn.cursor()
                # 构建参数化的SQL UPDATE语句
                sql = f"""UPDATE '{self.now_table}'
                              SET 药品名称 = :药品名称,
                                  规格 = :规格,
                                  单位 = :单位,
                                  单价 = :单价,
                                  生产厂家 = :生产厂家
                              WHERE 序号 = :序号"""
                # 执行SQL语句
                cursor.execute(sql, new_data)
                self.drug_db.conn.commit()  # 提交更改
                self.load_data()
        except Exception as e:
            CustomMessageBox("修改失败", f"无法修改记录：{e}", 2, 0).show()

    # 删除记录
    def delete_record(self):
        selected_items = self.selectedItems()
        if not selected_items:
            CustomMessageBox("警告", "请先选择要删除的记录", 2, 0).show()
            return
        # 同样假设第一列是可以唯一标识记录的ID
        record_id = int(selected_items[0].text())
        reply = CustomMessageBox("确认删除", "你确定要删除这条记录吗？", 1, 1).show()
        if reply == QMessageBox.Yes:
            # 执行删除操作
            try:
                cursor = self.drug_db.conn.cursor()
                cursor.execute(f"DELETE FROM '{self.now_table}' WHERE 序号 = ?", (record_id,))
                self.drug_db.conn.commit()
                # 删除后重新加载或更新表格数据
                self.load_data()
            except Exception as e:
                CustomMessageBox("删除失败", f"无法删除记录：{e}", 2, 0).show()

    # 复制记录
    def copy_selection(self):
        # 获取选中的单元格
        selection = self.selectedIndexes()
        if selection:
            # 字符串列表用于保存每个选中单元格的文本
            selected_data = []
            # 行号列表用于检查行的变化
            rows = []
            for index in selection:
                row = index.row()
                # 如果行号列表中没有当前行号，添加一个换行符
                if len(rows) == 0 or row != rows[-1]:
                    rows.append(row)
                    if selected_data:
                        selected_data.append('\n')  # 不是第一行，添加换行符
                # 添加单元格的文本
                selected_data.append(index.data())
                selected_data.append('\t')  # 添加制表符作为列分隔符
            # 复制到剪贴板
            clipboard = QApplication.clipboard()
            clipboard.setText(''.join(selected_data))

    def load_data(self):
        self.setData()
        # 清除现有数据
        self.clearContents()
        self.setRowCount(0)
        if not self.data:
            # 如果没有数据，则已经清空了 QTableWidget，此处不需要额外操作
            return

        # 设置 QTableWidget 的行和列
        self.setRowCount(len(self.data))
        self.setColumnCount(len(self.data[0]))

        # 设置列标题
        headers = self.data[0].keys()
        self.setHorizontalHeaderLabels(headers)

        # 遍历数据，填充 QTableWidget
        for row_index, row_data in enumerate(self.data):
            for column_index, column_name in enumerate(headers):
                item_value = row_data.get(column_name, "")  # 获取字典中的数据
                self.setItem(row_index, column_index, QTableWidgetItem(str(item_value)))

        current_row_count = self.rowCount()
        desired_row_count = 12  # 你想要的最少行数
        for row in range(current_row_count, desired_row_count):
            self.insertRow(row)
            for column in range(self.columnCount()):
                self.setItem(row, column, QTableWidgetItem(""))


# 数据库
class SQLiteDB:
    def __init__(self, db_path):
        self.db_path = db_path
        # 连接db文件
        self.conn = sqlite3.connect(self.db_path)
        # self.tablesName = self.getTables()
        self.conn.row_factory = sqlite3.Row  # 使得查询结果可以通过列名访问

    def closeConneect(self):
        self.conn.close()

    def getTablesName(self):
        cur = self.conn.cursor()
        # 查询sqlite_master表获取所有表名
        tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = tables.fetchall()
        # 提取表名
        table_names = [table[0] for table in tables]
        # 关闭游标
        cur.close()
        return table_names

    def search_table(self, table_name, text):
        cursor = self.conn.cursor()
        text_tuple = ()  # 定义一个空的元组，以便在不需要模糊查询时使用

        # 如果文本为空，返回整个表
        if text == '':
            query = f"SELECT * FROM '{table_name}'"
        else:
            # 首先获取表的列信息
            query = f"PRAGMA table_info('{table_name}')"
            cursor.execute(query)
            columns = [row[1] for row in cursor.fetchall()]  # 获取列名

            # 使用参数化查询以避免SQL注入
            like_clauses = ' OR '.join([f"{col} LIKE ?" for col in columns])
            query = f"SELECT * FROM '{table_name}' WHERE {like_clauses}"
            text = f"%{text}%"
            text_tuple = (text,) * len(columns)  # 创建一个包含多个文本的元组，用于模糊查询

        try:
            if text_tuple:
                cursor.execute(query, text_tuple)
            else:
                cursor.execute(query)
            rows = cursor.fetchall()
            # 假定行数据可以直接转换为字典
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"发生错误: {e}")
            return []
        finally:
            cursor.close()


class ClassificationXlsx:
    def __init__(self, files_path_list):
        # 获取被分类文件所在文件夹地址
        xlsx_path = files_path_list[0][0:-len(files_path_list[0].split('/')[-1])]
        # 定义分类表文件的保存地址
        self.save_file_path = xlsx_path + '药品分类.xlsx'
        # 创建工作表
        self.sava_file_xlsx = xlsxwriter.Workbook(self.save_file_path)
        # 标题格式
        self.title_format = self.sava_file_xlsx.add_format({'font_size': 16,  # 字体大小
                                                            'bold': True,  # 是否粗体
                                                            'align': 'center',  # 水平居中对齐
                                                            'valign': 'vcenter'  # 垂直居中对齐
                                                            })
        # 表头格式
        self.herder_format = self.sava_file_xlsx.add_format({'bold': True,  # 是否粗体
                                                             'align': 'left',  # 水平左对齐
                                                             'valign': 'vcenter',  # 垂直居中对齐
                                                             'border': 1  # 边框，0:无边框；1:外边框；
                                                             })
        # 左对齐格式
        self.left_format = self.sava_file_xlsx.add_format({'align': 'left',  # 水平左对齐
                                                           'valign': 'vcenter'  # 垂直居中对齐
                                                           })
        # 右对齐格式
        self.right_format = self.sava_file_xlsx.add_format({'align': 'right',  # 水平右对齐
                                                            'valign': 'vcenter'  # 垂直居中对齐
                                                            })
        # 边框格式
        self.frame_format = self.sava_file_xlsx.add_format({'border': 1  # 边框，0:无边框；1:外边框；
                                                            })
        # 定义表头
        self.xlsx_header = ['药品名称', '药品规格', '单位', '发药数', '发药金额']
        # 定义每个工作表的有效行域
        self.save_file_effective_area = {}
        # 定义输出的结果
        self.result = []

    def save(self):
        try:
            # 尝试关闭并保存文件
            self.sava_file_xlsx.close()

            # 文件保存成功，添加保存路径到结果中
            self.result.append('生成的文件地址：' + self.save_file_path)
        except Exception as e:
            # 其他所有类型的错误
            CustomMessageBox("保存错误", "发生未知错误。错误详情：" + str(e) + "\n文件已存在且可能已经被另一个程序打开，无法保存。请关闭文件后重试。", 2, 0).show()
            self.result.append('生成的文件无法保存！')
            self.result.append("文件已存在且可能已经被另一个程序打开，无法保存。请关闭文件后重试。")

    def createWorkSheet(self, table_names):
        unknow = "unrecognized"
        for table in table_names:
            try:
                self.setWorkSheet(table)
            except BaseException:
                self.result.append(f"数据库表 {table} 不在table.csv中！")
                time = datetime.datetime.now()
                title = "table.csv错误"
                text = "时间：" + str(time) + "\n" + f"数据库表 {table} 不在table.csv中"
                CustomMessageBox(title, text, 0, 0).show()
                continue
        # 设置“无法识别”表
        self.setWorkSheet(unknow)

    def setWorkSheet(self, table):
        # 为工作表添加sheet
        worksheet = self.sava_file_xlsx.add_worksheet(csvToDict()[table])
        # 设置工作表的有效行域
        self.save_file_effective_area[f"{table}_worksheet_row"] = 2
        # 合并单元格并写入表标题
        worksheet.merge_range('A1:E1', f'城关村{csvToDict()[table]}药房发药统计明细', self.title_format)
        # 写入表头
        xlsx_header_col = 0
        for item in self.xlsx_header:
            worksheet.write(1, xlsx_header_col, item, self.herder_format)
            xlsx_header_col += 1
        # 调整xlsx格式
        worksheet.set_row(0, 20.4)  # 第0行的行高
        worksheet.set_row(1, 20)  # 第1行的行高
        worksheet.set_column(0, 0, 27, self.left_format)  # 第0列到第0列的列宽，左对齐
        worksheet.set_column(1, 3, 12, self.left_format)  # 第1列到第3列的列宽，左对齐
        worksheet.set_column(4, 4, 12, self.right_format)  # 第4列到第4列的列宽，右对齐

    def createSum(self, table_names):
        unknow = "unrecognized"
        for table in table_names:
            try:
                self.setSum(table)
            except BaseException:
                continue
        # 设置“无法识别”表
        self.setSum(unknow)

    def setSum(self, table):
        # 定义Excel求和函数语句
        # 为防止求和函数出错，需要判别后赋予正确的求和
        if self.save_file_effective_area[table + '_worksheet_row'] != 2:
            sum_string = '=SUM(E3:E' + str(self.save_file_effective_area[table + '_worksheet_row']) + ')'
        else:
            sum_string = '0'
        # 将sheet的求和写入
        worksheet = self.sava_file_xlsx.get_worksheet_by_name(csvToDict()[table])
        worksheet.write(self.save_file_effective_area[table + '_worksheet_row'], 4, sum_string)


def csvToDict():
    # CSV文件路径
    csv_file_path = 'recourse/database/tables.csv'

    # 使用with语句打开文件，确保文件会被正确关闭
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        # 使用csv.reader读取文件
        reader = csv.reader(file)

        # 使用字典推导式将csv数据转换为字典
        csv_dict = {rows[0]: rows[1] for rows in reader}

    return csv_dict
