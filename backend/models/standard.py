from sqlalchemy import Column, Integer, String, Float
from config.rds import metadata

class StandardTable(object): 
    id = Column(Integer, primary_key=True, autoincrement=True)
    aircraftsernum_1 = Column(Float)
    phaseofflight_1 = Column(Float)
    amschprsovdrivf_1a = Column(Float)
    amschprsovdrivf_1b = Column(Float)
    amschprsovdrivf_2b = Column(Float)
    amscprsovdrivf_1a = Column(Float)
    amscprsovdrivf_1b = Column(Float)
    amscprsovdrivf_2b = Column(Float)
    basbleedlowpressf_1a = Column(Float)
    basbleedlowpressf_2b = Column(Float)
    basbleedlowtempf_1a = Column(Float)
    basbleedlowtempf_2b = Column(Float)
    basbleedoverpressf_1a = Column(Float)
    basbleedoverpressf_2b = Column(Float)
    basbleedovertempf_1a = Column(Float)
    basbleedovertempf_2b = Column(Float)
    bleedfavtmcmd_1a = Column(Float)
    bleedfavtmcmd_1b = Column(Float)
    bleedfavtmcmd_2a = Column(Float)
    bleedfavtmcmd_2b = Column(Float)
    bleedfavtmfbk_1a = Column(Float)
    bleedfavtmfbk_1b = Column(Float)
    bleedfavtmfbk_2b = Column(Float)
    bleedhprsovcmdstatus_1a = Column(Float)
    bleedhprsovcmdstatus_1b = Column(Float)
    bleedhprsovcmdstatus_2a = Column(Float)
    bleedhprsovcmdstatus_2b = Column(Float)
    bleedHprsovopposstatus_1a = Column(Float)
    bleedhprsovopposstatus_1b = Column(Float)
    bleedHprsovopposstatus_2a = Column(Float)
    bleedHprsovopposstatus_2b = Column(Float)
    bleedmonpress_1a = Column(Float)
    bleedmonpress_1b = Column(Float)
    bleedmonpress_2a = Column(Float)
    bleedmonpress_2b = Column(Float)
    bleedonstatus_1a = Column(Float)
    bleedonstatus_1b = Column(Float)
    bleedonstatus_2b = Column(Float)
    bleedoverpresscas_2a = Column(Float)
    bleedoverpresscas_2b = Column(Float)
    bleedprecooldiffpress_1a = Column(Float)
    bleedprecooldiffpress_1b = Column(Float)
    bleedprecooldiffpress_2a = Column(Float)
    bleedprecooldiffpress_2b = Column(Float)
    bleedhprsovopposstatus_1a = Column(Float)
    bleedhprsovopposstatus_2a = Column(Float)
    date = Column(String)
    duration = Column(Float)
    cumulative_duration = Column(Float)
    time_to_failure = Column(Float)
