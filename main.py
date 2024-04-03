import sys
import os
import platform

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMainWindow, QHeaderView, QApplication
from PySide2.QtCore import Qt

from modules import *
from modules import Settings
from widgets import *

os.environ["QT_FONT_DPI"] = "96"  # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # 设置为全局组件
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # 使用自定义标题栏|为MAC或LINUX使用“False”
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "药品分类器"
        description = "药房发药统计——药品分类器"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # 切换菜单
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # 设置UI定义
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # 表格参数
        # ///////////////////////////////////////////////////////////////
        # widgets.tableWidget_drug.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 设置第一列的固定宽度
        widgets.tableWidget_drug.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        widgets.tableWidget_drug.setColumnWidth(0, 50)  # 设置第一列的宽度为50像素
        # 获取列总数
        columnCount = widgets.tableWidget_drug.columnCount()
        # 设置第一列以外的其他列的尺寸调整模式为 Stretch
        for columnIndex in range(1, columnCount):
            widgets.tableWidget_drug.horizontalHeader().setSectionResizeMode(columnIndex, QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        # widgets.btn_new.clicked.connect(self.buttonClick)
        # widgets.btn_save.clicked.connect(self.buttonClick)

        # some widgets
        widgets.pushButton_use_instruction.clicked.connect(self.buttonClick)
        widgets.pushButton_openfile.clicked.connect(self.buttonClick)
        widgets.pushButton_classification.clicked.connect(self.buttonClick)
        widgets.pushButton_select.clicked.connect(self.buttonClick)
        widgets.pushButton_add.clicked.connect(self.buttonClick)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)

        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)

        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # CLOSE APPLICATION
        # 关闭应用程序
        def closeWindow():
            self.drug_db.closeConneect()
            print("关闭数据库连接")
            self.close()

        # widgets.closeAppBtn.clicked.connect(lambda: self.close())
        widgets.closeAppBtn.clicked.connect(closeWindow)


        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # 设置主页和选择菜单
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

        # 设置数据库类
        self.drug_db = SQLiteDB('recourse/database/drug_classification.db')
        # self.drug_db = SQLiteDB(r"D:\PyCharm\PJ\DrugClassification_32bit\recourse\database\drug_classification.db")
        # 清除comboBox_sheet现有的所有选项
        widgets.comboBox_sheet.clear()
        # 添加新的选项
        widgets.comboBox_sheet.addItems(self.drug_db.getTablesName())
        # 为tableWidget_drug设置数据库连接
        widgets.tableWidget_drug.setDrugDB(self.drug_db)
        # 展示tableWidget_drug数据
        self.tableShow(widgets.comboBox_sheet.currentText(), widgets.lineEdit_select.text())

    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        if btnName == "pushButton_use_instruction":
            # widgets.plainTextEdit_2.clear()  # 清除文本
            widgets.plainTextEdit_2.appendPlainText("#########################\n"
                                                    "--使用说明：\n"
                                                    "第一步：点击“选择文件\n"
                                                    "第二步：选中需要分类的药房发药统计表\n"
                                                    "第三步：点击右下角“打开\n"
                                                    "第四步：点击“开始分类\n"
                                                    "或者：\n"
                                                    "第一步：将需要分类的药房发药统计表拖入文件地址栏\n"
                                                    "第二步：点击“开始分类”\n"
                                                    "系统提示分类是否成功。\n"
                                                    "#########################")  # 添加文本
        if btnName == "pushButton_openfile":
            file_paths, _ = QFileDialog.getOpenFileNames(self, "选取文件", "./", "Excel Files (*.xlsx)")
            # 如果需要将选中的所有文件路径显示在lineEdit中，可以将它们连接成一个字符串
            # 这里使用"; "作为文件路径之间的分隔符，你可以根据需要选择其他分隔符
            widgets.lineEdit_filepath.setText("; ".join(file_paths))
            # 如果只是需要处理这些文件，不需要显示路径，可以直接在这里处理file_paths列表

        if btnName == "pushButton_classification":
            # widgets.plainTextEdit_2.clear()  # 清除文本
            time = datetime.datetime.now()
            # 以”;“为分隔符将选择的多文件路径分割字符串为列表
            files_path_list = widgets.lineEdit_filepath.text().split('; ')
            if files_path_list[0] != '':
                # 转换结果
                conversion_results = self.classification(files_path_list)
                widgets.plainTextEdit_2.appendPlainText('*************************')
                widgets.plainTextEdit_2.appendPlainText('时间：' + str(time))
                for result in conversion_results:
                    widgets.plainTextEdit_2.appendPlainText(result)
                widgets.plainTextEdit_2.appendPlainText('*************************')

            else:
                # print('!!!!!!!!!!!!!!!!!!!!!!!!!\n'
                #       '时间：  ', time, '\n'
                #                      '未选取文件，请先选择正确的文件\n'
                #                      '!!!!!!!!!!!!!!!!!!!!!!!!!')
                title = "文件错误"
                text = "时间：" + str(time) + "\n" + "未选取文件，请先选择正确的文件"
                CustomMessageBox(title, text, 0, 0).show()

        if btnName == "pushButton_select":
            self.tableShow(widgets.comboBox_sheet.currentText(), widgets.lineEdit_select.text())

        if btnName == "pushButton_add":
            widgets.lineEdit_select.clear()
            self.tableShow(widgets.comboBox_sheet.currentText(), widgets.lineEdit_select.text())
            now_table = widgets.comboBox_sheet.currentText()
            if now_table not in self.drug_db.getTablesName():
                CustomMessageBox("警告", "选择的表不存在于数据库中！", 2, 0).show()
            else:
                # try:
                cursor = self.drug_db.conn.cursor()
                sql = f"SELECT MAX(序号) FROM '{now_table}';"
                cursor.execute(sql)
                max_id_row = cursor.fetchone()
                if max_id_row:
                    max_id = max_id_row[0]  # fetchone()返回的是一个元组，即使只有一个值
                else:
                    max_id = 0  # 如果表为空，可能没有最大序号
                new_id = max_id + 1
                # 弹出修改窗口并传入选中的记录ID
                dialog = RecordDialog(str(new_id), None, 'add', self)
                if dialog.exec_() == QDialog.Accepted:
                    # 如果用户确认添加，获取新数据
                    new_data = dialog.getNewData()
                    # 构建参数化的SQL INSERT语句
                    sql = f"""INSERT INTO {now_table} (序号, 药品名称, 规格, 单位, 单价, 生产厂家)
                                      VALUES (:序号, :药品名称, :规格, :单位, :单价, :生产厂家)"""
                    # 执行SQL语句
                    cursor.execute(sql, new_data)
                    self.drug_db.conn.commit()  # 提交更改
                    # 重新加载或更新表格数据
                    widgets.tableWidget_drug.load_data()
                # except Exception as e:
                #     CustomMessageBox("添加失败", f"无法添加记录：{e}", 2, 0).show()


    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

    def getDrugTable(self, drug_name, drug_manufactor):
        # 获取所有表名
        table_names = self.drug_db.getTablesName()

        cur = self.drug_db.conn.cursor()
        # 定义默认的药品类型
        right_table = 'unrecognized'
        # 定义查询出的匹配到的表名
        match_table = []

        # 构建动态SQL查询
        for table_name in table_names:
            query = f"SELECT * FROM `{table_name}` WHERE 药品名称=?"
            cur.execute(query, (drug_name,))
            if len(cur.fetchall()) != 0:
                match_table.append(table_name)

        # 药名只符合一种类型
        if len(match_table) == 1:
            right_table = match_table[0]
        # 药名符合多种类型
        if len(match_table) > 1:
            # 对比类型中的厂家前两个字
            for match in match_table:
                query = f"SELECT `生产厂家` FROM `{match}` WHERE 药品名称=?"
                manufactor_list = cur.execute(query, (drug_name,)).fetchall()
                if manufactor_list[0][0] != '' and manufactor_list[0][0] is not None:
                    if manufactor_list[0][0][0:2] == drug_manufactor[0:2]:
                        right_table = match
        # 关闭游标
        cur.close()
        return right_table

    def classification(self, files_path_list):
        unknow = "unrecognized"
        create_file = ClassificationXlsx(files_path_list)
        # 获取所有表名
        table_names = self.drug_db.getTablesName()
        # 创建sheet并设置格式
        create_file.createWorkSheet(table_names)
        # 读取传入的xlsx文件
        for file_path in files_path_list:
            # 读取传入的xlsx文件
            try:
                workbook = xlrd.open_workbook(filename=file_path)
            except BaseException:
                create_file.result.append(file_path + '文件错误，或者该文件非xlsx文件！')
                time = datetime.datetime.now()
                title = "文件错误"
                text = "时间：" + str(time) + "\n" + file_path + "\n文件错误，或者该文件非xlsx文件！"
                CustomMessageBox(title, text, 0, 0).show()
                continue
            # 获取第一个sheet表格
            table = workbook.sheets()[0]
            # 判别读取的xlsx格式是否正确
            if table.cell_value(
                    rowx=0, colx=0) != '药房发药统计明细' or table.cell_value(
                rowx=1, colx=0) != '药品名称' or table.cell_value(
                rowx=1, colx=1) != '药品规格' or table.cell_value(
                rowx=1, colx=2) != '单位' or table.cell_value(
                rowx=1, colx=3) != '发药数' or table.cell_value(
                rowx=1, colx=4) != '发药金额':
                create_file.result.append(file_path + '非药房发药统计明细！转换失败！')
                time = datetime.datetime.now()
                title = "表格格式错误"
                text = "时间：" + str(time) + "\n" + file_path + "\n非药房发药统计明细！转换失败！"
                CustomMessageBox(title, text, 0, 0).show()
                continue
            # 行列下标从0开始，定义，药名从第三行第一列开始，所以row=2、col=0
            row = 2
            col = 0
            # 获取药品名单元格内的值
            while row < table.nrows:  # table.nrows是表格的有效行数
                if table.cell_value(rowx=row, colx=col) != '':
                    drug_name = table.cell_value(rowx=row, colx=col)
                    # 药名规范化：去掉".",厂家只对比前两个字
                    drug_name = drug_name.replace('.', '')
                    # 去掉" "
                    drug_name = drug_name.replace(' ', '')
                    # 药名最后一个字是数字的去掉数字
                    while drug_name[-1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        drug_name = drug_name.replace(drug_name[-1], '')
                    # 正则表达式 去掉括号及括号中内容
                    drug_name = re.sub('\\(.*?\\)', '', drug_name)
                    drug_name = re.sub('（.*?）', '', drug_name)
                    drug_name = re.sub('\\(.*?）', '', drug_name)
                    drug_name = re.sub('（.*?\\)', '', drug_name)
                    # 药品厂家
                    drug_manufactor = table.cell_value(rowx=row, colx=6)
                    # 与数据库进行对比，判别药品类型
                    drug_type = self.getDrugTable(drug_name, drug_manufactor)
                    # 定义默认的sheet类型
                    sheet_type = create_file.sava_file_xlsx.get_worksheet_by_name(csvToDict()[unknow])
                    # 定义默认的sheet的行
                    row_name = unknow + '_worksheet_row'
                    # drug_type改变sheet_type和row_name
                    try:
                        sheet_type = create_file.sava_file_xlsx.get_worksheet_by_name(csvToDict()[drug_type])
                        row_name = drug_type + '_worksheet_row'
                    except BaseException:
                        text = f"文件名：{file_path}\n" \
                               f"药品名：{drug_name}\n" \
                               f"药品厂家：{drug_manufactor}\n" \
                               f"药品类型：{drug_type} 不在table.csv中！"
                        create_file.result.append(f"药品类型 {drug_type} 不在table.csv中！")
                        time = datetime.datetime.now()
                        title = "table.csv错误"
                        text = "时间：" + str(time) + "\n" + text
                        CustomMessageBox(title, text, 0, 0).show()

                    # 分类好后写入新的xlsx文件
                    for record_col in range(0, 5):
                        # 读取要分类的一行记录
                        row_value = table.cell_value(rowx=row, colx=record_col)
                        # “发药金额”列需要转为数字最后才能进行求和操作
                        if record_col == 4:
                            row_value = float(row_value)
                        # 把记录写入生成的文件
                        sheet_type.write(create_file.save_file_effective_area[row_name], record_col, row_value,
                                         create_file.frame_format)
                    # 生成文件的对应sheet的有效行+1
                    create_file.save_file_effective_area[row_name] += 1
                # 行+1，准备读取下一行记录
                row += 1
            # 加入转换成功提示
            create_file.result.append(file_path + '文件转换成功！')
        # 设置每个sheet的求和
        create_file.createSum(table_names)
        # 保存文件
        create_file.save()

        return create_file.result

    def tableShow(self, table, text):
        # 为tableWidget_drug设置Table和SelectText
        widgets.tableWidget_drug.setNowTable(table)
        widgets.tableWidget_drug.setNowSelectText(text)
        # 为tableWidget_drug填写初始表格
        widgets.tableWidget_drug.load_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
