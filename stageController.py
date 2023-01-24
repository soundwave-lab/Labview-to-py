
import pyvisa
import time

#　　　　　　　　　　　　↓↓↓↓　三軸コマンドのurl　↓↓↓↓
# https://jp.optosigma.com/html/jp/software/motorize/manual_jp/SHOT-302GS_304GS.pdf


class StageController:
    rm_ = pyvisa.ResourceManager()

    def __init__(self, interface):  # 接続先を指定
        self._stage = self.rm_.open_resource(interface)

    def max_speed(self):
        self._stage.write(
            "D:WS500000F500000R0S500000F500000R0S500000F500000R0S500000F500000R0")

    def change_speed(self, min_speed, max_speed, acce_time):
        self._stage.write(
            f"D:WS{min_speed}F{max_speed}R{acce_time}S{min_speed}F{max_speed}R{acce_time}S{min_speed}F{max_speed}R{acce_time}S{min_speed}F{max_speed}R{acce_time}")

    # 原点復帰
    def to_zero(self):
        self._stage.write("A:W+P0+P0+P0+P0")
        self._stage.write("G:")
        time.sleep(1)

    # 原点指定
    def set_zero(self):
        self._stage.write("R:W")

    # 移動量指定(正方向移動)　パルス数で指定(三軸ごとに1パルスの移動量が違うので)
    def move_one(self, axis, puls):
        puls = self.__plus_check(puls)
        self._stage.write(f"M:{axis}{puls}")
        self._stage.write("G:")
        time.sleep(0.13)

    # 移動場所指定
    def move_to_rel(self, puls1, puls2, puls3, puls4):
        puls1 = self.__plus_check(puls1)
        puls2 = self.__plus_check(puls2)
        puls3 = self.__plus_check(puls3)
        puls4 = self.__plus_check(puls4)
        self._stage.write(f"M:W"+puls1+puls2+puls3+puls4)
        self._stage.write("G:")
        time.sleep(0.13)

    # 移動場所指定
    def move_to_abs(self, puls1, puls2, puls3, puls4):
        puls1 = self.__plus_check(puls1)
        puls2 = self.__plus_check(puls2)
        puls3 = self.__plus_check(puls3)
        puls4 = self.__plus_check(puls4)
        self._stage.write(f"A:W"+puls1+puls2+puls3+puls4)
        self._stage.write("G:")
        time.sleep(0.13)

    def status(self):
        return self._stage.query("Q:")

    def __plus_check(self, plus):
        if plus >= 0:
            command = "+P"+str(plus)
        else:
            command = "-P"+str(abs(plus))
        return command
