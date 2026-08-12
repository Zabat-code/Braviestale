########################################################
# ARCO DE THERON — "RIVALES, NO AMIGOS, Y ESTÁ BIEN ASÍ"
# ------------------------------------------------------
# Dinámica: Theron tiene un rival académico de toda la vida
# dentro de la propia biblioteca del templo — un erudito
# mayor llamado Maestro Occam, que siempre lo superó en
# reconocimiento formal pese a que Theron es, en la práctica,
# más agudo. El arco NO termina en amistad cercana: termina
# en que Theron es ayudado por el protagonista en algo que le
# importa de verdad, y a partir de ahí hay respeto mutuo, sin
# dejar de ser dos personas que compiten por naturaleza.
########################################################

define maestro_occam = Character("Maestro Occam", color="#8a7a5c")

# Estados:
#   "distancia_cordial" -> colaboran por necesidad, sin cercanía
#   "rivalidad_visible"  -> Theron muestra su frustración con Occam
#   "prueba_compartida"  -> el protagonista lo ayuda en algo real
#   "respeto_mutuo"       -> arco cerrado, sin volverse "amigos"
default estado_arco_theron = "distancia_cordial"
default theron_ocasion_occam_vista = False

init python:

    def resumen_diario_theron():
        if estado_arco_theron == "distancia_cordial":
            return "Theron es útil y agradable, aunque siempre mantiene cierta distancia formal. No sé mucho de él más allá de los libros."
        elif estado_arco_theron == "rivalidad_visible":
            return "Descubrí que Theron carga una rivalidad de años con otro erudito de la ciudad, el Maestro Occam. Le molesta más de lo que admite."
        elif estado_arco_theron == "prueba_compartida":
            return "Ayudé a Theron con algo que de verdad le importaba — más allá de los libros. Todavía no sé si eso cambió algo entre nosotros."
        elif estado_arco_theron == "respeto_mutuo":
            return "Theron y yo no somos exactamente amigos cercanos, pero hay un respeto ahí que antes no existía. Le basta, y a mí también."
        return ""

    registrar_arco_diario("Theron", resumen_diario_theron)


########################################################
# INTERACCIÓN PRINCIPAL — visitar a Theron desde el hub
########################################################

label interactuar_theron:

    if not (companero_theron is not None and companero_theron.en_party):
        "Theron no está disponible por ahora — quizás aún no se ha unido al grupo."
        return

    if estado_arco_theron == "distancia_cordial":
        jump theron_escena_distancia_cordial
    elif estado_arco_theron == "rivalidad_visible":
        jump theron_escena_rivalidad_visible
    elif estado_arco_theron == "prueba_compartida":
        jump theron_escena_prueba_compartida
    else:
        jump theron_escena_respeto_mutuo


########################################################
# ESTADO: DISTANCIA CORDIAL
########################################################

label theron_escena_distancia_cordial:

    scene bg biblioteca_templo with dissolve
    show theron at center

    theron "[nombre_protagonista]. Justo a tiempo, encontré algo que podría interesarte sobre las runas de tu libro."

    menu:
        "¿De qué hablan?"

        "Escuchar lo que encontró sobre las runas":
            theron "Nada concluyente todavía, pero hay un patrón que se repite en textos de hace más de un siglo. Sea lo que sea esto, no es nuevo — solo olvidado."
            "Habla con precisión clínica, casi como si estuviera dando una lección a un público invisible más que conversando contigo."

        "Preguntarle algo sobre él mismo, no sobre el trabajo":
            theron "¿Sobre mí? No hay mucho que contar. Leo, investigo, corrijo a quien se equivoca. La vida de un erudito no es tan interesante como parece en las historias."
            "Lo dice con una ligereza que no termina de sonar del todo genuina — como una respuesta ya ensayada para desviar la pregunta."
            $ estado_arco_theron = "rivalidad_visible"

    return


########################################################
# ESTADO: RIVALIDAD VISIBLE
########################################################

label theron_escena_rivalidad_visible:

    scene bg biblioteca_templo with dissolve

    if not theron_ocasion_occam_vista:
        $ theron_ocasion_occam_vista = True

        "Al entrar, [nombre_protagonista] encuentra a Theron discutiendo, en voz baja pero tensa, con un hombre mayor de túnica académica."

        show maestro_occam at left
        show theron at right

        maestro_occam "Sigues citando fuentes de segunda mano, muchacho. En mis tiempos, eso ni siquiera calificaba como borrador."

        theron "Con todo respeto, Maestro, sus 'tiempos' llevan veinte años sin publicar nada que no sea una reedición de lo mismo."

        maestro_occam "Insolente. Ya veremos quién presenta primero algo de valor real al Consejo de la Ciudad."

        "El Maestro Occam se retira con la misma frialdad con la que llegó. Theron se queda con los puños apretados, respirando con más fuerza de la que admitiría."

        hide maestro_occam

        theron "...disculpa eso. No es algo que suela mostrar."

        menu:
            "¿Cómo reacciona [nombre_protagonista]?"

            "Preguntarle directamente qué hay entre Occam y él":
                theron "Ese hombre lleva veinte años siendo el erudito 'oficial' de esta ciudad. Yo llevo diez tratando de que alguien note que la mitad de sus teorías están mal fundamentadas. Adivina a quién escuchan."
                "Habla con una amargura que contrasta fuerte con su tono habitualmente controlado."
                theron "No es que necesite su aprobación. Es solo... cansado, tener siempre que demostrar el doble para que valga la mitad."

            "No presionar, simplemente ofrecerle ayudar en lo que sea que necesite":
                theron "Aprecio el gesto. Aunque no sé bien qué podrías hacer tú por un problema que llevo cargando desde antes de que llegaras a esta ciudad."
                "Aun así, algo en su tono se suaviza un poco ante la oferta, aunque no lo diga en voz alta."

    else:
        theron "[nombre_protagonista]. Perdón por lo del otro día, con Occam. No suelo perder la compostura así."

        "El tema queda ahí, latente, esperando una oportunidad real para resolverse de algo más que palabras."

    return


########################################################
# PRUEBA COMPARTIDA — bisagra del arco
# ------------------------------------------------------
# Se dispara cuando el jugador ayuda a Theron con algo real:
# conseguirle una fuente o material que necesita para
# presentar su investigación al Consejo antes que Occam.
########################################################

label theron_disparar_prueba_compartida:
    # Llamar este label desde algún punto de la trama principal
    # (ej. tras cierto avance de días, o vinculado a otra misión)
    # para dar pie a la escena decisiva.

    if estado_arco_theron != "rivalidad_visible":
        return

    scene bg biblioteca_templo with dissolve
    show theron at center

    theron "[nombre_protagonista]... tengo que pedirte algo, y no me resulta cómodo pedirlo."

    "Es la primera vez que Theron se muestra genuinamente incómodo frente a ti, sin el barniz de precisión académica de siempre."

    theron "Necesito una fuente que solo existe, hasta donde sé, en las ruinas del bosque donde encontraste tu libro de runas. Si consigo presentarla al Consejo antes que Occam publique su próxima teoría... por primera vez, tendría algo irrefutable."

    menu:
        "¿[nombre_protagonista] accede a ayudarlo?"

        "Ir a buscar la fuente que necesita":
            theron "Gracias. En serio. No sé bien cómo devolver esto."
            "[nombre_protagonista] parte hacia las ruinas —un desvío breve pero significativo, revisitando el lugar donde todo este hilo empezó— y regresa con lo que Theron necesitaba."

            scene bg biblioteca_templo with dissolve
            show theron at center

            theron "Esto es... esto es exactamente lo que necesitaba. [nombre_protagonista], no tengo palabras."

            "Por una vez, Theron no suena como quien está dando una lección. Suena, simplemente, agradecido."

            $ estado_arco_theron = "prueba_compartida"
            $ protagonista.sumar_rasgo("inte", 1)

        "Decirle que ese tipo de rivalidad no vale tanto esfuerzo":
            theron "Fácil de decir para quien no ha pasado diez años siendo ninguneado por decir la verdad de forma menos elegante que otro."
            "Lo dice sin rencor real, más resignado que ofendido — pero la oportunidad de ayudarlo de forma concreta se pierde, por ahora."

    return


########################################################
# ESTADO: PRUEBA COMPARTIDA
########################################################

label theron_escena_prueba_compartida:

    scene bg biblioteca_templo with dissolve
    show theron at center

    theron "El Consejo aceptó revisar mi presentación, gracias a lo que conseguiste. Todavía no sé si ganaré, pero al menos esta vez compito con algo real."

    menu:
        "¿Cómo responde [nombre_protagonista]?"

        "Decirle que se lo merece, gane o pierda":
            theron "...gracias. No estoy acostumbrado a que alguien lo diga sin esperar algo a cambio."
            $ estado_arco_theron = "respeto_mutuo"

        "Preguntarle si esto cambia algo con Occam":
            theron "No creo que Occam y yo dejemos de chocar nunca, la verdad. Pero por primera vez, siento que compito de igual a igual. Eso ya es más de lo que tenía antes."
            $ estado_arco_theron = "respeto_mutuo"

    return


########################################################
# ESTADO: RESPETO MUTUO (arco cerrado — sin volverse amistad
# cercana, deliberadamente)
########################################################

label theron_escena_respeto_mutuo:

    scene bg biblioteca_templo with dissolve
    show theron at center

    theron "[nombre_protagonista]. ¿Vienes por más lecturas, o solo a interrumpir mi trabajo otra vez?"

    "Lo dice con una media sonrisa que antes no tenía — no son exactamente amigos cercanos, y probablemente nunca lo serán del todo. Pero hay algo sólido entre ustedes ahora, algo que no necesita nombrarse como amistad para ser real."

    theron "De cualquier forma. Si vuelves a encontrar algo como aquel libro de runas, ya sabes a quién traérselo primero."

    return
