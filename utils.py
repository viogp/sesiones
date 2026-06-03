import time

bloqueo = ('Estar bloqueada es más duro y difícil que ir haciendo. \n')
docencia = ('La docencia es una oportunidad para clarificar tus ideas y ampliar tu legado. \n')

def good_answer(answer, options=['s','n']):
    isgood = False
    while not isgood:
        if answer in options:
            isgood = True
        else:
            answer = input('No te he entendido, escribe s o n: ')
    return answer


def treflexion(tt,unit='min',Testing=False):
    if unit=='min':
        print(f'     Tienes {tt} min.\n')
        ttot = tt
        if not Testing:
            time.sleep(tt*60.)    
    elif unit=='s':
        ttot = tt/60.
        if not Testing:
            time.sleep(tt)    
    return ttot


