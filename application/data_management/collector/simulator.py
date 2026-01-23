import logging
import random
import time

import pandas as pd

from application.data_management.models.well_data import WellData
from application.data_management.processor.data_processor import DataProcessor


class SimulatorCollector:

    def __init__(self, processor: DataProcessor):
        self.processor = processor
        self.running = False

    def start(self):
        """启动采集循环"""
        self.running = True

        while self.running:
            logging.info("SimulatorCollector 采集数据中...")
            device_id, data = self.collect()
            self.processor.process(device_id, data)
            time.sleep(60)

    def stop(self):
        """停止采集循环"""
        self.running = False

    def collect(self) -> tuple:
        """
        读取数据
        """
        # 先使用虚拟数据模拟
        sheet_data = pd.read_excel('../data/Caveman423.xlsx')
        columns_len = len(sheet_data.columns)
        random_column = random.randrange(0, columns_len)
        selected_column = sheet_data.iloc[random_column].to_dict()
        device_id = 'well-1'
        selected_column['cmt5_time'] = selected_column['cmt5_time'].timestamp()

        well_data = WellData.from_dict(selected_column)

        logging.info(f"{device_id} 采集到数据: {well_data}")

        return device_id, well_data


if __name__ == '__main__':

    collector = SimulatorCollector()
    collector.start()
