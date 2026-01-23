from dataclasses import dataclass


@dataclass
class WellData:
    cmt5_time: int
    dP: float
    gVF: float
    gasFlowRate: float
    liquidFlowRate: float
    oilFlowRate: float
    pressure: float
    temperature: float
    waterCut: float
    waterFlowRate: float

    @staticmethod
    def from_dict(data: dict[str, str]) -> 'WellData':
        return WellData(
            cmt5_time=int(data['cmt5_time']),
            dP=float(data['dP']),
            gVF=float(data['gVF']),
            gasFlowRate=float(data['gasFlowRate']),
            liquidFlowRate=float(data['liquidFlowRate']),
            oilFlowRate=float(data['oilFlowRate']),
            pressure=float(data['pressure']),
            temperature=float(data['temperature']),
            waterCut=float(data['waterCut']),
            waterFlowRate=float(data['waterFlowRate']),
        )

