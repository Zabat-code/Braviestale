########################################################
# ARCO DE DORAN — "EL PESO DE LO QUE NO SE DIJO"
# ------------------------------------------------------
# Dinámica: cercanía de toda la vida -> algo se rompe entre
# ellos tras un evento traumático -> Doran se distancia y
# culpa (en parte injustamente) a [nombre_protagonista] ->
# el jugador reconstruye la confianza con el tiempo, sin un
# número de "rango" visible, solo estado narrativo.
#
# Gancho narrativo: si Doran fue quien cayó del puente (ver
# 06_troll_puente.rpy), el trauma es ESE evento — sobrevivió,
# pero algo en él cambió, y en el fondo culpa a
# [nombre_protagonista] por la decisión de las pociones.
# Si fue Mira quien cayó, Doran carga una culpa distinta:
# no haber podido hacer nada para evitarlo, y esa impotencia
# se transforma en irritabilidad hacia el protagonista.
#
# No hay conteo de interacciones. El arco avanza por FLAGS
# de estado, y cada visita ofrece contenido distinto según
# en qué estado narrativo se encuentre.
########################################################

# Estados posibles del arco (progresión no lineal, por flags):
#   "cercano"      -> estado inicial, antes de cualquier ruptura
#   "distante"     -> tras el evento traumático, Doran se aleja
#   "confrontado"  -> el jugador lo encaró o él mismo se abrió
#   "reconstruido" -> la confianza volvió, con matices nuevos
default estado_arco_doran = "cercano"
default doran_evento_disparado = False
default doran_confrontacion_hecha = False
default doran_visitas_distante = 0
define nombre_evento_doran = "el puente"

init python:

    def resumen_diario_doran():
        if estado_arco_doran == "cercano":
            return "Doran sigue siendo el mismo de siempre. Nada que anotar todavía, más allá de lo obvio: confío en él con los ojos cerrados."
        elif estado_arco_doran == "distante":
            if doran_visitas_distante == 0:
                return "Algo cambió en Doran desde " + nombre_evento_doran + ". Apenas me habla. Debería intentar hablar con él, aunque no sé bien por dónde empezar."
            else:
                return "Sigo intentando acercarme a Doran, pero se cierra en cuanto toco el tema. Tal vez necesite tiempo — o tal vez necesite que insista de otra forma."
        elif estado_arco_doran == "confrontado":
            return "Por fin hablamos de lo que pasó. No quedó resuelto del todo, pero al menos ya no hay silencio entre nosotros."
        elif estado_arco_doran == "reconstruido":
            return "Doran y yo volvimos a encontrar el paso. No es exactamente como antes — quizás es mejor. Ahora sabe que puede contarme las cosas difíciles."
        return ""

    registrar_arco_diario("Doran", resumen_diario_doran)


########################################################
# DISPARADOR DEL EVENTO TRAUMÁTICO
# ------------------------------------------------------
# Se llama una vez, al llegar a la ciudad, para fijar qué
# evento originó el distanciamiento de Doran según cómo se
# resolvió la escena del puente.
########################################################

label inicializar_arco_doran:

    if companero_perdido_id == "doran" or (companero_recuperado and estado_arco_doran == "cercano"):
        # Doran fue quien cayó del puente y ya fue recuperado
        # (o está por serlo) — el trauma es haber caído, sentirse
        # responsable de haber estado tan débil, y una punzada de
        # resentimiento hacia el protagonista por elegir curarse
        # a sí mismo en vez de a él (si ese fue el camino tomado).
        $ nombre_evento_doran = "la caída del puente"
        $ estado_arco_doran = "distante"
        $ doran_evento_disparado = True

    elif companero_perdido_id == "mira":
        # Mira fue quien cayó; Doran no pudo hacer nada para
        # evitarlo, y esa impotencia se le queda atravesada.
        $ nombre_evento_doran = "lo que pasó con Mira en el puente"
        $ estado_arco_doran = "distante"
        $ doran_evento_disparado = True

    else:
        # Nadie cayó (protagonista se sacrificó con las pociones):
        # Doran no tiene un trauma "de origen" tan marcado. Su
        # arco puede activarse más adelante por otro evento
        # menor durante la vida en la ciudad.
        pass

    return


########################################################
# INTERACCIÓN PRINCIPAL — visitar a Doran desde el hub
########################################################

label interactuar_doran:

    if not companero_doran.en_party:
        "Doran no está contigo en este momento."
        return

    if estado_arco_doran == "cercano":
        jump doran_escena_cercano
    elif estado_arco_doran == "distante":
        jump doran_escena_distante
    elif estado_arco_doran == "confrontado":
        jump doran_escena_confrontado
    else:
        jump doran_escena_reconstruido


########################################################
# ESTADO: CERCANO (antes de cualquier ruptura, o si nunca
# se disparó un trauma marcado — vida cotidiana normal)
########################################################

label doran_escena_cercano:

    scene bg ciudad_plaza with dissolve
    show doran at center

    doran "¡[nombre_protagonista]! Justo pensaba en ti. ¿Todo bien por aquí?"

    menu:
        "¿De qué hablan?"

        "Preguntarle cómo se siente con todo lo que ha pasado":
            doran "Sinceramente... mejor de lo que esperaba. Contigo y Mira cerca, se siente casi como estar en casa. Casi."
            "Habla con la misma honestidad simple de siempre — no hay nada que ocultar, todavía."

        "Recordar juntos algo de Aldenbrock":
            doran "¿Te acuerdas cuando el viejo Corven nos pilló robando manzanas y tu padre tuvo que pagarle el doble para que no lo contara?"
            "Se ríen un buen rato. Por un momento, el peso de todo lo demás se siente un poco más lejano."

    return


########################################################
# ESTADO: DISTANTE (tras el evento traumático)
########################################################

label doran_escena_distante:

    scene bg ciudad_plaza with dissolve
    show doran at center

    $ doran_visitas_distante += 1

    if doran_visitas_distante == 1:
        doran "...ah. Eres tú."
        "No hay calidez en su saludo, algo que antes era automático entre ustedes. Doran evita mirarte directamente."
        "[nombre_protagonista] no sabe bien qué decir. El silencio se estira más de lo cómodo."
        doran "Necesito estar solo un rato. No es nada personal."
        "Es evidente que sí lo es."
        return

    elif doran_visitas_distante == 2:
        doran "¿Otra vez aquí?"
        "No suena hostil del todo — más cansado que enojado."

        menu:
            "¿Cómo insiste [nombre_protagonista]?"

            "Preguntarle directamente qué le pasa":
                doran "¿Que qué me pasa? Lo que pasó. Eso me pasa. ¿No es obvio?"
                "Lo dice con más filo del que esperabas. Se arrepiente casi de inmediato, pero no se retracta."
                doran "Olvídalo. No debí decir eso así."
                "Se aleja antes de que puedas responder."

            "Simplemente quedarte cerca, sin presionar":
                "No dices nada. Te sientas cerca, sin exigir una conversación."
                "Doran no te aleja, pero tampoco habla. Pasan un rato así, en un silencio que —por primera vez desde la ruptura— no se siente completamente hostil."
                doran "...gracias por no irte. Aunque no lo demuestre."

        return

    else:
        doran "[nombre_protagonista]. Sigues viniendo, ¿eh?"
        "Algo en su tono ha cambiado, aunque todavía guarda distancia."
        "Este parece el momento de encarar el tema de frente, si [nombre_protagonista] se atreve."
        jump doran_confrontacion_disponible


########################################################
# LA CONFRONTACIÓN — momento de bisagra del arco
########################################################

label doran_confrontacion_disponible:

    menu:
        "¿[nombre_protagonista] encara la conversación pendiente?"

        "Decirle abiertamente lo que sintió con su distancia":
            $ protagonista.sumar_rasgo("car", 1)
            "[nombre_protagonista] respira hondo y dice lo que ha estado callando: que su silencio también duele, que no eligió que las cosas pasaran así, que también carga con lo que pasó."

            doran "..."

            "Doran se queda callado un largo rato, la mandíbula tensa."

            doran "Lo sé. Lo sé, ¿okay? Sé que no fue tu culpa, no realmente. Pero necesitaba culpar a alguien que no fuera... que no fuera nadie. O todo. No sé explicarlo bien."

            doran "Perdón por hacerte cargar con eso también."

            $ estado_arco_doran = "confrontado"
            $ doran_confrontacion_hecha = True

        "Disculparte, aunque no estés seguro de qué hiciste mal":
            doran "No... no tienes que disculparte tú. Ese es justo el problema — llevo días actuando como si la culpa fuera tuya cuando ni yo mismo sé bien de quién es."

            "Es la primera vez que Doran admite, aunque sea a medias, que su enojo nunca estuvo del todo bien dirigido."

            $ estado_arco_doran = "confrontado"
            $ doran_confrontacion_hecha = True

    return


########################################################
# ESTADO: CONFRONTADO (resuelto el conflicto directo,
# falta la reconstrucción plena)
########################################################

label doran_escena_confrontado:

    scene bg ciudad_plaza with dissolve
    show doran at center

    doran "Oye. Gracias por... por no rendirte conmigo, supongo. Sé que no lo hice fácil."

    menu:
        "¿Cómo responde [nombre_protagonista]?"

        "\"Para eso están los amigos, ¿no?\"":
            doran "Ja. Sí. Para eso están."
            "Algo en su postura se relaja, como si una parte de él por fin hubiera soltado el aire que llevaba conteniendo."
            $ estado_arco_doran = "reconstruido"

        "Preguntarle cómo se siente ahora, de verdad":
            doran "Mejor. No del todo bien, pero... mejor. Es raro, ¿sabes? Uno cree que va a estar bien apenas hablar de las cosas, pero es más lento que eso."
            "Habla con una honestidad nueva, distinta a la simpleza de antes — más consciente de sí mismo."
            $ estado_arco_doran = "reconstruido"

    return


########################################################
# ESTADO: RECONSTRUIDO (arco cerrado, con textura nueva)
########################################################

label doran_escena_reconstruido:

    scene bg ciudad_plaza with dissolve
    show doran at center

    doran "[nombre_protagonista]. ¿Todo en orden?"

    "La calidez ha vuelto, aunque no idéntica a como era antes — hay algo más consciente en cómo Doran te mira ahora, como quien ya sabe que la confianza también puede romperse y repararse."

    doran "Sea lo que sea que venga después de esto... me alegra que sigamos siendo nosotros. A pesar de todo."

    return
