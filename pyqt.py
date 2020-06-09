import sys, os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from untitled import Ui_MainWindow
import base64
class mywindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(mywindow,self).__init__()
        self.setupUi(self)

    # 遍历获取目录下的所有文件绝对路径
    def getFilePath(self, path):
        rList = []
        if os.path.isfile(path):  # 是个文件
            rList.append(path)
        else:  # 是文件夹
            for root, folder, file in os.walk(path):
                for i in file:
                    file_path = os.path.join(root, i)
                    rList.append(file_path)
        return rList

    # 确定按钮 点击事件
    def button_click(self):

        input_path = self.lineEdit.text()
        output_path = self.lineEdit_2.text()
        option = self.comboBox.currentText()
        if not (input_path and output_path):
            QMessageBox.warning(self, "警告", "输入或输出路径为空！",
                                        QMessageBox.Ok)
        else:
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            rList = self.getFilePath(input_path)
            if option == "图片转base64":
                for i in rList:
                    with open(i, 'rb') as f:
                        line = f.read()
                    pic_base64 = base64.b64encode(line).decode()
                    file_name = os.path.splitext(os.path.split(i)[-1])[0] + ".txt"
                    with open(os.path.join(output_path, file_name), "w", encoding="utf8") as a:
                        a.write(pic_base64)
            else:  # base64转图片
                for i in rList:
                    with open(i, encoding="utf8") as f:
                        line = f.read()
                    file_name = os.path.splitext(os.path.split(i)[-1])[0] + ".jpg"
                    with open(os.path.join(output_path, file_name), "wb") as a:
                        a.write(base64.b64decode(line))
            QMessageBox.information(self, "提示", "转换完成！",
                                QMessageBox.Ok)

    # 选择 输入文件 按钮点击事件
    def file_choose(self):
        file, ok = QFileDialog.getOpenFileName(self, 'Open file', './', 'All Files ( * )')
        if ok:
            self.lineEdit.setText(file)
    # 选择 输出文件夹 按钮点击事件
    def folder_choose(self):
        folder = QFileDialog.getExistingDirectory(self,'Open folder','./', )

        self.lineEdit_2.setText(folder)
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())

