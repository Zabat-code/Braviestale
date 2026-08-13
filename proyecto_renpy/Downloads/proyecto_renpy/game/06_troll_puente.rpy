########################################################
# JEFE: TROLL DEL BOSQUE
# ------------------------------------------------------
# Al morir, el troll asesta un ataque fulminante de área
# que deja a los 3 miembros del grupo en HP crítico
# (calculado dinámicamente como % de su HP máximo actual).
# El botín son solo 2 POCIONES — no alcanza para los 3.
#
# Consecuencias:
#   - Si usas 1 poción en ti mismo + 1 en un compañero:
#     el compañero SIN poción queda crítico. Eso es lo que
#     determina, de forma orgánica, quién se salva en el
#     puente (sin necesidad de forzar nada más).
#   - Si usas AMBAS pociones en Doran y Mira (arriesgándote
#     a ti mismo): el juego te castiga con 3 encuentros
#     aleatorios antes del puente, todos dirigidos a ti,
#     obligándote a resolver tu propia supervivencia con
#     lo que tengas disponible.
########################################################

init python:

    def crear_troll_bosque(nivel=10):
        f = nivel / 10.0
        return EnemigoTipado(
            "Troll del Bosque", hp=int(180*f), ataque=int(16*f), defensa=int(6*f),
            agilidad=4, exp_otorga=int(120*f), oro_otorga=int(60*f),
            tipo="Tierra", sprite="troll_bosque", nivel=nivel,
            debil_arma="Impacto", resiste_arma="Corte"
        )


default inventario_pociones = 0
default pocion_usada_en_protagonista = False
default pocion_usada_en_doran = False
default pocion_usada_en_mira = False


label combate_jefe_troll:

    scene bg claro_ruinas_antiguas with fade
    play music "music/jefe_tema.ogg" fadein 1.0 loop

    "En un claro cubierto de piedras cubiertas de musgo —restos de algo mucho más antiguo que el pueblo— una silueta masiva se incorpora entre los árboles."

    "Un Troll. Más grande que cualquier ogro que hayan visto esa noche."

    doran "¡[nombre_protagonista], cuidado! ¡Esa cosa puede aplastarnos de un solo golpe!"

    mira "¡No hay otro camino, tenemos que pasar por aquí o nos alcanzarán los goblins!"

    $ troll = crear_troll_bosque(nivel=10)

    call combate([troll]) from _call_combate_troll_jefe

    if not protagonista.esta_vivo():
        jump combate_derrota

    jump troll_ataque_final


########################################################
# ATAQUE FULMINANTE POST-MORTEM DEL TROLL
########################################################

label troll_ataque_final:

    scene bg claro_ruinas_antiguas with vpunch

    "El Troll cae de rodillas, derrotado... pero antes de desplomarse por completo, descarga su puño contra el suelo con la poca fuerza que le queda."

    play sound "sfx/impacto_tierra.ogg"

    "La onda expansiva los alcanza a los tres. No hay forma de esquivarla."

    python:
        import random as _r

        def aplicar_golpe_critico(personaje):
            porcentaje_restante = _r.uniform(0.08, 0.15)
            personaje.hp = max(2, int(personaje.hp_max * porcentaje_restante))

        aplicar_golpe_critico(protagonista)
        aplicar_golpe_critico(companero_doran)
        aplicar_golpe_critico(companero_mira)

    "El impacto los lanza contra las rocas. Cuando [nombre_protagonista] logra incorporarse, el dolor es inmediato — apenas puede mantenerse en pie."

    doran "...auch. Eso... eso no se sintió nada bien."

    mira "Doran... [nombre_protagonista]... ¿están bien? Yo... apenas puedo moverme."

    "Los tres están al borde del colapso. Entre los restos del Troll, algo brilla: un pequeño saquito de cuero."

    "Dentro hay solo dos frascos de cristal azul. Pociones curativas."

    "Solo dos. Para los tres."

    jump decision_pociones


########################################################
# DECISIÓN DE LAS POCIONES
########################################################

label decision_pociones:

    $ inventario_pociones = 2

    "[nombre_protagonista] sostiene las dos pociones en la mano, sintiendo su propio pulso débil y errático."

    menu:
        "¿Qué hace [nombre_protagonista] con la primera poción?"

        "Usarla en sí mismo — si caes tú, todo termina aquí":
            $ pocion_usada_en_protagonista = True
            $ inventario_pociones -= 1
            python:
                protagonista.hp = min(protagonista.hp_max, protagonista.hp + int(protagonista.hp_max * 0.6))
            "Bebes la poción de un trago. El calor vuelve a tu cuerpo, la visión se aclara. Sigues en pie."
            jump decision_segunda_pocion

        "Dársela a Doran, se ve peor herido":
            $ pocion_usada_en_doran = True
            $ inventario_pociones -= 1
            python:
                companero_doran.hp = min(companero_doran.hp_max, companero_doran.hp + int(companero_doran.hp_max * 0.6))
            doran "[nombre_protagonista]... gracias. No tenías que—"
            "\"Cállate y levántate\", le dices, con más firmeza de la que sientes."
            jump decision_segunda_pocion

        "Dársela a Mira, apenas puede sostenerse":
            $ pocion_usada_en_mira = True
            $ inventario_pociones -= 1
            python:
                companero_mira.hp = min(companero_mira.hp_max, companero_mira.hp + int(companero_mira.hp_max * 0.6))
            mira "N-no debiste... pero... gracias, [nombre_protagonista]."
            jump decision_segunda_pocion


label decision_segunda_pocion:

    "Queda una última poción. [nombre_protagonista] mira a su alrededor: a sí mismo, a Doran, a Mira. Los tres apenas se sostienen en pie."

    python:
        opciones_disponibles = []
        if not pocion_usada_en_protagonista:
            opciones_disponibles.append("protagonista")
        if not pocion_usada_en_doran:
            opciones_disponibles.append("doran")
        if not pocion_usada_en_mira:
            opciones_disponibles.append("mira")

    menu:
        "¿A quién le da la última poción?"

        "Usarla en ti mismo" if "protagonista" in opciones_disponibles:
            $ pocion_usada_en_protagonista = True
            python:
                protagonista.hp = min(protagonista.hp_max, protagonista.hp + int(protagonista.hp_max * 0.6))
            "Bebes la última poción. No te sientes orgulloso de la decisión, pero sabes que sin ti, nadie más sale de este bosque."
            jump resolucion_pociones

        "Dársela a Doran" if "doran" in opciones_disponibles:
            $ pocion_usada_en_doran = True
            python:
                companero_doran.hp = min(companero_doran.hp_max, companero_doran.hp + int(companero_doran.hp_max * 0.6))
            doran "¿Por qué a mí...? [nombre_protagonista], si algo te pasa por mi culpa—"
            "\"No va a pasar nada. Solo camina\", respondes, sin estar del todo seguro."
            jump resolucion_pociones

        "Dársela a Mira" if "mira" in opciones_disponibles:
            $ pocion_usada_en_mira = True
            python:
                companero_mira.hp = min(companero_mira.hp_max, companero_mira.hp + int(companero_mira.hp_max * 0.6))
            mira "[nombre_protagonista]... no voy a olvidar esto."
            jump resolucion_pociones


########################################################
# RESOLUCIÓN: determinar si el protagonista se arriesgó
########################################################

label resolucion_pociones:

    if pocion_usada_en_protagonista:
        if not pocion_usada_en_doran:
            $ companero_perdido_id = "doran"
        else:
            $ companero_perdido_id = "mira"

        "Con las pociones repartidas, el grupo logra estabilizarse lo suficiente para seguir moviéndose — aunque el camino no será fácil para todos por igual."

        jump camino_al_puente

    else:
        "Ambas pociones fueron para Doran y Mira. [nombre_protagonista] respira con dificultad, sosteniéndose de un árbol para no caer — pero sigue de pie."

        doran "[nombre_protagonista], estás... no te ves nada bien."

        "\"Estoy bien. Sigamos moviéndonos\", mientes, y ellos, demasiado agotados para discutir, te creen."

        jump camino_al_puente_riesgo


########################################################
# CAMINO SEGURO AL PUENTE (protagonista curado)
########################################################

label camino_al_puente:

    scene bg bosque_noche_persecucion with dissolve

    "El grupo avanza, más lento de lo que querrían, pero con vida. A la distancia, el sonido de gruñidos y pisadas pesadas les recuerda que la persecución no ha terminado."

    jump escena_puente


########################################################
# CAMINO ARRIESGADO (protagonista sin curar — 3 encuentros forzados)
########################################################

label camino_al_puente_riesgo:

    scene bg bosque_noche_persecucion with dissolve

    "Cada paso duele. [nombre_protagonista] aprieta los dientes y sigue caminando, consciente de que un solo tropiezo podría costarle todo."

    $ encuentros_forzados_restantes = 3

    label loop_encuentros_riesgo:

        if encuentros_forzados_restantes <= 0:
            jump fin_encuentros_riesgo

        "Algo se mueve entre los árboles. De nuevo."

        $ enemigo_riesgo = tirar_encuentro_zona("bosque_gris")

        "El combate es más difícil de lo normal — [nombre_protagonista] apenas puede mantenerse en pie, y cada golpe que recibe pesa el doble."

        call combate([enemigo_riesgo]) from _call_combate_riesgo_puente

        if not protagonista.esta_vivo():
            "El cuerpo de [nombre_protagonista] finalmente cede al agotamiento y a las heridas acumuladas."
            jump combate_derrota

        $ encuentros_forzados_restantes -= 1
        jump loop_encuentros_riesgo

    label fin_encuentros_riesgo:
        "Contra todo pronóstico, [nombre_protagonista] sigue en pie. Malherido, pero vivo."

        $ companero_perdido_id = None

        jump escena_puente

    return


########################################################
# ESCENA DEL PUENTE — la separación se resuelve aquí
########################################################

label escena_puente:

    scene bg puente_colgante_bosque with dissolve
    play sound "sfx/viento_fuerte.ogg"

    "Un puente colgante, viejo y desgastado, es la única forma de cruzar el barranco que se abre ante ustedes."

    doran "No tiene muy buena pinta, pero no hay otra opción. Vamos, rápido, antes de que algo más nos alcance."

    if companero_perdido_id is None:
        "Cruzan uno por uno, el puente crujiendo bajo cada paso. Las maderas ceden un poco, pero resisten."

        "Los tres llegan al otro lado, agotados pero juntos."

        jump escape_bruja_o_continuar

    else:
        $ nombre_perdido = "Doran" if companero_perdido_id == "doran" else "Mira"
        $ nombre_quedado = "Mira" if companero_perdido_id == "doran" else "Doran"

        "[nombre_protagonista] cruza primero, con piernas temblorosas. Luego [nombre_perdido], todavía débil por la herida sin curar."

        "A medio camino, una de las maderas cede bajo su peso."

        play sound "sfx/madera_rota.ogg"

        if companero_perdido_id == "doran":
            show doran at center with vpunch
            doran "¡[nombre_protagonista]!"
        else:
            show mira at center with vpunch
            mira "¡[nombre_protagonista]!"

        "El puente se parte. [nombre_protagonista] alcanza a sujetarse del borde — pero [nombre_perdido] no tiene la fuerza suficiente para aferrarse."

        "Solo hay tiempo para ver cómo cae hacia la niebla del barranco, la voz perdiéndose en la distancia."

        python:
            if companero_perdido_id == "doran":
                companero_doran.en_party = False
            else:
                companero_mira.en_party = False

        "El resto del puente se derrumba tras [nombre_protagonista]. Del otro lado, ya no queda forma de cruzar."

        "[nombre_protagonista] se queda solo con [nombre_quedado], ambos mirando hacia la niebla donde [nombre_perdido] desapareció."

        jump escape_bruja_o_continuar


label escape_bruja_o_continuar:
    jump casa_bruja_llegada


########################################################
# MISIÓN DE RECUPERACIÓN — EL COMPAÑERO PERDIDO Y LA ARPÍA
# ------------------------------------------------------
# BETTINA, vecina de la ciudad, reporta el robo de objetos
# brillantes de su casa. Seguir el rastro lleva a una cueva
# donde se encuentra al compañero perdido (Doran o Mira,
# según cuál cayó del puente). Tras el reencuentro, la Bruja
# de escenas anteriores aparece y se revela como Arpía — jefe
# de esta misión, combate OBLIGATORIO de ganar.
########################################################

default arpia_derrotada = False

label mision_recuperar_companero_perdido:

    if companero_perdido_id is None:
        "No hay nadie que recuperar — Doran y Mira siguen juntos."
        return

    $ nombre_perdido_mision = "Doran" if companero_perdido_id == "doran" else "Mira"

    scene bg templo_refugio with dissolve

    "Una mujer se acerca, dudosa, retorciéndose las manos."

    "Bettina" "Disculpa... ¿tú eres de los que llegaron hace poco? Necesito ayuda. Alguien — o algo — entró a mi casa anoche y se llevó todo lo que brillaba. Monedas, un broche de plata, hasta los clavos de la puerta."

    "Bettina" "Seguí el rastro hasta la entrada de una cueva, cerca del límite del bosque. No me atreví a entrar sola."

    "[nombre_protagonista] duda solo un instante. Una cueva, cerca del bosque — el mismo bosque del que [nombre_perdido_mision] nunca volvió a salir."

    "Bettina" "Te pagaré lo que pueda si recuperas aunque sea parte de lo robado. Pero ten cuidado... dicen que esa cueva no está vacía."

    jump mision_rescate_cueva


label mision_rescate_cueva:

    scene bg cueva_entrada with dissolve
    play music "music/tension.ogg" fadein 1.0 loop

    "La entrada de la cueva es estrecha, apenas iluminada por la luz que se cuela desde afuera. Algo brilla tenue en el fondo — restos de lo robado, amontonados como un nido."

    call intentar_encuentro_aleatorio("cuevas") from _call_encuentro_cueva_rescate

    if not protagonista.esta_vivo():
        jump combate_derrota

    "Más adentro, entre las sombras, algo se mueve."

    if companero_perdido_id == "doran":
        jump reencuentro_doran
    else:
        jump reencuentro_mira


########################################################
# REENCUENTRO CON DORAN
########################################################

label reencuentro_doran:

    scene bg cueva_interior with dissolve

    "Una figura se encoge contra la pared de roca, a la defensiva, sosteniendo una piedra afilada como si fuera un arma."

    show doran at center with dissolve
    doran "¿[nombre_protagonista]...? ¿[nombre_protagonista]!"

    "Es él. Delgado, sucio, con la ropa hecha jirones — pero vivo."

    doran "Pensé que... pensé que no volvería a ver a nadie conocido. Caí del puente, el agua me arrastró río abajo, y desde entonces he estado escondiéndome aquí, robando lo que podía para sobrevivir."

    doran "Lo siento por lo de la casa de esa mujer. No sabía qué más hacer."

    "[nombre_protagonista] no sabe si abrazarlo o gritarle. Termina haciendo ambas cosas, en ese orden."

    menu:
        "¿Doran participa en lo que viene?"

        "Decirle que se quede atrás, ya ha pasado suficiente":
            doran "¿Estás loco? Después de todo esto, no pienso quedarme sentado. Vine a pelear si hace falta."
            $ doran_participa_combate_arpia = True

        "Dejar que decida él mismo si pelea":
            doran "Dame un arma. No voy a dejar que hagas esto solo, no de nuevo."
            $ doran_participa_combate_arpia = True

    jump revelacion_arpia


########################################################
# REENCUENTRO CON MIRA
########################################################

label reencuentro_mira:

    scene bg cueva_interior with dissolve

    "Junto a un pequeño árbol torcido que crece imposible entre las rocas, una figura se incorpora al oír pasos."

    show mira at center with dissolve
    mira "¿[nombre_protagonista]? ¿De verdad eres tú?"

    "Está pálida, más delgada de lo que recuerdas, pero con esa misma mirada aguda de siempre."

    mira "Sobreviví gracias a este árbol — sus frutos, al menos, no me mataron en el intento. He estado juntando lo que brilla porque... no sé, pensé que si alguien me buscaba, vería el reflejo desde lejos."

    "Se ríe de su propia idea, con una risa cansada."

    mira "Funcionó, después de todo."

    "[nombre_protagonista] la abraza antes de que pueda decir nada más."

    menu:
        "¿Mira participa en lo que viene?"

        "Decirle que se quede atrás, ya ha pasado suficiente":
            mira "No. He tenido tiempo de sobra para pensar aquí sola. No pienso quedarme quieta ahora que por fin puedo hacer algo."
            $ mira_participa_combate_arpia = True

        "Dejar que decida ella misma si pelea":
            mira "Gracias por confiar en que puedo. Vamos."
            $ mira_participa_combate_arpia = True

    jump revelacion_arpia


default doran_participa_combate_arpia = False
default mira_participa_combate_arpia = False


########################################################
# REVELACIÓN: LA BRUJA ES LA ARPÍA
########################################################

label revelacion_arpia:

    scene bg cueva_interior with vpunch
    play sound "sfx/alarma_aldea.ogg"

    "Un chillido agudo resuena desde el fondo de la cueva, seguido de un batir de alas que no debería caber en un espacio tan estrecho."

    "La misma silueta que los recibió en la cabaña del bosque emerge de la oscuridad — pero ya no oculta lo que es."

    show bruja_arpia at center with vpunch

    "Donde antes había una anciana de mirada calma, ahora hay plumas oscuras entretejidas con piel humana, garras donde deberían estar las manos, y esos mismos ojos, ahora completamente amarillos."

    bruja "Vaya, vaya... el sabor que se me escapó en el bosque, viniendo directo a mi nido. Qué generoso."

    doran "¡Esa cosa es la bruja de la cabaña!"

    mira "¡Es un monstruo, siempre lo fue!"

    "No hay tiempo para más preguntas. La Arpía extiende las alas por completo, bloqueando la única salida."

    jump combate_jefe_arpia


########################################################
# JEFE: LA ARPÍA (= LA BRUJA)
# ------------------------------------------------------
# Combate OBLIGATORIO de ganar. Si el jugador pierde, se
# activa reintento inmediato del mismo combate (no hay
# checkpoint anterior ni pérdida de diálogo ya visto).
########################################################

init python:

    def crear_arpia_jefe(nivel=15):
        f = nivel / 15.0
        return EnemigoTipado(
            "La Arpía", hp=int(220*f), ataque=int(18*f), defensa=int(5*f),
            agilidad=16, exp_otorga=int(150*f), oro_otorga=int(80*f),
            tipo="Aire", sprite="bruja_arpia", nivel=nivel,
            debil_arma="Proyectil", resiste_arma="Corte"
        )


label combate_jefe_arpia:

    $ arpia = crear_arpia_jefe(nivel=15)

    # Nota de diseño: si Doran/Mira decidieron participar,
    # aquí es donde se conectaría su unidad de combate al
    # encuentro (el motor de combate actual soporta un solo
    # personaje activo — pendiente extender a combate de party
    # completa si se desea que peleen activamente en pantalla).

    call combate([arpia]) from _call_combate_arpia_jefe

    if not protagonista.esta_vivo():
        # Combate obligatorio: reintento inmediato del mismo
        # combate, sin retroceder a un punto anterior.
        "El mundo se oscurece por un instante — pero algo te hace abrir los ojos de nuevo, con otra oportunidad de enfrentarla."
        jump combate_jefe_arpia

    $ arpia_derrotada = True

    jump post_combate_arpia


label post_combate_arpia:

    scene bg cueva_interior with vpunch

    "La Arpía se retuerce, herida, y con un último chillido se lanza hacia una grieta en el techo de la cueva, desapareciendo hacia el cielo nocturno."

    bruja "Esto no termina aquí, pequeños... nada termina realmente, cuando se sirve a algo más grande."

    "Sus palabras se pierden en el viento. No la persiguen — no tienen fuerzas, y lo que queda de la cueva empieza a ceder."

    "[nombre_protagonista] toma lo que puede del botín brillante —lo suficiente para devolverle algo a Bettina— y sale de la cueva junto con [nombre_perdido_mision], por fin de vuelta."

    python:
        if companero_perdido_id == "doran":
            companero_doran.en_party = True
        else:
            companero_mira.en_party = True
        companero_recuperado = True
        companero_perdido_id = None

    scene bg templo_refugio with dissolve

    "Bettina" "¡Lo lograste! No... no puedo creerlo. Toma, es lo poco que puedo ofrecerte, pero es sincero."

    $ oro_jugador += 25

    "[nombre_perdido_mision] vuelve a estar junto a ti, junto al resto del grupo. No todo estaba perdido."

    return
