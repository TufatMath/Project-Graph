import sys
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import numpy as np
import math
import pyqtgraph.exporters


# Диалоговое окно для истории функций
class HistoryDialog(QDialog):
    def __init__(self, functionHistory):
        super().__init__()
        self.initUI(functionHistory)
        self.setWindowTitle("История функций")

    def initUI(self, functionHistory):
        # Макет для диалога "История"
        layout = QVBoxLayout(self)

        # Текстовый браузер для отображения истории
        self.functionBrowser = QTextBrowser()
        layout.addWidget(self.functionBrowser)

        # Добавление в историю
        for function in functionHistory:
            self.functionBrowser.append(function)

        # Расположение кнопок
        knopkiLayout = QHBoxLayout()
        layout.addLayout(knopkiLayout)

        # Кнопка "ОК"
        okknopka = QPushButton("ОК")
        okknopka.clicked.connect(self.accept)
        knopkiLayout.addWidget(okknopka)

        # Кнопка отмена
        otmenaknopka = QPushButton("Отмена")
        otmenaknopka.clicked.connect(self.reject)
        knopkiLayout.addWidget(otmenaknopka)


# Главное окно, в котором рисуется график функции
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.functionHistory = []  # Список для хранения истории функций
        self.functionLayout = QHBoxLayout()  # Макет на котором будут кнопки и изображение графика функции
        self.setWindowTitle("Изображение графиков функции")
        self.initUI()

    def initUI(self):
        # Центральный виджет главного окна
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        # Макет центрального виджета
        layout = QVBoxLayout(centralWidget)

        self.plotWidget = pg.PlotWidget() # PyQTGraph
        layout.addWidget(self.plotWidget)

        # Для ввода и истории
        inputLayout = QVBoxLayout()
        layout.addLayout(inputLayout)
        inputLayout.addLayout(self.functionLayout)

        # Названия для ввода значений
        functionLabel = QLabel("y = ")
        self.functionEdit = QLineEdit()
        xminLabel = QLabel("xmin = ")
        self.xminEdit = QLineEdit()
        xmaxLabel = QLabel("xmax = ")
        self.xmaxEdit = QLineEdit()
        self.functionLayout.addWidget(functionLabel)
        self.functionLayout.addWidget(self.functionEdit)
        self.functionLayout.addWidget(xminLabel)
        self.functionLayout.addWidget(self.xminEdit)
        self.functionLayout.addWidget(xmaxLabel)
        self.functionLayout.addWidget(self.xmaxEdit)

        buildknopka = QPushButton("Построить график") # Кнопка для построения функции на координатной плоскости
        buildknopka.clicked.connect(self.buildknopka)
        self.functionLayout.addWidget(buildknopka)

        historyknopka = QPushButton("История") # Кнопка для истории
        historyknopka.clicked.connect(self.historyknopka)
        self.functionLayout.addWidget(historyknopka)

        saveknopka = QPushButton("Сохранить") # Кнопка для сохранения картинки
        saveknopka.clicked.connect(self.saveknopka)
        inputLayout.addWidget(saveknopka)

        # Для демонстрации значений координат, на которые наведен курсор мыши
        self.plotWidget.getPlotItem().scene().sigMouseMoved.connect(self.coordmouse)
        self.coordinatesLabel = QLabel()
        self.functionLayout.addWidget(self.coordinatesLabel)

    def buildknopka(self):
        try:
            function = self.functionEdit.text()
            xmin = float(self.xminEdit.text())
            xmax = float(self.xmaxEdit.text())
        except ValueError:
            QMessageBox.warning(self, "Неправильный ввод", "Введите правильно функцию и/или диапазон значений икса.")
            return

        # Массив значений икса
        x = np.linspace(xmin, xmax, 100)

        # Функция при каждом из значений икса
        try:
            y = eval(function)
        except Exception:
            QMessageBox.warning(self, "Ошибка вычеслений", "Ошибка при вычислении функции. Введите правильно функцию.")
            return

        # Счетчик в истории
        self.functionHistory.append(f"{len(self.functionHistory) + 1}) {function} for x in [{xmin}, {xmax}]")

        # Очистить то, что было
        self.plotWidget.clear()

        # Добавить новое
        self.plotWidget.plot(x, y)

    def historyknopka(self):
        historyDialog = HistoryDialog(self.functionHistory)

        # Диаологовое окно истории и его закрытие
        result = historyDialog.exec_()
        if result == QDialog.Accepted:
            # Если "ОК"
            pass
        else:
            # Если "Отмена"
            pass

    def saveknopka(self):
        exporter = pyqtgraph.exporters.ImageExporter(self.plotWidget.plotItem)

        # Для открытия окна, в котором выбираем куда и как сохранить
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getSaveFileName(self, "Сохранение фото", "",
                                                  "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;All Files (*)",
                                                  options=options)

        # Сохраняем как
        if fileName:
            exporter.export(fileName)

    def coordmouse(self, event):
        # Получение координат
        x = event.x()
        y = event.y()
        # Преобразование координат мыши в данные
        data_coords = self.plotWidget.getPlotItem().vb.mapSceneToView(event)
        # Превращение в текст
        self.coordinatesLabel.setText(f"Координаты мыши: ({data_coords.x():.0f}, {data_coords.y():.0f})")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())