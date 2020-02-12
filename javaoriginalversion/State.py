class State : #市民状态
    NORMAL = 0 #未被感染
    SHADOW = NORMAL + 1 #潜伏者
    CONFIRMED = SHADOW + 1 #感染者
    FREEZE = CONFIRMED + 1 #已隔离