import os

# 디스플레이 환경변수가 없으면 :0으로 설정
# 원격 명령으로 실행하는 경우 DISPLAY 환경변수가 없습니다.
if os.environ.get("DISPLAY") == None:
    os.environ["DISPLAY"] = ":0"
    print("DISPLAY environment variable set to :0")

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QTextEdit
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QScrollArea
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import QProcess

from src.config import MODEL_COMMENDS


class DemoAppMainWindow(QMainWindow):
    """메인 윈도우"""

    __log_limit: int = 1000
    __cmd_buttons: list
    __process: object
    __pending_command: str

    def __init__(self, parent=None):
        """생성자"""
        super().__init__(parent)
        self.setWindowTitle("Hanulsoft Jetson Demo")
        self.__init_ui()
        self.__process = None
        self.__pending_command = None

    def __init_ui(self):
        """UI 초기화"""
        self.setStyleSheet("font-size: 24px;")
        self.log_terminal = QTextEdit()
        self.log_terminal.setReadOnly(True)
        self.log_terminal.setMinimumWidth(800)

        model_select_area = QScrollArea(self)
        model_select_widget = QWidget()
        model_select_layout = QVBoxLayout()

        self.__cmd_buttons = []
        for model_cmd in MODEL_COMMENDS:
            model_name, model_network = model_cmd.split(" ")
            model_button = QPushButton(f"{model_name}: {model_network}")
            model_button.setStyleSheet("text-align:left;")
            model_button.clicked.connect(
                lambda _, btn=model_button, cmd=model_cmd: self.on_model_button_click(
                    btn, cmd
                )
            )
            model_select_layout.addWidget(model_button)
            model_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.__cmd_buttons.append(model_button)
        model_select_widget.setLayout(model_select_layout)
        model_select_area.setWidget(model_select_widget)
        model_select_area.setMinimumWidth(570)

        main_widget = QWidget(self)
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.log_terminal, 1)
        main_layout.addWidget(model_select_area)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        return

    def __execute_command(self, command):
        """명령 실행"""
        self.__process = QProcess(self)
        self.__process.finished.connect(self.__on_process_finished)
        self.__process.readyReadStandardOutput.connect(self.__on_stdout_ready)
        self.__process.readyReadStandardError.connect(self.__on_stderr_ready)
        self.__process.start(command)

    def __on_stdout_ready(self):
        """표준 출력 준비 완료"""
        text = self.__process.readAllStandardOutput().data().decode()
        self.log_terminal.append(text)
        self.__trim_log_terminal()

    def __on_stderr_ready(self):
        """표준 에러 준비 완료"""
        text = self.__process.readAllStandardError().data().decode()
        self.log_terminal.append(text)
        self.__trim_log_terminal()

    def __trim_log_terminal(self):
        """로그 터미널의 줄 수가 1000줄을 초과하면 가장 오래된 줄을 제거합니다."""
        text = self.log_terminal.toPlainText()
        lines = text.split("\n")

        if len(lines) > self.__log_limit:
            new_text = "\n".join(lines[len(lines) - self.__log_limit :])
            self.log_terminal.setPlainText(new_text)

    def __on_process_finished(self):
        """프로세스 종료"""
        if self.__pending_command:
            command = self.__pending_command
            self.__pending_command = None
            self.__execute_command(command)
        return

    def show(self):
        """표시"""
        super().show()
        display_geometry = QApplication.desktop().screenGeometry()
        w, h = display_geometry.width() * 2 / 3, display_geometry.height()
        x, y = display_geometry.width() * 1 / 3, 0
        self.setGeometry(int(x), int(y), int(w), int(h))

    def on_model_button_click(self, button, menu):
        """모델 버튼 클릭"""
        mode, network = menu.split(" ")
        if mode == "backgroundnet":
            command = f"{mode} --replace=src/images/background_net.png --network={network} csi://0"
        else:
            command = f"{mode} --network={network} csi://0"
        print(f"on_model_button_click: {command}")
        for btn in self.__cmd_buttons:
            btn.setEnabled(True)
        button.setEnabled(False)
        if self.__process and self.__process.state() == QProcess.Running:
            self.__pending_command = command
            self.__process.terminate()
        else:
            self.__execute_command(command)
        return


if __name__ == "__main__":
    app = QApplication([])
    window = DemoAppMainWindow()
    window.show()
    app.exec_()
