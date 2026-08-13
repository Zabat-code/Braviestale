########################################################
# ARCO DE MIRA — "LO QUE SE GUARDA POR MIEDO A PESAR"
# ------------------------------------------------------
# Dinámica: sin ruptura dramática. Mira carga un miedo que
# no ha compartido con nadie — sentir que no es lo bastante
# útil comparada con Doran (fuerza) o el propio protagonista
# (liderazgo de facto del grupo). Ese miedo se profundiza si
# ELLA fue quien cayó del puente (ver 06_troll_puente.rpy):
# sobrevivir sola, sin poder ayudar a nadie, confirma sus
# peores temores sobre sí misma.
#
# El arco avanza por APERTURA gradual, no por conflicto: cada
# visita profundiza un poco más lo que Mira está dispuesta a
# compartir, hasta la revelación completa del miedo, y luego
# un momento donde el protagonista puede reafirmar su valor
# de una forma que ella recuerde.
########################################################

# Estados:
#   "cotidiana"   -> conversaciones normales, sin profundidad
#   "insinuando"  -> deja entrever que algo la inquieta
#   "abierta"     -> comparte el miedo de fondo directamente
#   "afirmada"    -> el protagonista responde de forma que la marca
default estado_arco_mira = "cotidiana"
default mira_visitas_cotidiana = 0

init python:

    def resumen_diario_mira():
        if estado_arco_mira == "cotidiana":
            if mira_visitas_cotidiana == 0:
                return "Mira está bien, o eso parece. Nada fuera de lo normal, aunque a veces se queda pensativa más de la cuenta."
            else:
                return "Sigo notando algo en Mira que no termina de encajar — como si hubiera algo que no dice. No quiero presionarla."
        elif estado_arco_mira == "insinuando":
            return "Mira dejó entrever que algo la preocupa de verdad. No llegó a decir qué. Tal vez la próxima vez."
        elif estado_arco_mira == "abierta":
            return "Mira por fin me dijo lo que la carcome por dentro. No sé si ya se siente mejor, pero al menos ya no está sola con eso."
        elif estado_arco_mira == "afirmada":
            return "Algo cambió entre Mira y yo después de esa conversación. Se le nota distinta — más segura, aunque sea un poco."
        return ""

    registrar_arco_diario("Mira", resumen_diario_mira)


########################################################
# INTERACCIÓN PRINCIPAL — visitar a Mira desde el hub
########################################################

label interactuar_mira:

    if not companero_mira.en_party:
        "Mira no está contigo en este momento."
        return

    if estado_arco_mira == "cotidiana":
        jump mira_escena_cotidiana
    elif estado_arco_mira == "insinuando":
        jump mira_escena_insinuando
    elif estado_arco_mira == "abierta":
        jump mira_escena_abierta
    else:
        jump mira_escena_afirmada


########################################################
# ESTADO: COTIDIANA
########################################################

label mira_escena_cotidiana:

    scene bg templo_refugio with dissolve
    show mira at center

    $ mira_visitas_cotidiana += 1

    if mira_visitas_cotidiana == 1:
        mira "[nombre_protagonista]. ¿Vienes a rescatarme de la tarea más aburrida del mundo, o solo a interrumpir?"

        menu:
            "¿De qué hablan?"

            "Preguntarle en qué anda":
                mira "Catalogando suministros. Alguien tiene que hacerlo, y por lo visto ese alguien soy yo. No me quejo, pero tampoco es que me apasione."
                "Habla con su ligereza habitual, aunque [nombre_protagonista] nota algo, apenas, detrás de sus palabras."

            "Ofrecerte a ayudarla con lo que sea que hace":
                mira "¿En serio? No esperaba eso. Está bien, no rechazo la ayuda. Ven, te explico."
                "Pasan un rato trabajando juntos, en un silencio cómodo, cómplice, del tipo que solo se construye con años de conocerse."

    else:
        mira "Otra vez por aquí. No es que me moleste, para nada."
        "Charlan de cosas sin demasiado peso — el clima, la comida del refugio, algún rumor tonto de la ciudad. Es agradable, pero [nombre_protagonista] empieza a notar que Mira nunca deja que la conversación se acerque a nada realmente personal."

        menu:
            "¿[nombre_protagonista] intenta profundizar?"

            "Preguntarle directamente si está bien, de verdad":
                mira "..."
                "Se queda callada un instante más de lo normal."
                mira "¿Por qué lo preguntas?"
                "Su tono defensivo, apenas perceptible, confirma que la pregunta tocó algo."
                $ estado_arco_mira = "insinuando"

            "Dejar que la conversación siga su curso ligero":
                "[nombre_protagonista] decide no presionar, por ahora. Hay tiempo."

    return


########################################################
# ESTADO: INSINUANDO
########################################################

label mira_escena_insinuando:

    scene bg templo_refugio with dissolve
    show mira at center

    mira "[nombre_protagonista]. Sobre lo del otro día..."

    "Se detiene, como si estuviera decidiendo si de verdad quiere continuar esa frase."

    menu:
        "¿Cómo la anima [nombre_protagonista]?"

        "Esperar en silencio a que ella continúe":
            "No dices nada. Simplemente esperas, dándole el espacio que parece necesitar."

            mira "A veces siento que... no sé. Que si no estuviera aquí, nada cambiaría demasiado. Doran puede pelear con las manos desnudas si hace falta. Tú siempre sabes qué decisión tomar. Y yo solo... leo libros y ayudo con inventario."

            "Lo dice casi como si fuera un chiste, pero no lo es."

            $ estado_arco_mira = "abierta"

        "Decirle que no tiene que contarte nada que no quiera":
            mira "Gracias por eso. En serio."
            "Sin embargo, algo en su expresión sugiere que agradece más la oferta de espacio que el hecho de no tener que hablar."
            "El tema queda pendiente, pero la puerta sigue abierta para la próxima vez."

    return


########################################################
# ESTADO: ABIERTA (revelación del miedo de fondo)
########################################################

label mira_escena_abierta:

    scene bg templo_refugio with dissolve
    show mira at center

    mira "¿Puedo decirte algo que no le he dicho a nadie más?"

    "[nombre_protagonista] asiente, y Mira, por primera vez desde que la conoces, no encuentra un chiste con qué llenar el silencio antes de hablar."

    mira "Desde que caímos huyendo de la aldea, no dejo de pensar en que si algo me faltara... nadie lo notaría del todo. No como notarían si faltara Doran, o tú."

    if companero_perdido_id == "mira" or companero_recuperado:
        mira "Y después de lo del puente... de estar ahí sola, sin poder hacer nada más que sobrevivir... es como si el miedo se hubiera confirmado solo. Sobreviví, sí. Pero no pude ayudar a nadie mientras tanto."
        "Su voz tiembla apenas al decirlo, el recuerdo todavía demasiado cerca."
    else:
        mira "No es que quiera que algo malo pase, para que quede claro. Solo... a veces me pregunto qué aporto de verdad a todo esto, más allá de leer runas viejas."

    "[nombre_protagonista] tiene toda su atención puesta en ella ahora, sin saber todavía qué decir que no suene vacío."

    jump mira_momento_afirmacion


########################################################
# EL MOMENTO DE AFIRMACIÓN — bisagra del arco
########################################################

label mira_momento_afirmacion:

    menu:
        "¿Qué le responde [nombre_protagonista]?"

        "Recordarle un momento específico en que su ayuda fue decisiva":
            "[nombre_protagonista] no responde con generalidades vacías — le recuerda, con detalle, un momento concreto donde su criterio, su calma, o su conocimiento marcaron la diferencia real entre salir bien o mal de algo."
            mira "...no recordaba que lo vieras así."
            "Sus ojos brillan, contenidos, como si llevara mucho tiempo esperando escuchar exactamente eso, sin saberlo."
            $ protagonista.sumar_rasgo("car", 1)
            $ estado_arco_mira = "afirmada"

        "Decirle que su valor no depende de ser 'útil' en combate":
            mira "Fácil de decir. Más difícil de sentir, cuando ves a Doran partir en dos a un goblin de un solo golpe."
            "Aun así, algo en tu insistencia parece calar más hondo de lo que su respuesta seca sugiere."
            mira "...gracias, de todos modos. Creo que lo necesitaba escuchar, aunque no lo demuestre bien."
            $ estado_arco_mira = "afirmada"

    return


########################################################
# ESTADO: AFIRMADA (arco cerrado, con textura nueva)
########################################################

label mira_escena_afirmada:

    scene bg templo_refugio with dissolve
    show mira at center

    mira "[nombre_protagonista]. Oye... gracias otra vez por lo del otro día. No he dejado de pensarlo."

    "Hay una seguridad nueva, pequeña pero real, en cómo se para frente a ti ahora — como si una parte de ella hubiera decidido, aunque sea a medias, creerte."

    mira "De cualquier forma, ya volví a mis libros. Alguien tiene que ser la que entiende de qué rayos hablan esas runas."

    "Lo dice con humor, pero esta vez no suena a que se esté escondiendo detrás de él."

    return
