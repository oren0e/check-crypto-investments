from abc import ABC, abstractmethod
from typing import Optional, Tuple


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
    def process(self, local_data, remote_data):
        ...


class DataSender(ABC):
    @abstractmethod
    def send_message(self, msg) -> None:
        ...


class BaseBot:
    def __init__(
        self,
        functions: Optional[Tuple[DataProcessor]],
        local_inputs: Optional[DataReader],
        remote_inputs: Optional[DataReader],
        displayer: Optional[DataDisplayer],
        outputs: Optional[Tuple[DataSender]],
    ) -> None:
        self.functions = functions
        self.local_inputs = local_inputs
        self.remote_inputs = remote_inputs
        self.displayer = displayer
        self.outputs = outputs

    def run(self):
        local_data = self.local_inputs.get_data()
        remote_data = self.remote_inputs.get_data()
        raw_outputs = {}
        for function in self.functions:
            raw_outputs[function.NAME] = self.displayer.generate(function.process(local_data, remote_data))
        for output in self.outputs:
            for function_name in raw_outputs:
                output.send_message(raw_outputs[function_name])
