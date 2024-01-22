class Conditions:
    '''Условия'''

    def __init__(self):
        pass

    def conditions_1(self, ec, ec0, esi_dop):
        '''Определяем допустимое значение питания стока'''
        res = 0.5 * (ec0 + esi_dop)
        if ec < res:
            return True
        else:
            return False

    def condition_2(self):
        pass