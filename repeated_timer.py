import time
from threading import Timer
from datetime import datetime


# timer function
def on_timer_function():
    print("hello, world")


class RepeatedTimer(object):
    nruns = 0

    def __init__(self, times, function, *args, **kwargs):
        self._timer = None
        self.function = function
        self.times = times
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, tm=type(self), **self.kwargs)

    def start(self):

        if self.times[1] != -1 and type(self).nruns >= self.times[1]:
            self.stop()
            # больше ничего не перезапускаем
            return

        if not self.is_running:
            # если число запусков не бесконечно (-1) и оно превысило переданное значение
            self._timer = Timer(self.times[0], self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


def timer(start, **kwargs):
    # получаем текущее время для сравнения
    now = datetime.today().strftime("%H:%M:%S")
    tm = kwargs.get('tm')  # объект нашего класса таймера (не экземпляр!)

    print(now, tm.nruns)  # просто дебаг
    # првоеряем не подошло ли время...
    if str(now) == start:
        on_timer_function()  # функция, которая должна быть запущена в опред. время
        tm.nruns += 1  # считаем число запусков


def main():
    time.sleep(100)
    print('end main')


if __name__ == "__main__":
    # запускаем проверку каждую секунду, запуск функции - ровно 1 раз (-1 бесконечно)
    rt = RepeatedTimer((1., -1), timer, '21:37:00')
    try:
        main()  # your long-running job goes here...
    finally:
        rt.stop()