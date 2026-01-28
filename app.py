import jwt
from datetime import datetime, timedelta
from flask import Flask, render_template, request, session, redirect, url_for, make_response


app = Flask(__name__)
app.secret_key = 'mi_clave_secreta_super_segura' 

JWT_SECRET = 'clave_jwt_super_segura' 
JWT_ALGORITHM = 'HS256' 
CLAVE_CORRECTA = 'GosaCalidad'  


@app.route('/inicio')
def inicio():
    if not verificar_jwt():
        return redirect(url_for('root'))
    return render_template('Index.html')

@app.route('/menufs')
def menufs():
    return render_template('MenuFs.html')

@app.route('/fase1')
def fase1():
    return render_template('MenuF1.html')

@app.route('/resultadofase1')
def resultadofase1():
    return render_template('ResultadoF1.html')

@app.route('/fase2')
def fase2():
    return render_template('MenuF2.html')

@app.route('/resultadofase2')
def resultadofase2():
    return render_template('ResultadoF2.html')

@app.route('/fase3')
def fase3():
    return render_template('MenuF3.html')

@  app.route('/resultadofase3')
def resultadofase3():
    return render_template('ResultadoF3.html')

@app.route('/fase4')
def fase4():
    return render_template('MenuF4.html')

@app.route('/resultadofase4')
def resultadofase4():   
    return render_template('ResultadoF4.html')

@app.route('/fase5')
def fase5():
    return render_template('MenuF5.html')

@app.route('/resultadofase5')
def resultadofase5():
    return render_template('ResultadoF5.html')  



# ======== FUNCIONES DE APOYO ========

def calcular_puntaje(respuestas):
    total = sum(respuestas)
    maximo = len(respuestas) * 10
    return round((total / maximo) * 100, 2)


def mensaje_fase1(valor):
    if valor == 100:
        return "¡Excelente trabajo! Has eliminado lo innecesario y tu espacio está optimizado. Nada sobra, todo tiene un propósito. ¡Gran paso hacia la eficiencia!"
    elif valor >= 80:
        return "Casi listo. Has identificado lo esencial, pero todavía hay elementos que podrían ser eliminados o reorganizados."
    elif valor >= 60:
        return "Buen progreso. Has hecho avances, pero aún quedan cosas innecesarias afectando el flujo de trabajo."
    elif valor >= 40:
        return "Necesitas revisar qué objetos no agregan valor. Hay muchas cosas ocupando espacio sin utilidad."
    elif valor >= 20:
        return "Todavía hay un desorden considerable. Evalúa qué realmente necesitas y elimina lo que solo ocupa espacio."
    else:
        return "No se han eliminado elementos innecesarios. Esto puede generar desorden y afectar la productividad."

def mensaje_fase2(valor):
    if valor == 100:
        return "Todo está en su lugar correcto y fácilmente accesible. Tu espacio es eficiente y ordenado."
    elif valor >= 80:
        return "Muy buen trabajo. Solo algunos elementos necesitan mejor ubicación para mayor accesibilidad."
    elif valor >= 60:
        return "Has avanzado en la organización, pero aún hay herramientas y documentos sin una ubicación fija."
    elif valor >= 40:
        return "Falta estructurar mejor el orden. Define lugares específicos y etiquétalos para mayor eficiencia."
    elif valor >= 20:
        return "No hay un sistema claro de organización. Esto puede generar pérdida de tiempo buscando elementos."
    else:
        return "El espacio sigue desorganizado. Esto dificulta el trabajo y aumenta el tiempo de búsqueda."

def mensaje_fase3(valor):
    if valor == 100:
        return "¡Impecable! Tu espacio está limpio y libre de residuos. La prevención es parte de la rutina."
    elif valor >= 80:
        return "Muy buena limpieza. Solo algunos detalles necesitan mayor atención para mantenerlo perfecto."
    elif valor >= 60:
        return "Se nota esfuerzo en la limpieza, pero algunas áreas aún presentan suciedad o descuido."
    elif valor >= 40:
        return "La limpieza no es constante. Necesitas implementar hábitos de mantenimiento más frecuentes."
    elif valor >= 20:
        return "El espacio tiene acumulación de suciedad. Establece una rutina clara de limpieza para mejorar el entorno."
    else:
        return "No se ha aplicado limpieza en el área de trabajo. Esto puede afectar la seguridad y productividad."

def mensaje_fase4(valor):
    if valor == 100:
        return "¡Gran trabajo! Has estandarizado procesos y todo el equipo sigue las mismas reglas de organización."
    elif valor >= 80:
        return "Casi perfecto. Hay algunas prácticas que pueden afinarse para garantizar la estandarización total."
    elif valor >= 60:
        return "Has avanzado en la estandarización, pero todavía hay variaciones en los procesos."
    elif valor >= 40:
        return "Falta mayor compromiso en seguir los estándares establecidos. Se requiere más capacitación."
    elif valor >= 20:
        return "Las reglas no están claras ni aplicadas de manera uniforme. Esto afecta la consistencia en el trabajo."
    else:
        return "No hay normas claras o estandarización. Sin esto, los resultados pueden ser inconsistentes."

def mensaje_fase5(valor):
    if valor == 100:
        return "¡Felicidades! La metodología 5S ya forma parte de tu cultura de trabajo y se mantiene con compromiso."
    elif valor >= 80:
        return "Muy buen trabajo. Has desarrollado disciplina, pero aún se requiere constancia."
    elif valor >= 60:
        return "Vas por buen camino, aunque algunas reglas aún no se siguen de manera automática."
    elif valor >= 40:
        return "Necesitas reforzar hábitos para que el cumplimiento de 5S sea natural y constante."
    elif valor >= 20:
        return "La disciplina es baja, lo que dificulta mantener el orden y limpieza. Necesitas mayor compromiso."
    else:
        return "No hay seguimiento de la metodología. Sin disciplina, los esfuerzos previos pueden perderse."

# ======== EVALUACIÓN DE FASE 1 ========
@app.route('/resultadofase1', methods=['POST'])
def evaluar1():
    r1 = int(request.form['diagnostico'])
    r2 = int(request.form['identificacion'])
    r3 = int(request.form['eliminacion'])

    total = calcular_puntaje([r1, r2, r3])
    session['fase1_resultado'] = total
    mensaje = mensaje_fase1(total)
    return render_template('ResultadoF1.html', total=total, mensaje=mensaje)

# ======== EVALUACIÓN DE FASE 2 ========
@app.route('/resultadofase2', methods=['POST'])
def evaluar2():
    r = [
        int(request.form['ubicacion_estrategica']),
        int(request.form['accesibilidad']),
        int(request.form['sistema_visual']),
        int(request.form['almacenamiento_inteligente'])
    ]
    total = calcular_puntaje(r)
    session['fase2_resultado'] = total
    mensaje = mensaje_fase2(total)
    return render_template('ResultadoF2.html', total=total, mensaje=mensaje)

# ======== EVALUACIÓN DE FASE 3 ========
@app.route('/resultadofase3', methods=['POST'])
def evaluar3():
    r = [
        int(request.form['limpieza_rutinaria']),
        int(request.form['inspeccion_rapida']),
        int(request.form['limpieza_finalizar']),
        int(request.form['responsabilidad_compartida'])
    ]
    total = calcular_puntaje(r)
    session['fase3_resultado'] = total
    mensaje = mensaje_fase3(total)
    return render_template('ResultadoF3.html', total=total, mensaje=mensaje)

# ======== EVALUACIÓN DE FASE 4 ========
@app.route('/resultadofase4', methods=['POST'])
def evaluar4():
    r = [
        int(request.form['registro_detallado']),
        int(request.form['checklist']),
        int(request.form['formatos_calidad']),
        int(request.form['capacitacion'])
    ]
    total = calcular_puntaje(r)
    session['fase4_resultado'] = total
    mensaje = mensaje_fase4(total)
    return render_template('ResultadoF4.html', total=total, mensaje=mensaje)

# ======== EVALUACIÓN DE FASE 5 ========
@app.route('/resultadofase5', methods=['POST'])
def evaluar5():
    r = [
        int(request.form['reunion_jefes']),
        int(request.form['sistema_incentivos']),
        int(request.form['auditorias_mensuales'])
    ]
    total = calcular_puntaje(r)
    session['fase5_resultado'] = total
    mensaje = mensaje_fase5(total)
    return render_template('ResultadoF5.html', total=total, mensaje=mensaje)

# ======== RESULTADO FINAL 5S ========
@app.route('/resultado_general')
def resultado_general():
    f1 = session.get('fase1_resultado', 0)
    f2 = session.get('fase2_resultado', 0)
    f3 = session.get('fase3_resultado', 0)
    f4 = session.get('fase4_resultado', 0)
    f5 = session.get('fase5_resultado', 0)

    promedio = round((f1 + f2 + f3 + f4 + f5) / 5, 2)

    if promedio == 100:
        mensaje = (
            "¡Felicidades! Has alcanzado la implementación total de las 5S. "
            "Tu espacio de trabajo es un ejemplo de eficiencia, orden y disciplina. "
            "Mantén este estándar y ayuda a otros a mejorar su entorno con buenas prácticas. "
            "La mejora continua es el camino."
        )
    elif promedio >= 81:
        mensaje = (
            "¡Estás muy cerca de la excelencia! Tu compromiso con las 5S se nota en la organización, "
            "estandarización y disciplina del trabajo. Revisa los pequeños detalles pendientes y ajusta "
            "lo necesario para alcanzar un nivel impecable. Sigue así."
        )
    elif promedio >= 61:
        mensaje = (
            "¡Gran progreso! Tu espacio de trabajo refleja una buena aplicación de las 5S, lo que mejora la productividad y el orden. "
            "Solo algunos detalles requieren optimización para alcanzar la excelencia. Mantén la constancia y refuerza los hábitos adquiridos."
        )
    elif promedio >= 41:
        mensaje = (
            "Vas por buen camino. Se han implementado varias prácticas de las 5S, pero aún hay áreas que requieren ajustes y mayor compromiso. "
            "Identifica los puntos débiles y sigue fortaleciendo cada etapa para conseguir un entorno más eficiente y estructurado."
        )
    elif promedio >= 21:
        mensaje = (
            "Has comenzado el camino hacia la mejora, pero aún queda mucho por hacer. Algunas prácticas de las 5S se han adoptado, "
            "pero la falta de constancia impide resultados óptimos. Enfócate en aplicar los principios con disciplina para lograr un impacto visible en la organización."
        )
    else:
        mensaje = (
            "Aún queda mucho por mejorar. La metodología 5S no se ha implementado completamente, lo que puede afectar la organización y productividad. "
            "Es momento de dar el primer paso y comenzar a transformar tu entorno de trabajo con pequeñas acciones. Cada esfuerzo cuenta."
        )

    return render_template('ResultadoFinal.html', promedio=promedio, mensaje=mensaje)

# ======== AUTENTICACIÓN JWT ========

@app.route('/', methods=['GET', 'POST'])
def root():
    if not verificar_jwt():
        error = None
        if request.method == 'POST':
            clave = request.form.get('clave')
            if clave == CLAVE_CORRECTA:
                token = jwt.encode(
                    {
                        'usuario': 'autenticado',
                        'exp': datetime.utcnow() + timedelta(seconds=1)
                    },
                    JWT_SECRET,
                    algorithm=JWT_ALGORITHM
                )
                resp = make_response(redirect(url_for('inicio')))
                resp.set_cookie('token', token)
                return resp
            else:
                error = "Clave incorrecta"
        return render_template('Clave.html', error=error)
    else:
        return redirect(url_for('inicio'))


def verificar_jwt():
    token = request.cookies.get('token')
    if not token:
        return False
    try:
        jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

# ======== EJECUTAR FLASK ========
if __name__ == '__main__':
    app.run(debug=True)