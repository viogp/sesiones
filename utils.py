import time
from config import lang

bloqueo = ('Estar bloqueada es más duro y difícil que ir haciendo. \n')
docencia = ('La docencia es una oportunidad para clarificar tus ideas y ampliar tu legado. \n')

MESSAGES = {
    'es': {
        'prepare_session': "📝 Prepara tu SESIÓN de TRABAJO 📝",
        'ask_duration': "⏰ ¿Durante cuántos minutos (MM) o\n       hasta qué hora (HH:MM) quieres trabajar? ",
        'input_duration': "\n   Escribe durante cuántos minutos (MM) o\n hasta qué hora (HH:MM) quieres trabajar: ",
        'focus_msg': '\n   🕐 Hasta \033[1m{tfin}\033[0m, céntrate en \n     \033[1;32m"{obj}"\033[0m \n',
        'rest_msg': '\n   🤸 Descansa {mins}min,\033[1m hasta {tfin}\033[0m',
        'session_type': '\n  Tipo de SESIÓN DE TRABAJO:',
        'type_1': "  1) Mis proyectos  🔭",
        'type_2': "  2) Docencia 📚",
        'type_3': "  3) Otros (administración, etc) ⚙️",
        'choose_type': '   Elige una opción (1/2/3): ',
        'invalid_type': '   Escribe 1, 2 o 3: ',
        'ask_objective': '\n🌱 ¿Qué objetivo tienes para esta sesión de trabajo? ',
        'next_step': '   📋 Objetivo para este bloque de trabajo y primer paso: ',
        'late_start': '\n   ⚠️  Comienzas esta sesión ({delay:.1f} min tarde)\n',
        'goal_done': '      ✅ ¡Bien hecho!',
        'improve_next': '    - ¿Qué puedes mejorar para la siguiente vez?',
        'time_left': '\r     ⏳ Quedan menos de {mins} min',
        'structure': '\n   🗂️  Estructura de la sesión de trabajo:',
        'block_info': '     - Bloque {i} ({hi} - {hf}): {mins} min',
        'summary_hours': '🎉 Has trabajado {h} horas y {m} min en ',
        'summary_hour': '🎉 Has trabajado {h} hora y {m} min en ',
        'summary_min': '🎉 Has trabajado {m} min en ',
        'enjoy_q': '    - ¿Con qué te lo has pasado bien? ',
        'improve_q': '    - ¿Qué podrías mejorar para la próxima vez? ',
        'continue_q': '  - ¿Quieres continuar con otro bloque (s/n)? ',
        'bad_input': 'No te he entendido, escribe s o n: ',
        'debug_block': 'DEBUG (block_length):',
        'debug_total': '  total_mins={total_mins:.1f}, initial rest={rest}',
        'debug_block0': '  block0={block0}, remaining_mins={remaining_mins:.1f}',
        'debug_adjust': 'DEBUG (nuevas_horas): Bloques ajustados \n',
        'debug_times': 'DEBUG (nuevas_horas): Horas de comienzo y fin ajustadas \n',
        'stop_debug': 'STOP: need debugging nuevas_horas',
        'added_block': 'Bloque añadido ({len}):\n',
        'added_break': 'Descanso añadido ({len}): ',
        'excess_msg': 'el último bloque tiene un exceso de {excess:.1f}',
        'delay_msg': '\n   ⚠️  RETRASO ACUMULADO: sigue trabajando\n',
        'test_obj': "test"
    },
    'en': {
        'prepare_session': "📝 Prepare your WORK SESSION 📝",
        'ask_duration': "⏰ For how many minutes (MM) or\n       until what time (HH:MM) do you want to work? ",
        'input_duration': "\n   Write for how many minutes (MM) or\n until what time (HH:MM) you want to work: ",
        'focus_msg': '\n   🕐 Until \033[1m{tfin}\033[0m, focus on \n     \033[1;32m"{obj}"\033[0m \n',
        'rest_msg': '\n   🤸 Rest for {mins}min,\033[1m until {tfin}\033[0m',
        'session_type': '\n  Type of WORK SESSION:',
        'type_1': "  1) My projects  🔭",
        'type_2': "  2) Teaching 📚",
        'type_3': "  3) Others (admin, etc) ⚙️",
        'choose_type': '   Choose an option (1/2/3): ',
        'invalid_type': '   Write 1, 2 or 3: ',
        'ask_objective': '\n🌱 What objective do you have for this work session? ',
        'next_step': '   📋 Objective for this work block and first step: ',
        'late_start': '\n   ⚠️  You are starting this session ({delay:.1f} min late)\n',
        'goal_done': '      ✅ Well done!',
        'improve_next': '    - What can you improve for next time?',
        'time_left': '\r     ⏳ Less than {mins} min left',
        'structure': '\n   🗂️  Work session structure:',
        'block_info': '     - Block {i} ({hi} - {hf}): {mins} min',
        'summary_hours': '🎉 You have worked {h} hours and {m} min on ',
        'summary_hour': '🎉 You have worked {h} hour and {m} min on ',
        'summary_min': '🎉 You have worked {m} min on ',
        'enjoy_q': '    - What did you enjoy about it? ',
        'improve_q': '    - What could you improve for next time? ',
        'continue_q': '  - Do you want to continue with another block (y/n)? ',
        'bad_input': 'I didn\'t understand, write y or n: ',
        'debug_block': 'DEBUG (block_length):',
        'debug_total': '  total_mins={total_mins:.1f}, initial rest={rest}',
        'debug_block0': '  block0={block0}, remaining_mins={remaining_mins:.1f}',
        'debug_adjust': 'DEBUG (nuevas_horas): Blocks adjusted \n',
        'debug_times': 'DEBUG (nuevas_horas): Start and end times adjusted \n',
        'stop_debug': 'STOP: need debugging nuevas_horas',
        'added_block': 'Block added ({len}):\n',
        'added_break': 'Break added ({len}): ',
        'excess_msg': 'the last block has an excess of {excess:.1f}',
        'delay_msg': '\n   ⚠️  ACCUMULATED DELAY: keep working\n',
        'test_obj': "test"
    }
}

def get_msg(key, **kwargs):
    """
    Obtiene el mensaje en el idioma configurado y formatea los argumentos.
    Si el idioma no está definido, devuelve el español por defecto.
    """
    current_lang = lang if lang in MESSAGES else 'es'
    message = MESSAGES[current_lang].get(key, MESSAGES['es'].get(key, f"MISSING_KEY: {key}"))
    return message.format(**kwargs)


def get_verify_prompt():
    """Retorna la pregunta de verificación específica según el idioma"""
    if lang == 'en':
        return MESSAGES['en']['verify_obj_en']
    return MESSAGES['es']['verify_obj_es']


def good_answer(answer, options=['s','n']):
    isgood = False
    while not isgood:
        if answer in options:
            isgood = True
        else:
            print(get_msg('bad_input'))
            answer = input('')
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




