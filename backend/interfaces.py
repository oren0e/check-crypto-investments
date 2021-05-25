from abc import abstractmethod, ABC
from typing import List, Dict


class DataReader(ABC):
    @abstractmethod
    def get_data(self):
        ...


class DataDisplayer(ABC):
    @abstractmethod
    def generate(self) -> str:
       """
       Generates formatted text to be ready to send via send method
       """


class DataProcessor(ABC):
    NAME: str
    
    @abstractmethod
    def process(self, data):
        ...


class DataSender(ABC):
    @abstractmethod
    def send_message(self) -> None:
        ...


class BaseBot:
    functions: List[DataProcessor]
    inputs: DataReader
    displayer: DataDisplayer
    outputs: List[DataSender]

    def run(self):
        data = self.inputs.get_data()
        raw_outputs = {}
        for function in functions:
            raw_outputs[function.NAME] = displayer.generate(function.process(data))
        for output in outputs:
            for function_name in raw_outputs:
                output.send_message(raw_outputs[function_name])
