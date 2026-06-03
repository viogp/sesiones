from datetime import datetime, timedelta
import math

#end_given = 0; time_input = "08:30"; timezone = "es"  # Comienzo jornada
end_given = 1; time_input = "18:00"; timezone = "es"  # Final jornada
#end_given = 2; time_input = "18:15"; timezone = "es"  # Con actividad

#--------------------------------------
work_h = 8; work_min = 00  # Objetivo

prep_h = 1; prep_min = 30  # Prep mañanas
comida_h = 1
commute1_min = 45 # Llegar a actividad
commute2_min = 30 # De actividad a casa
activity_min = 75 # Duración actividad extraescolar
cena_h = 2; cena_min = 30 # Cena, recoger y prep
noct_min = 0.  # Prep noche

paseo_min = 0
paseo_t = datetime.strptime("00:00", "%H:%M")

# Earliest I want to go to bed
sleep_early = datetime.strptime("22:00", "%H:%M")

# Prep mañanas, horas de comidas y lo más tarde para cenar
if (timezone == "uk"):
    comida_t = datetime.strptime("12:30", "%H:%M")
    cena_last = datetime.strptime("20:00", "%H:%M")
    # paseo_min = 20
    # paseo_t = datetime.strptime("08:35", "%H:%M")
    prep_min = 0
elif (timezone == "es"):
    comida_t = datetime.strptime("13:30", "%H:%M")
    cena_last = datetime.strptime("21:00", "%H:%M")
    
#--------------------------------------
def display_t(tt, transform=None):
    if (transform == 'uk'):
        tt = tt - timedelta(hours=1)
    elif (transform == 'es'):
        tt = tt + timedelta(hours=1)
    return tt.strftime("%H:%M %p")

def display_delta(h1, m1):
    hh = int(h1)
    mm = int(m1)

    # Handle case where minutes exceed 60
    if mm >= 60:
        additional_hours = mm // 60  # Integer division
        mm = mm % 60  # Remainder gives us the minutes
        hh += additional_hours

    if (mm < 1):
        strd = str(hh) + 'h'
    elif (hh < 1):
        strd = str(mm) + 'min'
    else:
        strd = str(hh) + 'h' + str(mm) + 'min'
    return strd


def get_h_min(td):
    return td.seconds//3600., (td.seconds//60.) % 60


def t1_lessthan_t2(time1, time2):
    """
    Compare two time objects, correctly handling midnight crossing.
    Returns True if time1 is earlier than time2, considering midnight crossing.
    """
    # Convert times to minutes since midnight for easier comparison
    minutes1 = time1.hour * 60 + time1.minute
    minutes2 = time2.hour * 60 + time2.minute

    # If the times are far apart (more than 12 hours), we assume there's a midnight crossing
    if abs(minutes1 - minutes2) > 720:
        # If time1 is in early hours (00:00 - 12:00) and time2 is late (12:00 - 23:59)
        # then time1 is actually later (next day)
        if minutes1 < minutes2:
            return False
        else:
            return True
    else:
        # Normal comparison for times within the same day
        return minutes1 < minutes2

# Input time to string
tt = datetime.strptime(time_input, "%H:%M")

# Sleep recommendation (full 1h30min cycles and 14min to fall asleep) + read
stime = 5 * 1.5 + 0.5
mm, hh = math.modf(stime)
sleep_h = int(hh)
sleep_min = int(mm * 60.)

# Initialize variables
start_t = None
end_t = None
activity_t = None

# Start or end times given
if (end_given == 1):  # Final de la jornada dado
    end_t = tt
    mm = work_min
    if (timezone == "uk"):
        mm = work_min + paseo_min
    start_t = end_t - timedelta(hours=work_h + comida_h, minutes=mm)

    wake_up_t = start_t - timedelta(hours=prep_h, minutes=prep_min)
    in_bed_t = wake_up_t - timedelta(hours=sleep_h, minutes=sleep_min)

elif (end_given == 0):  # Comienzo de jornada dado
    start_t = tt
    mm = work_min

    if (paseo_min > 0):
        if (start_t == paseo_t):
            paseo_min = 0
        else:
            mm = work_min + paseo_min
    end_t = start_t + timedelta(hours=work_h + comida_h, minutes=mm)

    wake_up_t = start_t - timedelta(hours=prep_h, minutes=prep_min)
    in_bed_t = wake_up_t - timedelta(hours=sleep_h, minutes=sleep_min)

elif (end_given == 2):  # Activity time given
    activity_t = tt
    
    # Calculate when work ends (activity time minus commute)
    end_t = activity_t - timedelta(minutes=commute1_min)

    # Calculate when work starts
    mm = work_min
    if (timezone == "uk"):
        mm = work_min + paseo_min
    start_t = end_t - timedelta(hours=work_h + comida_h, minutes=mm)

    # Calculate when to wake up and go to bed
    wake_up_t = start_t - timedelta(hours=prep_h, minutes=prep_min)
    in_bed_t = wake_up_t - timedelta(hours=sleep_h, minutes=sleep_min)

# Adjust timetable if I need to go to bed too early
if t1_lessthan_t2(in_bed_t.time(), sleep_early.time()):
    in_bed_t = sleep_early
    wake_up_t = in_bed_t + timedelta(hours=sleep_h, minutes=sleep_min)
    start_t = wake_up_t + timedelta(hours=prep_h, minutes=prep_min)

    print(display_t(start_t), display_t(paseo_t))
    if (start_t == paseo_t):
        paseo_min = 0

    work = end_t - start_t - timedelta(hours=comida_h, minutes=paseo_min)
    work_h, work_min = get_h_min(work)
    if ((work_h == 7 and work_min < 30) or (work_h < 7)):
        print("\n \033[1;31;40m Con este horario NO cumples los mínimos de trabajo  \033[0;37;40m \n")

noct_t = in_bed_t - timedelta(minutes=noct_min)

# Trabajo diario
hh = work_h * 5.
mm = work_min * 5.
if (mm > 60.):
    m1, h1 = math.modf(mm / 60.)
    mm = int(m1 * 60.)
    hh = int(hh + h1)
print(f"\033[1;34;40m Plan para trabajar {display_delta(work_h, work_min)}/día, {display_delta(hh, mm)}/semana ({timezone}):\033[0;37;40m \n")

# Hora de levantarse
print(f"* {display_t(wake_up_t)} arriba. \n")

# Trabajo hasta la hora de comer
if (paseo_min > 0):
    dt = paseo_t - start_t
    hh, mm = get_h_min(dt)
    print(f"\033[1;32;40m* {display_t(start_t)} comienzo trabajando {display_delta(hh, mm)}.\033[0;37;40m \n")
    print(f"* {display_t(paseo_t)} paseo ({paseo_min}min). \n")
    start_t = start_t + timedelta(minutes=paseo_min)

hh, mm = get_h_min(comida_t - start_t)
if timezone == 'uk':
    print(f"\033[1;32;40m* {display_t(start_t)} ({display_t(start_t, 'es')} ES) trabajo {display_delta(hh, mm)} hasta la hora de comer.\033[0;37;40m \n")
else:
    print(f"\033[1;32;40m* {display_t(start_t)} trabajo {display_delta(hh, mm)} hasta la hora de comer.\033[0;37;40m \n")

# Comida
if timezone == 'uk':
    print(f"* {display_t(comida_t)} ({display_t(start_t, 'es')} ES) hora de comer. \n")
else:
    print(f"* {display_t(comida_t)} hora de comer. \n")

# Fin jornada laboral
hh, mm = get_h_min(end_t - comida_t - timedelta(hours=comida_h))
if timezone == 'uk':
    print(f"\033[1;32;40m* {display_t(end_t)}  ({display_t(end_t, 'es')} ES) termino la jornada laboral ({display_delta(hh, mm)} desde la comida).\033[0;37;40m \n")
else:
    print(f"\033[1;32;40m* {display_t(end_t)} termino la jornada laboral ({display_delta(hh, mm)} desde la comida).\033[0;37;40m \n")

if end_given == 2:  # Actividad dada
    dej_h = 0.
    dej_min = activity_min 
    cena_t = activity_t + timedelta(minutes=dej_min+commute2_min)
else:
    activity_t = end_t
    if timezone=="uk":
        activity_min = 120.
    elif timezone=="es":
        activity_min = 150.
        
    cena_t = end_t + timedelta(minutes=activity_min)    
    if t1_lessthan_t2(cena_last, cena_t):
        cena_t = cena_last
    dej_h,dej_min = get_h_min(cena_t - end_t)
    
if(dej_h*60.+dej_min > 30.):
    print(f"* {display_t(activity_t)} me muevo (~{display_delta(dej_h, dej_min)}). \n")

# Dinner
print(f"* {display_t(cena_t)} ceno, recojo y prep. (~{display_delta(cena_h, cena_min)}). \n")

ocio_t = cena_t + timedelta(hours=cena_h, minutes=cena_min)
ocio_h, ocio_min = get_h_min(noct_t - ocio_t)
print(f"* {display_t(ocio_t)} ocio creativo (~{display_delta(ocio_h, ocio_min)}). \n")

# A la cama
print(f"* {display_t(noct_t)} en la cama y a dormir (~{display_delta(sleep_h, sleep_min)}). \n")
