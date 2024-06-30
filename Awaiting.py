import inspect
from threading import Condition
from typing import Callable, Dict


class Awaiting:
    def __init__(self):
        self.ref_map: Dict[str, Condition] = dict()

    def __get_condition(
            self,
            func_name: str
    ) -> Condition:
        cond = self.ref_map.get(func_name, None)
        if cond is None: self.ref_map[func_name] = Condition()
        return self.ref_map[func_name]

    def notify(self) -> None:
        func_name: str = tuple(map(
            lambda x: x.function,
            inspect.stack()
        ))[1]
        cond = self.__get_condition(func_name)
        with cond: cond.notify()

    def wait_for(
            self,
            func_name: str,
            condition: Callable[[], bool]
    ) -> None:
        cond = self.__get_condition(func_name)
        with cond:
            while not condition(): cond.wait()


awaiting = Awaiting()
