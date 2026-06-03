# vamos.py
import os
import math
import sys
from datetime import datetime, timedelta
from time import sleep
from config import *
import utils as u
from utils import bloqueo, docencia  

def get_sound():
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    from pygame import mixer
    mixer.init()
    sound = mixer.Sound("sounds/mixkit-discrete-door-bell-announcement-225.wav")
    sound.play()
    sleep(2)
    return

def calculate_time_difference(end_time_str):
    end_time = datetime.strptime(end_time_str, "%H:%M")
    current_time = datetime.now().time()
    current_datetime = datetime.combine(datetime.today(), current_time)
    end_datetime = datetime.combine(datetime.today(), end_time.time())
    time_difference = end_datetime - current_datetime
    minutes_left = time_difference.total_seconds() / 60.
    return math.ceil(minutes_left)


def check_block_delay(start_time, threshold_min=2):
    """Verifica si ha pasado más de threshold_min desde el inicio"""
    current_time = datetime.now()
    delay = (current_time - start_time).total_seconds() / 60.
    if delay > threshold_min:
        print(u.get_msg('late_start', delay=delay))
    return delay


def block_length(target_minutes, target_hour, rest):
    current_time = datetime.now()
    
    work_end_minutes = target_minutes - int(rest)
    if work_end_minutes < 0:
        work_end_minutes += 60
        work_end_hour = target_hour - 1
    else:
        work_end_hour = target_hour
        
    current_datetime = datetime.combine(current_time.date(), current_time.time())
    work_end_datetime = current_datetime.replace(
        hour=int(work_end_hour) % 24, 
        minute=int(work_end_minutes))
        
    if work_end_datetime <= current_datetime:
        work_end_datetime += timedelta(hours=1)
        
    delta = work_end_datetime - current_datetime
    block_mins = int(delta.total_seconds()/60.)

    if Testing:
        print(f'{u.get_msg("debug_block")} target={target_hour}:{target_minutes:02d}',
              f'work_end={work_end_hour}:{work_end_minutes:02d}, {block_mins}min')
    return block_mins


def adjust_first_block(total_mins, minblock=14):
    max_block0 = 60-mins_res0
    if minblock > max_block0:
        return minblock, total_mins - minblock - int(mins_res0)
            
    current_time = datetime.now()
    current_minutes = current_time.minute
    if current_minutes <= (30 - mins_res0):
        target_minutes = 30
        target_hour = current_time.hour
    elif current_minutes <= max_block0:
        target_minutes = 0
        target_hour = current_time.hour + 1
    else:
        target_minutes = 30
        target_hour = current_time.hour + 1
    
    block0 = block_length(target_minutes, target_hour, mins_res0)
    if block0 < minblock:
        if target_minutes == 30:
            target_minutes = 0
            target_hour += 1
        else:
            target_minutes = 30
        block0 = block_length(target_minutes, target_hour, mins_res0)
    
    if block0 > total_mins:
        block0 = total_mins
        
    if total_mins - block0 >= mins_res0:
        remaining_mins = total_mins - block0 - int(mins_res0)
    else:
        remaining_mins = 0

    if Testing:
        print(u.get_msg('debug_total', total_mins=total_mins, rest=mins_res0))
        print(u.get_msg('debug_block0', block0=block0, remaining_mins=remaining_mins))
    return block0, remaining_mins


def get_last_block(bloques, hora_comienzo, str_mins=None):
    if str_mins and ":" in str_mins:
        end_time = datetime.strptime(str_mins, "%H:%M")
        end_datetime = datetime.combine(datetime.today(), end_time.time())
        last_start = hora_comienzo[-1]
        actual_duration = (end_datetime - last_start).total_seconds() / 60.
        if actual_duration > 0:
            bloques[-1] = actual_duration
    return bloques


def nuevas_horas(bloques, descansos, hora_comienzo, str_mins=None):
    nueva_hora_0 = [hora_comienzo[0]]
    nueva_hora_fin = []
    for i in range(len(bloques)-1):
        fin_actual = nueva_hora_0[i] + timedelta(minutes=bloques[i])
        nueva_hora_fin.append(fin_actual)
        inicio_siguiente = fin_actual + timedelta(minutes=descansos[i])
        nueva_hora_0.append(inicio_siguiente)

    nueva_hora_fin.append(datetime.strptime(str_mins, "%H:%M"))
    bloques = get_last_block(bloques, nueva_hora_0, str_mins=str_mins)
    
    if ((len(bloques) != len(nueva_hora_0)) or (len(bloques) != len(nueva_hora_fin))):
        print(u.get_msg('stop_debug')); sys.exit()

    if Testing:
        print(u.get_msg('debug_adjust'), f"{bloques}")
        print(u.get_msg('debug_times'),
              f"{[h.strftime('%H:%M') for h in nueva_hora_0]} \n",
              f"{[h.strftime('%H:%M') for h in nueva_hora_fin]}")        
        
    return bloques, nueva_hora_0, nueva_hora_fin


def adjust_last_block(bloques, hora_comienzo, hora_fin, str_mins=None, minblock=20, max_block=90):
    if len(bloques) < 2:
        return bloques, hora_comienzo, hora_fin

    bloques = get_last_block(bloques, hora_comienzo, str_mins=str_mins)
    descansos = [mins_res0 if i == 0 else mins_rest for i in range(len(bloques) - 1)]
    bloques, nueva_hora_0, nueva_hora_fin = nuevas_horas(bloques, descansos, hora_comienzo, str_mins=str_mins)
    
    last_block = bloques[-1]
    if minblock <= last_block <= max_block:
        return bloques, nueva_hora_0, nueva_hora_fin

    excess = last_block - max_block
    if Testing:
        print(f'{bloques} ({len(bloques)}):', u.get_msg('excess_msg', excess=excess))
        print(f'Descansos ({len(descansos)}): {descansos}')

    if excess > 0:
        if excess > minblock:
            bloques.insert(-1, max_block)
            bloques[-1] = excess
            descansos.append(mins_rest)
        else:
            bloques.insert(-1, last_block-excess-minblock)
            bloques[-1] = excess+minblock
            descansos.append(mins_res0)
        if Testing:
            print(u.get_msg('added_block', len=len(bloques)), f'{bloques}')
            print(u.get_msg('added_break', len=len(descansos)), f'{descansos}')

    bloques, nueva_hora_0, nueva_hora_fin = nuevas_horas(bloques, descansos, hora_comienzo, str_mins=str_mins)
    
    last_block = bloques[-1]
    if last_block < minblock:
        transfer = minblock - last_block
        if len(bloques) > 1:
            bloques[-2] -= transfer
            bloques[-1] += transfer
            if Testing:
                print(f'Bloques ajustados ({len(bloques)}):{bloques}')
        bloques, nueva_hora_0, nueva_hora_fin = nuevas_horas(bloques, descansos, nueva_hora_0, str_mins=str_mins)
    return bloques, nueva_hora_0, nueva_hora_fin


def get_mins_again():
    str_mins = input(u.get_msg('input_duration'))
    mins = get_mins(str_mins)
    return math.ceil(mins)


def get_mins(str_mins):
    if str_mins.isnumeric():
        mins = int(str_mins)
    elif ":" in str_mins:
        mins = calculate_time_difference(str_mins)
        if mins < 0:
            mins = get_mins_again()
    else:
        mins = get_mins_again()
    return math.ceil(mins)


def get_tfin(totm):
    minutes_to_add = totm
    current_time = datetime.now().time()
    current_datetime = datetime.combine(datetime.today(), current_time)
    new_datetime = current_datetime + timedelta(minutes=minutes_to_add)
    return new_datetime.strftime('%H:%M')

def get_tfin_message(totm, workon):
    tfin = get_tfin(totm)
    print(u.get_msg('focus_msg', tfin=tfin, obj=workon))
    return
    
def get_rest_message(minrest):
    tfin = get_tfin(minrest)
    print(u.get_msg('rest_msg', mins=int(minrest), tfin=tfin))
    return

def get_session_type():
    print(u.get_msg('session_type'))
    print(u.get_msg('type_1'))
    print(u.get_msg('type_2'))
    print(u.get_msg('type_3'))
    session_type = 3
    if not Testing:
        session_type = input(u.get_msg('choose_type'))
        while session_type not in ['1', '2', '3']:
            session_type = input(u.get_msg('invalid_type'))
    return session_type


def get_ready(session_type):
    if session_type == '1':
        print('\n   🔭 ', bloqueo)
        print('      ✨✨✨ ' + mipgl)    
        if not Testing:
            os.system("emacs " + path2project + " &")
            os.system("libreoffice " + path2papers + " &")
    elif session_type == '2':
        print('\n   📚 ', docencia)
    else:
        print('\n   ⚙️  ¡Al ataque!"')

    objetivos = u.get_msg('test_obj')
    if not Testing:
        objetivos = input(u.get_msg('ask_objective'))
    return objetivos


def verificar_objetivo(objetivo):
    # Obtener la pregunta de verificación según el idioma
    if lang == 'en':
        prompt = u.get_msg('verify_obj_en')
    else:
        prompt = u.get_msg('verify_obj_es')
    
    avance = input(prompt)
    
    # Normalizar la entrada según el idioma
    if lang == 'en':
        if avance.lower() in ['y', 'yes']:
            avanzado = 's'
        else:
            avanzado = 'n'
    else:
        if avance.lower() in ['s', 'si']:
            avanzado = 's'
        else:
            avanzado = 'n'

    if avanzado == 's':
        print(u.get_msg('goal_done'))
    else:
        print(u.get_msg('improve_next'))
        ttot = u.treflexion(s_respir, unit='s')
    return 


def work_block(mins, workon, Testing=False):
    get_tfin_message(mins, workon)
    
    if not Testing:
        secs = mins * 60.
        interval = 15 * 60.
        elapsed = 0

        while elapsed < secs:
            remaining = secs - elapsed
            display_interval = min(interval, remaining)
            sleep(display_interval)
            elapsed += display_interval
            
            mins_left = math.ceil((secs - elapsed) / 60.)
            if mins_left > 0:
                print(u.get_msg('time_left', mins=mins_left), end='', flush=True)
        print()
        get_sound()
    return mins * 60.


def rest_block(mbreak, Testing=False):
    get_rest_message(mbreak)
    if not Testing:
        sleep(mbreak*60.)
        get_sound()
    return mbreak


def preparar_siguiente_bloque(expected_start=None):
    workon = u.get_msg('test_obj')
    if not Testing:
        workon = input(u.get_msg('next_step'))
    
    if expected_start:
        check_block_delay(expected_start, threshold_min=2)
    return workon


def run_bloque_unico(objetivo, mins, Testing=False):
    totalt = work_block(mins, objetivo, Testing)
    if not Testing:
        verificar_objetivo(objetivo)
    return totalt


def run_sesion_completa(session_type, str_mins, minblock0=20, minblockn=30, twork=75, Testing=False):
    objetivo = get_ready(session_type)
    t_tot_cumu = 0.0
    
    total_mins = get_mins(str_mins)
    block0, t_resto = adjust_first_block(total_mins, minblock=minblock0)
    bloques = [block0]
    n_blocks = 1

    while t_resto > 0:
        remaining_blocks = max(1, int(t_resto/twork))
        next_block = min(mins_work, max(mins_work, t_resto/remaining_blocks))
        next_block = min(next_block, t_resto - mins_rest)
        if next_block < minblockn:
            break

        bloques.append(round(next_block))
        n_blocks += 1
        t_resto -= (next_block + mins_rest)
        
    hora_comienzo = [datetime.now()]
    hora_fin = []
    for i in range(len(bloques)):
        hora_fin.append(hora_comienzo[i] + timedelta(minutes=bloques[i]))
        if i < len(bloques) - 1:
            break_duration = mins_res0 if i == 0 else mins_rest
            hora_comienzo.append(hora_fin[i] + timedelta(minutes=break_duration))

    if str_mins and ":" in str_mins:
        end_time = datetime.strptime(str_mins, "%H:%M")
        end_datetime = datetime.combine(datetime.today(), end_time.time())
        hora_fin.append(end_datetime)
        
        if Testing:
            print(f'DEBUG: Antes de ajustar -> bloques: {bloques}')
            print(f'DEBUG: Antes de ajustar -> hora_comienzo:', f"{[h.strftime('%H:%M') for h in hora_comienzo]}")
        bloques, hora_comienzo, hora_fin = adjust_last_block(bloques, hora_comienzo, hora_fin, str_mins, minblock=minblockn, max_block=twork+5)
    else:
        hora_fin.append(str_mins) 

    print(u.get_msg('structure'))               
    for i, (hi, hf, b) in enumerate(zip(hora_comienzo, hora_fin, bloques)):
        print(u.get_msg('block_info', i=i, hi=hi.strftime("%H:%M"), hf=hf.strftime("%H:%M"), mins=math.ceil(b)))         

    hi=hora_comienzo[0]
    hf=hora_fin[0]
    print(f'\n🌱 Bloque {0} ({hi.strftime("%H:%M")} - {hf.strftime("%H:%M")}): {math.ceil(b)} min')
    iobj = preparar_siguiente_bloque(expected_start=hora_comienzo[0])
    
    for i, block_mins in enumerate(bloques):        
        t_tot_cumu += run_bloque_unico(iobj, block_mins, Testing=Testing)
        
        if i < (len(bloques) - 1):
            hi=hora_comienzo[i+1]
            hf=hora_fin[i+1]
            print(f'\n🌱 Bloque {i+1} ({hi.strftime("%H:%M")} - {hf.strftime("%H:%M")}): {math.ceil(b)} min')
            iobj = preparar_siguiente_bloque(expected_start=hora_comienzo[i+1])
            
            next_block_start = hora_comienzo[i+1]
            current_time = datetime.now()
            available_break = (next_block_start - current_time).total_seconds() / 60.
            mbreak = min(mins_rest, max(0, available_break))
        
            if mbreak > 0:
                t_tot_cumu += rest_block(mbreak, Testing=Testing)
            elif available_break < 0:
                print(u.get_msg('delay_msg'))    
        if Testing: break
    return t_tot_cumu, objetivo

def print_summary(totalt, objetivo, es_bloque, Testing=False):
    ms, s = divmod(totalt, 60)
    h, m = divmod(ms, 60)
    print("\n")
    
    if h > 1:
        # PASAR LOS ARGUMENTOS AQUÍ
        msg = u.get_msg('summary_hours', h=int(h), m=int(m))
    elif h > 0:
        msg = u.get_msg('summary_hour', h=int(h), m=int(m))
    else:
        msg = u.get_msg('summary_min', m=int(m))
        
    print(msg, '\033[1;32m{}\033[0m'.format(objetivo))
    
    if not es_bloque and not Testing:
        verificar_objetivo(objetivo)
        print(u.get_msg('enjoy_q'))
        ttot = u.treflexion(s_respir/2, unit='s', Testing=Testing)
        print(u.get_msg('improve_q'))
        ttot = u.treflexion(s_respir/2, unit='s', Testing=Testing)
    return


def sesion():
    print(u.get_msg('prepare_session'))
    print(u.get_msg('ask_duration'))
    str_mins = input('       ') 
    
    firstmins = get_mins(str_mins)
    
    threshold = mins_work
    es_bloque = firstmins <= threshold
    if Testing:
        print(f'Hay {firstmins} min disponibles')
        print(f'Tiempo mínimo para sesión = {threshold} min')
        print(f'¿Es un bloque de trabajo? {es_bloque}')
        
    totalt = 0.; obj = u.get_msg('test_obj')
    if es_bloque:
        while True and not Testing:
            obj = input('    📋 ¿Qué objetivo tienes para este bloque de trabajo? ')
            totalt += run_bloque_unico(obj, firstmins, Testing=Testing)
            
            continuoq = input(u.get_msg('continue_q'))
            # Ajustar good_answer para aceptar 'y' en inglés
            if lang == 'en':
                opciones = ['y', 'n']
            else:
                opciones = ['s', 'n']
            continuo = u.good_answer(continuoq, options=opciones)
            
            if continuo == 'n':
                break
    else:
        tipo = get_session_type()
        totalt, obj = run_sesion_completa(tipo, str_mins, minblock0=mins_b_0, minblockn=mins_b_n, twork=mins_work, Testing=Testing)

    print_summary(totalt, obj, es_bloque, Testing=Testing)
    print('      ✨✨✨ \n')        

if __name__ == "__main__":
    sesion()
