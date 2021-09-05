from backend.displayers import GasDisplayer, ReturnsDisplayer
from backend.interfaces import BaseBot
from backend.processors import ReturnsProcessor
from backend.readers import GasReader, InvestmentReader, PricesReader
from backend.senders import TelegramSender
from config.credentials import parse_credentials

credentials = parse_credentials()


class CCIBot(BaseBot):
    def __init__(self) -> None:
        super().__init__(
            (ReturnsProcessor(),),
            InvestmentReader(),
            PricesReader(vs_currency="usd"),
            ReturnsDisplayer(),
            (TelegramSender(api_token=credentials["cci_bot"]["api_token"], chat_id=credentials["cci_bot"]["chat_id"]),),
        )

    def run(self):
        local_data = self.local_inputs.get_data()
        remote_data = self.remote_inputs.get_data()
        raw_outputs = {}
        for function in self.functions:
            raw_outputs[function.NAME] = self.displayer.generate(
                function.process(local_data, remote_data)
            ) + GasDisplayer().generate(GasReader().get_data())
        for output in self.outputs:
            for function_name in raw_outputs:
                output.send_message(raw_outputs[function_name])


class CGroupBot(BaseBot):
    def __init__(self) -> None:
        super().__init__(
            None,
            None,
            GasReader(),
            GasDisplayer(),
            (
                TelegramSender(
                    api_token=credentials["cgroup_bot"]["api_token"], chat_id=credentials["cgroup_bot"]["chat_id"]
                ),
            ),
        )

    def run(self):
        remote_data = self.remote_inputs.get_data()
        msg = self.displayer.generate(remote_data)
        for output in self.outputs:
            output.send_message(msg)
