def to_kg(amount:float, unit:str)->float:
    if unit=='kg': return amount
    if unit=='g': return amount/1000
    if unit=='l': return amount
    if unit=='ml': return amount/1000
    if unit=='szt': return amount
    raise ValueError('unknown unit')
