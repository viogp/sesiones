import os
import matplotlib.pyplot as plt
import time
from config import *
import utils as u

tt = min_refl
t2 = tt*2.
t_half = tt/2.

rem = [' - Muéveta a diario: (~6000 pasos + 20min de ej.) o ~10000 pasos. \n',
       ' - Por las noches, haz más actividades sin pantallas, como dibujar. \n',
       ' - Rutina de sueño: 7:00 arriba y 23:00 en la cama. \n',
       ' - Da un paseo de unos 15min después de comer y cenar.\n',
       ' - No mires pantallas en la cama. \n',
       ' - Designa tiempos para leer mensajes potencialmente peligrosos. \n',
       ' - Haz yoga de forma regular. \n',
       ' - Genera unos planes semanales y diarios bien desmigajados. \n',
       ' - Cada semana, dedica tiempo a tu proyecto. \n',
       ' - Conéctate con tus por qué al escribirlos a diario. \n',
       ' - Ten ratos de ocio en los que no haces nada. \n',
       ' - Juega más, también con tus proyectos y actividades diarias. \n']

paliativo = ('  Toma distancia de tus pensamientos:\n'
             '  - Vete a un sitio tranquilo y haz 5 respiraciones lentas.\n'
             '  - Canción y a bailar.\n'
             '  - Escribe unos 10min sobre el tema.\n'
             '  - Sal fuera y da un paseo de unos 15min.\n')

trocea = (' 1) Decide cuál es el siguiente paso diminuto y \n'
          '    escríbelo de forma clara y precisa. \n'
          ' 2) Completa ese paso. \n'
          ' 3) Repite. \n')

lanza_vamos = '\nAhora, EMPIEZA, si quieres, ayúdate con vamos.py \n'


def get_response(message, frase):
    print('\n')
    print('* Es mejor prevenir que curar, así que:\n')
    if frase == 1:
        print(rem[7], rem[8], rem[11])
    elif frase == 2:
        print(rem[7], rem[9], rem[11])
    elif frase == 3:
        print(rem[2], rem[0], rem[1])
    elif frase == 4:
        print(rem[5], rem[3], rem[6], rem[10])
    elif frase == 5:
        print(rem[2], rem[1], rem[4])
    
    print(' * RECOMENDACIÓN:\n')
    print(message)
    return


def get_type():
    print('  🤝 TIPO DE AYUDA que necesitas 🤝\n')
    print('  1) General')
    print('  2) Comenzar el día (~1 min)')
    print('  3) Revisión semanal (~10 min)')
    print('  4) Revisión trimestral (~40 min)')
    print('  5) Revisión anual (~1 h)')
    print('  6) Transición (~ 10 min)')
    ntipos = 6
    tipo = input('\n   Elige una opción del 1 al '+str(ntipos)+': ')
    itipo = int(tipo)
    while itipo not in range(ntipos+1):
        tipo = input('   No te he entendido, escribe un número: ')
        itipo = int(tipo)
    return tipo


def life_wheel():
    """
    Collects scores for 6 life categories and displays them as a bar chart.
    Each score should be between 0 and 10.
    """
    categories = ["Sobrevivir", "Retos", "Pertenencia", "Cáracter", "Propósito", "Legado"]
    explicacion = ["Casa, salud, finanzas, lo básico.",
                   "Pensar a lo grande, aventuras, desilusiones, etc.",
                   "Relaciones con otras personas y la naturaleza.",
                   "Desarrollo personal, creatividad, aprender, valores.",
                   "Dirección, intención, motivación, ambición, disfrute.",
                   "Tu huella, el impacto invisible en otros, cómo quieres que se te recuerde."]

    if Testing:
        scores =[10,10,10,10,10,10]
    else:
    	scores = []
    	print("  🌈 Puntúa las distintas áreas de tu vida entre 0 y 10:\n")
    	i=0
    	for category in categories:
    	    expl = explicacion[i]
    	    
    	    while True:
    	        try:
    	            value = float(input(f"     {category} ({expl}): "))
    	            if 0 <= value <= 10:
    	                scores.append(value)
    	                break
    	            else:
    	                print("Por favor, introduce un número entre 0 y 10.")
    	        except ValueError:
    	            print("Da un número.")
    	    i += 1
            
    # Create the bar plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD"]
    bars = ax.bar(categories, scores, color=colors, edgecolor="white", linewidth=1.5)
    
    # Add value labels on top of each bar
    for bar, score in zip(bars, scores):
        height = bar.get_height()
        ax.annotate(f"{score:.1f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha="center", va="bottom",
                    fontsize=12, fontweight="bold")
    
    # Customize the plot
    ax.set_ylim(0, 11)
    ax.set_ylabel("Puntuación", fontsize=12)
    ax.set_title("Revisión vital", fontsize=16, fontweight="bold", pad=20)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.grid(True, linestyle="--", alpha=0.7)
    ax.set_axisbelow(True)
    
    # Add a horizontal reference line at midpoint
    ax.axhline(y=5, color="gray", linestyle=":", alpha=0.5, label="Midpoint (5)")
    
    plt.tight_layout()
    plt.show()
    
    return t_half

 
def get_moretime(frase,Testing=False):
    ttot = 0
    pasoq = input('  - ¿Tienes claro cómo dar ahora un pasito hacia lo que te importa (s/n)?\n')
    paso = u.get_sn(pasoq)
    
    if paso == 'n':
        get_response(trocea,frase)
        ttot += u.treflexion(tt,Testing=Testing)
        
        claroq = input('    ¿Lo tienes claro ahora (s/n)? ')
        claro = u.get_sn(claroq)
        if paso == 'n':
            get_response(paliativo, frase)
            exit()
    return ttot


def motivate(tt,Testing=False):
    print('  - Empieza por recordarte qué es lo importante para ti,\n',
          '    ¿qué quieres conseguir a largo plazo?, y\n',
          '    siente la resistencia, ¿como podrías jugar con las tareas?.\n')
    ttot = u.treflexion(t_half,Testing=Testing)
    return ttot


def fin_revision(ttot,Testing=False):
    print(f'  ⏳ Has terminado esta revisión en unos {ttot:.0f} min')
    print(lanza_vamos)
    print('     ✨✨✨ ')
    return


def transicion(Testing=False):
    ttot = 0
    if not Testing:
        start_time = time.time()

    print('\n  - La investigación es profunda y abierta; la docencia es social estructurada y con plazos.\n')
    diq = input('    - ¿Quieres transitar hacia la investigación? (s/n)')
    di = u.get_sn(diq)
    if di == 's':
        print('\n   🔭 Hacia la investigación\n')
        print('\n      ✨✨✨ Mi PGL: ' + mipgl)
        ttot = u.treflexion(s_respir/2,unit='s',Testing=Testing)
        print('\n      Trabaja combinando herramientas:')
        print('        - Ficheros de seguimiento tareas y objetivos en el ordenador.')
        print('          ~/roots/annual_reviews.org (visión global)')
        print('          ~/roots/project.org  (lista completa de tareas del proyecto)')
        print('          ~/roots/papers.ods (seguimiento para artículo)')
        print('        - Cuaderno para las tareas de la sesión de trabajo de hoy.')
        ttot = u.treflexion(s_respir,unit='s',Testing=Testing)
        print('        Celebra los pequeños logros diarios:')
        print('        - Pegatinas al final de una sesión de trabajo.')
        print('        - Si estás bastante dispersa: colorea cuadraditos cada ~15min.')
        ttot = u.treflexion(s_respir/2,unit='s',Testing=Testing)
        print('        Los primeros días, ayúdate con sesiones acompañada:')
        print('        - FocusMate: https://app.focusmate.com/dashboard')
        ttot = u.treflexion(s_respir/2,unit='s',Testing=Testing)
        print('        Sesiones que te han funcionado:')
        print('        - 9:00 a 13:10 (30min+75min+75min+40min) y un rato de correo')
        print('        - 14:30 a 18:00 (30min+75min+75min) y un rato de correo')
        ttot = u.treflexion(s_respir/2,unit='s',Testing=Testing)
    else:
        print('\n   📚 Hacia la docencia ')
        print(u.get_msg('docencia'))
        ttot = u.treflexion(s_respir/2,unit='s',Testing=Testing)
        print('\n      Recaba información sobre las asignaturas:')
        print('        - Ficheros de información en el ordenador:')
        print('          ~/branches/teaching')
        print('        - Cuadernos.')
        ttot = u.treflexion(s_respir,unit='s',Testing=Testing)

    ttot += motivate(tt,Testing=Testing)
    print('  🗓️  Mira en tu calendario cómo se presenta este periodo.')
    print('     Agenda medio día para recuperar tareas pequeñas. \n')
    ttot += u.treflexion(tt,Testing=Testing)
    ttot += sprint(plan=True,Testing=Testing)

    if not Testing:
        ttot = time.time() - start_time
    fin_revision(ttot,Testing=Testing)
    return


def comienzo(tt,Testing=False):
    print('\n  ✨ ¿Cómo se presenta el día?\n')
    ttot = u.treflexion(tt,unit='s',Testing=Testing)
    print('  🐉 ¿Cómo estás?\n')
    ttot = u.treflexion(tt,unit='s',Testing=Testing)
    print('  ☕ ¿Hay algo que te podría ayudar hoy?\n')
    ttot = u.treflexion(tt,unit='s',Testing=Testing)
    print(lanza_vamos)
    return


def refl_past(personal=False,Testing=False):
    print('\n')
    print('  ✨ ¿Cómo ha ido el último periodo?')
    print('     ¿Qué has conseguido? ¡Celébralo!')
    print('     ¿Qué ha fallado? Contesta con compasión\n')
    if not Testing and not personal and info_projects:
        os.system(path2metas)
    ttot = u.treflexion(tt,Testing=Testing)
    return ttot

def prioriza(anual=False,Testing=False):    
    if not anual:
        print('  👀 Mira tu lista de flujo de publicaciones y')
        print('     tus objetivos anuales, y ahora:')
    print('  📚 Prioriza tus proyectos basándote en')
    print('     tiempo, impacto y urgencia\n')
    ttot = u.treflexion(t2,Testing=Testing)
    return ttot


def objetivos(anual=False,Testing=Testing):
    ttot = 0 
    print('  🐉 Define tus objetivos mínimos (<5), si todo va mal, y')
    print('     y tus objetivos ideales.\n')
    ttot += u.treflexion(t2,Testing=Testing)
    if anual:
        print('  🧭 Haz una lista final de proyectos para el próximo curso')
    else:
        print('  🧭 Haz una lista final de proyectos hasta las próximas vacaciones')
    print('     REFINA tus objetivos: concretos, alcanzables, coherentes, tuyos,')
    print('                           con consecuencias positivas a largo plazo')
    print('     CREA sistemas para cumplir tus objetivos')
    ttot += u.treflexion(tt,Testing=Testing)
    return ttot


def sprint(plan=False,Testing=False):
    ttot = 0
    if plan:
        print('  🤔 Reflexiona sobre el último sprint:\n')
        print('     ¿Qué has conseguido?\n')
        print('     ¿Qué ha funcionado?\n')
        print('     ¿Qué puedes mejorar para el siguiente?\n')
        ttot += u.treflexion(t2,Testing=Testing)

        print('  📅 Planea el sprint:\n')
        print('     ¿En qué vas a trabajar y durante qué días?\n')
        print('     ¿Cuál es el objetivo mínimo, si hay problemas?\n')
        print('     ¿Cuál es el objetivo ideal, si todo va bien?\n')
        print('     ¿Qué estrategias vas a seguir para aumentar el foco?\n')
        print('     ¿Cuál es el objetivo de la primera sesión de trabajo?\n')
        ttot += u.treflexion(t2,Testing=Testing)
    else:
        print('  📅 Repasa tu calendario, tus prioridades trimestrales')
        print('     y tus objetivos del sprint actual:\n')
        print('     Decide tiempos y prioridades para la semana que viene\n')
        ttot += u.treflexion(tt,Testing=Testing)
    return ttot


def revision_semanal(Testing=False):
    ttot = 0
    if not Testing:
        start_time = time.time()
        
    ttot += refl_past(Testing=Testing)
    print('  🥰 ¿De qué estás agradecida?\n')
    print('     ¿Qué has aprendido y cómo puedes incorporarlo?\n')
    ttot += u.treflexion(t_half,Testing=Testing)
    planq = input('  📋 ¿Necesitas planear un nuevo sprint (s/n)?')
    print(' ')
    plana = u.get_sn(planq)
    if plana == 's':
        sprint(plan=True,Testing=Testing)
    else:
        sprint(Testing=Testing)

    if not Testing:
        ttot = time.time() - start_time
    fin_revision(ttot,Testing=Testing)
    return ttot


def revision_trimestral_parte(Testing=False):
    ttot = 0
    if not Testing:
        start_time = time.time()

    print('  🗓️  Incluye en tu calendario clases, vacaciones y eventos.')
    print('     Identifica qué días y cuántas horas podrás dedicar a tu proyecto. \n')
    ttot += u.treflexion(t2,Testing=Testing)
    print('  💆 ¿Qué rutinas de descanso vas a seguir?')
    print('     Por ejemplo: rutina de cierre, escribir los siguientes pasos, etc. \n')
    ttot += u.treflexion(t_half,Testing=Testing)
    ttot += sprint(plan=True,Testing=Testing)
    ttot += objetivos(Testing=Testing)

    if not Testing:
        ttot = time.time() - start_time
    return ttot


def revision_trimestral(Testing=False):
    ttot = 0
    if not Testing:
        start_time = time.time()

    ttot += refl_past(Testing=Testing)
    ttot += prioriza(Testing=Testing)
    ttot += revision_trimestral_parte(Testing=Testing)

    if not Testing:
        ttot = time.time() - start_time
    fin_revision(ttot,Testing=Testing)
    return ttot


def revision_anual(Testing=False):
    ttot = 0
    if not Testing:
        start_time = time.time()

    ttot += refl_past(Testing=Testing)
    print('  🔮 Escribe sobre este día dentro de un año.')
    print('     ¿Qué has hecho? ¿Cómo te sientes?')
    ttot += u.treflexion(t2,Testing=Testing)
    print('  🧭 Lee tu "Mission statement",\n')
    print('     ¿resuena contigo?, ¿quieres cambiar algo?\n')
    ttot += u.treflexion(t_half,Testing=Testing)

    print('  🔧 Ejercicio de alinear actividades:')
    print('     1) Haz una lista de actividades dentro de las categorías')
    print('        Investigación, Docencia, y Servicio')
    pasoq = input('- ¿La tienes (s/n)?\n')
    print('     2) Puntúa 3 aspectos de cada actividad')
    print('        Apoya mi misión:1=sí, 2=neutro, 3=no')
    print('        Merece la pena: 1=sí, 2=neutro, 3=no')
    print('        Puedo abandonarla: 1=sí, 2=neutro, 3=no')
    pasoq = input('- ¿Lo tienes (s/n)?\n')
    print('     3) Escribe tu lista de actividades alineadas en')
    if not Testing:
        os.system("libreoffice " + path2papers + " &")
    pasoq = input('- ¿Lo tienes (s/n)?\n')
    print('     4) Decide si quieres dejar alguna actividad no alineada')
    print('        y escríbelas en la hoja de cálculo')
    pasoq = input('- ¿Lo tienes (s/n)?\n')
    print('     5) Escribe la lista de tareas a alinear')
    print('        y reflexiona sobre ellas')
    pasoq = input('- ¿Lo tienes (s/n)?\n')

    print('  🗒️ Mira tu lista de flujo de publicaciones,\n')
    print('     ¿en qué proyectos te gustaría centrarte?,\n')
    print('     ¿hay otros proyectos en los que te gustaría trabajar?\n')
    ttot += u.treflexion(tt,Testing=Testing)
    ttot += prioriza(anual=True,Testing=Testing)
    ttot += objetivos(anual=True,Testing=Testing)
    print('  💻 Agenda el momento para hacer copias de seguridad\n')
    ttot += u.treflexion(t_half,Testing=Testing)
    print('  🏝️ Ahora vas a planear el periodo hasta las próximas vacaciones.\n')
    ttot += revision_trimestral_parte(Testing=Testing)

    if not Testing:
        ttot = time.time() - start_time    
    fin_revision(ttot,Testing=Testing)
    return


def revision_trimestral_personal(Testing=False):
    ttot = 0
    if not Testing:
        start_time = time.time()

    ttot += refl_past(personal=True,Testing=Testing)
    print('  🥰 ¿Qué emociones placenteras e incómodas has experimentado?\n')
    ttot += u.treflexion(t_half,Testing=Testing)
    print('  🐉 ¿Qué te gustaría haber hecho de otra forma?\n')
    ttot += u.treflexion(t_half,Testing=Testing)
    print('  📖 Novela en 1 párrafo est último periodo y ponle un título\n')
    ttot += u.treflexion(tt,Testing=Testing)    
    ttot += life_wheel()
    print('  ✒️ ¿Qué título querrías para el siguiente capítulo?')
    print('     ¿Qué te gustaría experimentar?')
    ttot += u.treflexion(t_half,Testing=Testing)
    print('  📋 Repasa tus prioridades anuales y tu calendario.')
    ttot += objetivos(Testing=Testing)
    print('  🗓️  Agenda el momento para hacer:')
    print('     - Copias de seguridad de tus fotos')
    print('     - Repaso de finanzas')
    ttot += u.treflexion(t_half,Testing=Testing)

    if not Testing:
        ttot = time.time() - start_time    
    fin_revision(ttot,Testing=Testing)
    return ttot


def ayuda_general(Testing=True):
    print("\n   🐉 ¿Cómo estás? \n")
    print("   1. No estoy haciendo lo que me he propuesto. \n")
    print("   2. Estoy agobiada, no me apetece y/o sé que no valgo para esto. \n")
    print("   3. No tengo energía. \n")
    print("   4. Estoy sobrepasada emocionalmente. \n")
    print("   5. Hoy he empezado más tarde de lo previsto. \n")
    
    frase = int(input("Número de la frase que mejor te describe hoy: "))
    print("\n")
    
    if frase == 1:
        motivate(tt,Testing=Testing)
        print(u.get_msg('bloqueo'))
        ttot = u.treflexion(s_respir,unit='s',Testing=Testing)
        print("\n ¿Cómo es la tarea a la que te enfrentas? \n")
        print("   1. Difícil. \n")
        print("   2. No está clara. \n")
        print("   3. Intimidante. \n")
        print("   4. Tediosa. \n")
        print("   5. Otra cosa. \n")
        motivo = int(input("Número de la frase que mejor describe tu tarea: "))
        print("\n")
        
        if motivo == 1:
            print('Crea una pre-tarea más sencilla y/o divertida.\n',
                  'Repite el proceso de encontrar tareas diminutas.\n')
        elif motivo == 2:
            print('Redacta la tarea de forma más precisa.\n',
                  'Si es necesario, divide la tarea en otras más pequeñas.\n')
        elif motivo == 3:
            print('El miedo indica que estás haciendo algo que te importa y que es complicado, aprecialo, ¡te vas a sentir satisfecha!.\n',
                  'Si te paraliza el miedo a ser juzgada: recuerda que estás aquí para crear y disfrutar del proceso.\n')
        elif motivo == 4:
            print('Cambia tu entorno.\n',
                  'Ponte música, cambia de mesa, enciende una vela, vete a la biblioteca, etc.\n')
        elif motivo == 5:
            print('¿Por qué no estás haciendo lo que te habías propuesto?.\n',
                  'Hazte esta pregunta 3 veces o 5.\n')
        
        print(lanza_vamos)
    
    elif frase == 2:
        print('Gracias mente por esta vocecilla impostora que me cuida al intentar que no malgaste energía.\n',
              'Tu voz es única y es importante.\n')
        motivate(tt,Testing=Testing)
        print(lanza_vamos)
    
    elif frase == 3:
        tarde1 = input("¿Es por la mañana o justo después de comer (s/n)?")
        tarde = u.get_sn(tarde1)
        if tarde == 's':
            message = ('Tómate un café. \n')
            get_response(message, frase)
        else:
            descanso1 = input("¿Puedes descansar al menos 5min (s/n)?")
            descanso = u.get_sn(descanso1)
            if descanso == 's':
                message = ('Tómate un descanso activo de al menos 5min:\n'
                           'Camina, baila, muévete. \n')
                get_response(message, frase)
            else:
                reunion1 = input("¿Tienes una reunión pronto (s/n)?")
                reunion = u.get_sn(reunion1)
                if reunion == 's':
                    message = ('Si puedes, atiende la reunión o\n'
                               'de pie o\n'
                               'moviéndote. \n')
                    get_response(message, frase)
                else:
                    message = ('Lávate la cara. \n')
                    get_response(message, frase)
    
    elif frase == 4:
        tarde1 = input("¿Puedes designar un tiempo más tarde para analizar lo que te preocupa (s/n)?")
        tarde = u.get_sn(tarde1)
        if tarde == 's':
            message = ('Agenda cuándo vas a darle vueltas al asunto. \n')
            get_response(message, frase)
        else:
            get_response(paliativo, frase)
    
    elif frase == 5:
        tarde1 = input("¿Más tarde de 1h (s/n)?")
        tarde = u.get_sn(tarde1)
        if tarde == 's':
            message = ('Dedica unos 15min a planear cómo recuperar el tiempo '
                       'durante los próximos 5 días de trabajo. \n'
                       'Piensa en reducir el descanso del mediodía '
                       'y alargar los días 30min. \n')
            get_response(message, frase)
        else:
            fregar1 = input("¿Te basta con reducir el descanso de la comida para recuperar? (s/n)")
            fregar = u.get_sn(fregar1)
            if fregar == 's':
                message = ('Recupera dejando de recoger o reduciendo '
                           'de otro modo el descanso de la comida. \n')
                get_response(message, frase)
            else:
                dia1 = input('¿Podrías recuperar el tiempo al final del día? (s/n)')
                dia = u.get_sn(dia1)
                if dia == 's':
                    message = ('Recupera quedándote un rato más hoy.\n' +
                               'Decide hasta cuándo y escríbelo. \n')
                    get_response(message, frase)
                else:
                    message = ('Agenda cuándo vas a recuperar el tiempo. \n')
                    get_response(message, frase)
    
    else:
        print('Vaya, no tengo ideas concretas...¿quizás un paseo?')
    return


def ritual_ayuda(tipo, Testing=False):
    if tipo == '1':
        ayuda_general(Testing=Testing)
    elif tipo == '2':
        comienzo(s_respir,Testing=Testing)
    elif tipo == '3':
        revision_semanal(Testing=Testing)
    elif tipo == '4':
        personalq = input('    - ¿Quieres hacer una revisión personal? (s/n)')
        personal = u.get_sn(personalq)
        if personal == 's':
            revision_trimestral_personal(Testing=Testing)
        else:
            revision_trimestral(Testing=Testing)
    elif tipo == '5':
        revision_anual(Testing=Testing)        
    else:
        transicion(Testing=Testing)
    return


def animo():
    import random
    animosas = ['Venga, ¡a por todas! \n',
                'Vamos, ¡tú puedes! \n',
                'Esto te importa un montón, ¡ponte con ello!\n',
                'Te sientes mejor cuando haces lo que te habías propuesto.\n']
    print(random.choice(animosas))
    print("     ✨✨✨    \n")
    
# ------------------------------
def rere():
    print("¡Hola caracola! \n")
    print("Respira una vez lentamente.\n")
    ttot = u.treflexion(s_respir,unit='s',Testing=Testing)
    tipo = get_type()
    ritual_ayuda(tipo, Testing=Testing)
    animo()

    
if __name__ == "__main__":
    rere()

