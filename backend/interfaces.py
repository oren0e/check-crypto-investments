from abc import abstractmethod, ABC
from typing import List


class DataReader(ABC):
    @abstractmethod
    def get_data(self):
        ...


class DataDisplayer(ABC):
    @abstractmethod
    def generate(self, data) -> str:
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
    def send_message(self, msg) -> None:
        ...


class BaseBot:
    def __init__(self, functions: List[DataProcessor], inputs: DataReader, displayer: DataDisplayer, outputs: List[DataSender]) -> None:
        self.functions = functions
        self.inputs = inputs
        self.displayer = displayer
        self.outputs = outputs

    def run(self):
        data = self.inputs.get_data()
        raw_outputs = {}
        for function in self.functions:
            raw_outputs[function.NAME] = self.displayer.generate(function.process(data))
        for output in self.outputs:
            for function_name in raw_outputs:
                output.send_message(raw_outputs[function_name])
