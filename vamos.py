import os
import math
import sys
from datetime import datetime, timedelta
from time import sleep
from config import *
import utils as u

def get_sound():
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    from pygame import mixer

    script_dir = os.path.dirname(os.path.abspath(__file__))
    rel_path   = "sounds/mixkit-discrete-door-bell-announcement-225.wav"
    sound_path = os.path.join(script_dir,rel_path)
    
    mixer.init()
    sound = mixer.Sound(sound_path)
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
        print(f'DEBUG (block_length):',
              f'target={target_hour}:{target_minutes:02d}',
              f'work_end={work_end_hour}:{work_end_minutes:02d}, {block_mins}min')
    return block_mins


def adjust_first_block(total_mins, minblock=14):
    """
    Ajusta el primer bloque de trabajo para que el descanso termine a :30 o :00.
    Si end_time_str se proporciona, usa esa hora como referencia.
    """   
    # Establecer un límite máximo para el primer bloque
    max_block0 = 60-mins_res0
    if minblock > max_block0:
        return minblock, total_mins - minblock - int(mins_res0)
            
    # Determinar el primer objetivo (:30 o :00)
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
    
    # Minutos del primer bloque
    block0 = block_length(target_minutes,target_hour,mins_res0)
    if block0 < minblock:
        if target_minutes == 30:
            target_minutes = 0
            target_hour += 1
        else:
            target_minutes = 30
        block0 = block_length(target_minutes,target_hour,mins_res0)
    
    if block0 > total_mins:
        block0 = total_mins
        
    if total_mins - block0 >= mins_res0:
        remaining_mins = total_mins - block0 - int(mins_res0)
    else:
        remaining_mins = 0

    if Testing:
        print(f'  total_mins={total_mins:.1f}, initial rest={mins_res0}')
        print(f'  block0={block0}, remaining_mins={remaining_mins:.1f}')
    return block0, remaining_mins


def get_last_block(bloques,hora_comienzo,str_mins=None):
    # Ajustar último bloque si hay str_mins especificado
    if str_mins and ":" in str_mins:
        end_time = datetime.strptime(str_mins, "%H:%M")
        end_datetime = datetime.combine(datetime.today(), end_time.time())
        last_start = hora_comienzo[-1]

        # Actualizar el último bloque con la duración real
        actual_duration = (end_datetime - last_start).total_seconds() / 60.
        if actual_duration > 0:
            bloques[-1] = actual_duration
    return bloques


def nuevas_horas(bloques,descansos,hora_comienzo,str_mins=None):
    # Reajustar las horas de comienzo de los bloques
    nueva_hora_0 = [hora_comienzo[0]]
    nueva_hora_fin = []
    for i in range(len(bloques)-1):
        # Calcular fin del bloque actual
        fin_actual = nueva_hora_0[i] + timedelta(minutes=bloques[i])
        nueva_hora_fin.append(fin_actual)
            
        # Calcular inicio del siguiente bloque
        inicio_siguiente = fin_actual + timedelta(minutes=descansos[i])
        nueva_hora_0.append(inicio_siguiente)

    # Recalcular la duración del último bloque dada la hora de finalización
    nueva_hora_fin.append(datetime.strptime(str_mins, "%H:%M"))
    bloques = get_last_block(bloques,nueva_hora_0,str_mins=str_mins)
    if ((len(bloques) != len(nueva_hora_0)) or
        (len(bloques) != len(nueva_hora_fin))):
        print('STOP: need debugging nuevas_horas'); sys.exit()

    if Testing:
        print(f'DEBUG (nuevas_horas): Bloques ajustados \n',f"{bloques}")
        print(f'DEBUG (nuevas_horas): Horas de comienzo y fin ajustadas \n',
              f"{[h.strftime('%H:%M') for h in nueva_hora_0]} \n",
              f"{[h.strftime('%H:%M') for h in nueva_hora_fin]}")        
        
    return bloques,nueva_hora_0,nueva_hora_fin



def adjust_last_block(bloques, hora_comienzo, hora_fin,
                      str_mins=None, minblock=20, max_block=90):
    """
    Ajusta el último bloque. Si es demasiado largo, lo divide.
    Devuelve la lista de bloques corregida y las horas recalculadas.
    """
    if len(bloques) < 2:
        return bloques, hora_comienzo, hora_fin

    bloques = get_last_block(bloques,hora_comienzo,str_mins=str_mins)
    descansos = [mins_res0 if i == 0 else mins_rest for i in range(len(bloques) - 1)]
    bloques,nueva_hora_0,nueva_hora_fin = nuevas_horas(bloques,
                                                       descansos,
                                                       hora_comienzo,
                                                       str_mins=str_mins)
    last_block = bloques[-1]
    if minblock <= last_block <= max_block:
        # Si el último bloque ya está dentro del rango aceptable, no hacer nada
        return bloques, nueva_hora_0, nueva_hora_fin

    excess = last_block - max_block
    if Testing:
        print(f'{bloques} ({len(bloques)}):',
              f'el último bloque tiene un exceso de {excess:.1f}')
        print(f'Descansos ({len(descansos)}): {descansos}')

    if excess > 0:
        # Insertar nuevo bloque antes del último
        if excess > minblock:
            bloques.insert(-1, max_block)
            bloques[-1] = excess
            descansos.append(mins_rest)
        else:
            bloques.insert(-1, last_block-excess-minblock)
            bloques[-1] = excess+minblock
            descansos.append(mins_res0)
        if Testing:
            print(f'Bloque añadido ({len(bloques)}):{bloques}')
            print(f'Descanso añadido ({len(descansos)}): {descansos}')

    bloques,nueva_hora_0,nueva_hora_fin = nuevas_horas(bloques,
                                                       descansos,
                                                       hora_comienzo,
                                                       str_mins=str_mins)
    # Comprobar que el último bloque no sea demasiado corto
    last_block = bloques[-1]
    if last_block < minblock:
        transfer = minblock - last_block
        # Tomar tiempo del bloque anterior
        if len(bloques) > 1:
            bloques[-2] -= transfer
            bloques[-1] += transfer
            if Testing:
                print(f'Bloques ajustados ({len(bloques)}):{bloques}')
        bloques,nueva_hora_0,nueva_hora_fin = nuevas_horas(bloques,
                                                           descansos,
                                                           nueva_hora_0,
                                                           str_mins=str_mins)
    return bloques, nueva_hora_0, nueva_hora_fin


def get_mins_again():
    str_mins = input(u.get_msg('input_duration'))
    mins = get_mins(str_mins)
    return math.ceil(mins)


def get_mins(str_mins):
    """Devuelve los minutos totales"""
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
        print('\n   🔭 ', u.get_msg('bloqueo'))
        print('      ✨✨✨ ' + mipgl)    
        if not Testing and info_projects:
            os.system(path2project)
            os.system(path2papers)
    elif session_type == '2':
        print('\n   📚 ', u.get_msg('docencia'))
    else:
        print('\n   ⚙️  ¡Al ataque!"')

    objetivos = "test"
    if not Testing:
        objetivos = input(u.get_msg('ask_objective'))
    return objetivos


def verificar_objetivo(objetivo,Testing=False):
    """
    Función para verificar el cumplimiento del objetivo
    """
    avance = 's'
    if not Testing:
        avance = input(u.get_msg('goal_check'))
    avanzado = u.get_sn(avance)

    if avanzado == 's':
        print(u.get_msg('goal_done'))
    else:
        print(u.get_msg('improve_next'))
        ttot = u.treflexion(s_respir, unit='s')
    return 


def work_block(mins, workon, Testing=False):
    """Ejecuta un bloque de trabajo con contador de tiempo"""
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
    """Ejecuta un bloque de descanso"""
    get_rest_message(mbreak)
    if not Testing:
        sleep(mbreak*60.)
        get_sound()
    return mbreak


def preparar_siguiente_bloque(expected_start=None):
    """Solicita el objetivo y el primer paso para el siguiente bloque"""
    workon = "test"
    if not Testing:
        workon = input(u.get_msg('next_step'))
    
    if expected_start:
        check_block_delay(expected_start, threshold_min=2)
    return workon


def run_bloque_unico(objetivo, mins, Testing=False):
    """
    Ejecuta UN solo bloque de trabajo.
    """
    totalt = work_block(mins, objetivo, Testing)
    
    # Comprobar si se ha cumplido el objetivo
    verificar_objetivo(objetivo, Testing=Testing)

    return totalt


def run_sesion_completa(session_type, str_mins,
                        minblock0=20,minblockn=30,
                        twork=75,Testing=False):
    """
    Ejecuta una sesión completa con múltiples bloques.
    Distribuye el tiempo en bloques de mins_work a mins_work.
    """
    objetivo = get_ready(session_type)
    t_tot_cumu = 0.0
    
    # Ajustar primer bloque para alinearse con :00 o :30
    total_mins = get_mins(str_mins)
    block0, t_resto = adjust_first_block(total_mins,minblock=minblock0)
    bloques = [block0]
    n_blocks = 1

    while t_resto > 0:
        # Calcular tamaño del siguiente bloque
        remaining_blocks = max(1, int(t_resto/twork))
        next_block = min(mins_work, max(mins_work, t_resto/remaining_blocks))
        next_block = min(next_block, t_resto - mins_rest)  # Dejar espacio para descanso
        if next_block < minblockn:
            break

        bloques.append(round(next_block))
        n_blocks += 1
        t_resto -= (next_block + mins_rest)
        
    # Calcular horas de comienzo y fin
    hora_comienzo = [datetime.now()]
    hora_fin = []
    for i in range(len(bloques)):
        hora_fin.append(hora_comienzo[i] + timedelta(minutes=bloques[i]))
        if i < len(bloques) - 1:
            break_duration = mins_res0 if i == 0 else mins_rest
            hora_comienzo.append(hora_fin[i] + timedelta(minutes=break_duration))

    # Hora de finalización y ajustar el último bloque
    if str_mins and ":" in str_mins:
        end_time = datetime.strptime(str_mins, "%H:%M")
        end_datetime = datetime.combine(datetime.today(), end_time.time())
        hora_fin.append(end_datetime)
        
        if Testing:
            print(f'DEBUG: Antes de ajustar -> bloques: {bloques}')
            print(f'DEBUG: Antes de ajustar -> hora_comienzo:',
                  f"{[h.strftime('%H:%M') for h in hora_comienzo]}")
        bloques, hora_comienzo, hora_fin = adjust_last_block(bloques, hora_comienzo,
                                                             hora_fin, str_mins,
                                                             minblock=minblockn,
                                                             max_block=twork+5)
    else:
        hora_fin.append(str_mins) 

    print(u.get_msg('structure'))               
    for i, (hi, hf, b) in enumerate(zip(hora_comienzo, hora_fin, bloques)):
        print(u.get_msg('block_summary'),f'{i} ({hi.strftime("%H:%M")} -',
              f'{hf.strftime("%H:%M")}): {math.ceil(b)} min')         

    # Ejecutar los bloques
    hi=hora_comienzo[0]
    hf=hora_fin[0]
    print(u.get_msg('block'),f'{0} ({hi.strftime("%H:%M")} -',
          f'{hf.strftime("%H:%M")}): {math.ceil(bloques[0])} min')
    iobj = preparar_siguiente_bloque(expected_start=hora_comienzo[0])
    for i, block_mins in enumerate(bloques):
        print(f'   \033[1;35m"{objetivo}"\033[0m')         
        t_tot_cumu += run_bloque_unico(iobj, block_mins, Testing=Testing)
        
        if i < (len(bloques) - 1):
            hi=hora_comienzo[i+1]
            hf=hora_fin[i+1]
            print(u.get_msg('block'),f'{i+1} ({hi.strftime("%H:%M")} -',
                  f'{hf.strftime("%H:%M")}): {math.ceil(block_mins)} min')
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
    str_mins = input(u.get_msg('ask_duration'))
    firstmins = get_mins(str_mins)
    
    threshold = mins_work #+ mins_rest
    es_bloque = firstmins <= threshold
    if Testing:
        print(f'Hay {firstmins} min disponibles')
        print(f'Tiempo mínimo para sesión = {threshold} min')
        print(f'¿Es un bloque de trabajo? {es_bloque}')
        
    totalt = 0.; obj = "test"
    if es_bloque: # Encadenar bloques simples si se desea
        while True and not Testing:
            obj = input(u.get_msg('objetivo_bloque'))
            totalt += run_bloque_unico(obj, firstmins, Testing=Testing)
            
            continuoq = input(u.get_msg('continue_q'))
            continuo = u.get_sn(continuoq)
            if continuo == 'n':
                break
    else:
        tipo = get_session_type()
        totalt, obj = run_sesion_completa(tipo,str_mins,
                                          minblock0=mins_b_0,
                                          minblockn=mins_b_n,
                                          twork=mins_work,
                                          Testing=Testing)

    # Resumen
    print_summary(totalt, obj, es_bloque,Testing=Testing)
    print('      ✨✨✨ \n')        

if __name__ == "__main__":
    sesion()
