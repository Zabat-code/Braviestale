########################################################
# NPCs DE AMBIENTACIÓN — CIUDADELA DEL VALLE HONDO
# ------------------------------------------------------
# Elenco secundario que da textura y variedad racial al
# mundo. No son reclutables ni romanceables (a diferencia
# del elenco principal de 6), pero algunos tienen función
# jugable: el Coliseo (combate opcional) y la escena de
# los soldados/fanáticos (elección moral puntual).
########################################################

define thrain = Character("Thrain", color="#c9915a")       # enano, herrero de la ciudad
define lyanwe = Character("Lyanwë", color="#7ec9a8")        # elfa, encargada de la biblioteca
define gorrak = Character("Gorrak", color="#a85c3f")        # orco, campeón del Coliseo
define soldado1 = Character("Soldado", color="#7a7a7a")
define fanatico1 = Character("Predicador", color="#c9b25a")
define pueblerino_asustado = Character("Refugiado", color="#9a9a9a")


########################################################
# THRAIN — HERRERO ENANO DE LA CIUDAD
# ------------------------------------------------------
# Ambientación con un poco de función: reconoce el trabajo
# del padre del protagonista si se le muestra algo forjado
# por Bram, dándole una línea de diálogo única.
########################################################

label visitar_herreria_thrain:

    scene bg herreria_ciudad with dissolve
    show thrain at center

    thrain "¿Buscas algo afilado, algo que aguante golpes, o simplemente estás perdiendo el tiempo mirando mi trabajo?"

    "Thrain apenas te mira, concentrado en el yunque. Los enanos de la Ciudadela tienen fama de no perder el tiempo con cortesías innecesarias — y él cumple la fama al pie de la letra."

    menu:
        "¿Cómo interactúa [nombre_protagonista]?"

        "Mostrarle una de las armas que trajiste de casa":
            thrain "Espera... esta marca. ¿De dónde sacaste esto?"
            "Examina el arma con una atención que contradice su tono brusco de hace un momento."
            thrain "Este trabajo... conozco esta marca. Un herrero de pueblo, técnica sólida, sin escuela formal pero con oficio de verdad. ¿Está vivo?"

            menu:
                "¿Qué responde [nombre_protagonista]?"

                "Decirle que es tu padre":
                    thrain "...entonces dile, si lo encuentras, que un enano de la Ciudadela respeta su trabajo. No es un cumplido que reparta seguido."
                    "Por primera vez, algo parecido a calidez cruza su rostro curtido."

                "No decir nada, solo asentir":
                    thrain "Como quieras. De todos modos, buen trabajo es buen trabajo, venga de donde venga."

        "Preguntar por sus servicios":
            thrain "Reparo, afilo, forjo bajo encargo. No hago caridad, pero tampoco cobro de más a quien no la tiene fácil. Ustedes los refugiados ya cargan suficiente."

    return


########################################################
# LYANWË — ELFA ENCARGADA DE LA BIBLIOTECA
# ------------------------------------------------------
# Nota: distinta de Theron (que trabaja EN la biblioteca del
# TEMPLO). Lyanwë dirige la biblioteca pública de la ciudad,
# un espacio separado. Puede dar contexto de lore adicional.
########################################################

label visitar_biblioteca_lyanwe:

    scene bg biblioteca_publica_ciudad with dissolve
    show lyanwe at center

    lyanwe "Bienvenido. Aquí encontrarás silencio, que ya es más de lo que ofrece el resto de esta ciudad abarrotada."

    "Habla con una calma medida, casi ensayada — la clase de calma que viene de haber vivido mucho más tiempo del que aparenta."

    menu:
        "¿Sobre qué pregunta [nombre_protagonista]?"

        "Preguntarle sobre los ataques de goblins y ogros organizados":
            lyanwe "Interesante que preguntes. Hay registros antiguos de grupos que buscaban dominar bestias mediante magia prohibida — comunicarse con ellas, controlarlas, eventualmente fusionarse con ellas."
            lyanwe "Se creía erradicado hace generaciones. Si esos registros ya no son solo historia... el mundo tiene un problema mayor del que parece."
            "[nombre_protagonista] siente un escalofrío — esto coincide, casi palabra por palabra, con lo que Theron mencionó."

        "Preguntarle por su pueblo, los elfos":
            lyanwe "Ah. Complicado. Mi gente prefiere no mezclarse con el resto de las razas — nuestras aldeas están cerradas a quien no sea élfico, por decisión propia, no por rechazo ajeno."
            lyanwe "Yo elegí vivir aquí, entre ustedes. No todos en mi pueblo estarían de acuerdo con esa elección."
            "Lo dice sin amargura evidente, aunque algo en su tono sugiere que no es un tema que disfrute profundizar."

    return


########################################################
# EL COLISEO — COMBATE OPCIONAL CONTRA GORRAK
# ------------------------------------------------------
# Jefe opcional. Recompensa: un arma única (Hacha de
# Doran Ancestral... no, ver abajo) que, si se equipa a
# Doran específicamente, desata un mini-momento de afinidad
# y él le da al jugador un ítem a cambio.
########################################################

default coliseo_gorrak_derrotado = False
default arma_gorrak_obtenida = False
default arma_gorrak_dada_a_doran = False

init python:

    def crear_gorrak_jefe(nivel=12):
        f = nivel / 12.0
        return EnemigoTipado(
            "Gorrak, Campeón del Coliseo", hp=int(200*f), ataque=int(17*f), defensa=int(7*f),
            agilidad=8, exp_otorga=int(130*f), oro_otorga=int(70*f),
            tipo="Tierra", sprite="gorrak_orco", nivel=nivel,
            debil_arma="Proyectil", resiste_arma="Impacto"
        )


label visitar_coliseo:

    scene bg coliseo_ciudad with dissolve

    "El Coliseo de la Ciudadela del Valle Hondo — un anfiteatro de piedra desgastada donde los mercenarios y curiosos apuestan sobre combates de exhibición."

    if coliseo_gorrak_derrotado:
        "Los gradas están vacías por hoy. Gorrak descansa apoyado en su hacha, observando el ruedo con la mirada perdida de quien ya venció a todos los retadores que le importaban."
        return

    show gorrak at center
    gorrak "Otro refugiado con ganas de probar suerte, ¿eh? He perdido la cuenta de cuántos como tú han terminado en el suelo."

    "Gorrak es enorme incluso para ser orco, con cicatrices que cuentan más combates de los que cualquiera podría presumir sobrar."

    menu:
        "¿[nombre_protagonista] se enfrenta a Gorrak?"

        "Aceptar el desafío":
            gorrak "¡Así se habla! Vamos a ver de qué estás hecho."
            jump combate_gorrak

        "Rechazar por ahora":
            gorrak "Sabia decisión, o cobarde. El ruedo sigue aquí cuando cambies de opinión."
            return


label combate_gorrak:

    $ gorrak_enemigo = crear_gorrak_jefe(nivel=12)

    call combate([gorrak_enemigo]) from _call_combate_gorrak

    if not protagonista.esta_vivo():
        # Combate opcional: NO hay reintento forzado. El jugador
        # puede simplemente retirarse y volver a intentarlo después
        # si quiere, sin Game Over — a diferencia de Bruja/Arpía.
        scene bg coliseo_ciudad with dissolve
        show gorrak at center
        gorrak "Ja. No está mal para un primer intento. Vuelve cuando quieras la revancha."
        "[nombre_protagonista] se retira del ruedo, magullado pero consciente. El Coliseo no exige que te juegues la vida — solo el orgullo."
        return

    scene bg coliseo_ciudad with vpunch
    show gorrak at center

    gorrak "...¡Ja! No lo esperaba, la verdad. Hace tiempo que nadie me hacía sudar así."

    "El público disperso que quedaba estalla en aplausos dispersos. Gorrak, sin rencor aparente, te tiende algo envuelto en tela áspera."

    gorrak "Toma. La gané hace años, en un torneo del que ya nadie se acuerda. Nunca encontré a nadie que la mereciera de verdad. Quizás tú sí."

    "Dentro de la tela hay un hacha de guerra, pesada, con el filo aún intacto pese a los años — un arma pensada para alguien de fuerza descomunal."

    $ coliseo_gorrak_derrotado = True
    $ arma_gorrak_obtenida = True

    "[nombre_protagonista] no tiene la fuerza ni el estilo de combate para aprovecharla del todo. Pero conoce a alguien que sí."

    return


########################################################
# EQUIPAR EL HACHA DE GORRAK A DORAN
# ------------------------------------------------------
# Acción disponible desde el hub una vez obtenida el arma.
# Darle el hacha a Doran específicamente desata un momento
# de afinidad y él corresponde con un ítem propio.
########################################################

label entregar_hacha_a_doran:

    if not arma_gorrak_obtenida:
        "No tienes ningún arma que darle a Doran por ahora."
        return

    if arma_gorrak_dada_a_doran:
        "Ya le diste el hacha a Doran. La lleva consigo desde entonces."
        return

    if not companero_doran.en_party:
        "Doran no está contigo en este momento."
        return

    scene bg ciudad_plaza with dissolve
    show doran at center

    "[nombre_protagonista] le muestra el hacha ganada en el Coliseo."

    doran "¿Esto es...? Espera, ¿ESTO es tuyo? [nombre_protagonista], esta hacha pesa más que un yunque, ¿de dónde—"

    "Le cuentas sobre Gorrak, el combate, todo."

    doran "Y me la das a mí, sin más."

    menu:
        "¿Qué le dice [nombre_protagonista]?"

        "\"Nadie la va a usar mejor que tú\"":
            doran "..."
            "Doran se queda mirando el hacha un momento, algo incómodo con el cumplido directo, pero visiblemente conmovido."
            doran "Gracias, [nombre_protagonista]. En serio. Toma, no es gran cosa, pero... la he cargado desde que salimos de Aldenbrock. Me la dio mi padre, para cuando fuera lo bastante grande."

        "\"Necesitas algo mejor que espadas de práctica\"":
            doran "Ja, no te falta razón. Está bien, la acepto. Y ya que estamos siendo prácticos..."
            doran "Toma esto. La he cargado desde que salimos de Aldenbrock, mi padre me la dio para cuando fuera lo bastante grande. Creo que es tu turno de tenerla."

    "Doran te entrega un pequeño amuleto de madera tallada, gastado por el uso — algo que claramente ha llevado consigo con cuidado todo este tiempo."

    $ arma_gorrak_dada_a_doran = True
    $ protagonista.sumar_rasgo("vol", 1)

    python:
        companero_doran.tipo_arma_equipada = "Impacto"  # el hacha es de tipo Impacto

    "Doran empieza a usar el hacha de inmediato, con un entusiasmo torpe pero genuino. Algo entre ustedes se siente un poco más firme desde entonces."

    return


########################################################
# CONFLICTO MORAL — SOLDADOS Y FANÁTICOS
# ------------------------------------------------------
# Escena puntual con elección moral. Sin consecuencias
# mecánicas duraderas (no afecta afinidad, oro, ni stats) —
# es una decisión de caracterización del protagonista.
########################################################

label escena_soldados_fanaticos:

    scene bg callejon_ciudad with dissolve

    "Cruzando un callejón cerca del mercado, [nombre_protagonista] se topa con una escena que no debería ser tan común como aparenta serlo."

    show soldado1 at left
    show pueblerino_asustado at right

    soldado1 "¿No entiendes las reglas? Los refugiados pagan tasa de 'protección'. Así son las cosas aquí. ¿O prefieres que tu gente duerma en la calle?"

    pueblerino_asustado "Por favor, ya les di todo lo que tenía esta semana, no me queda—"

    "El soldado lo empuja contra la pared, sin demasiada fuerza, pero con la clara intención de intimidar más que de lastimar. Nadie más en la calle parece dispuesto a mirar dos veces."

    show fanatico1 at center

    fanatico1 "Interesante mundo este, ¿no? Hasta los humanos más débiles reciben trato especial por sobre las otras razas. Es el orden natural reafirmándose, aunque sea de esta forma tan... burda."

    "El predicador observa la escena desde unos metros, sin intervenir, comentando como quien narra un espectáculo ajeno."

    menu:
        "¿Qué hace [nombre_protagonista]?"

        "Intervenir directamente, encarar al soldado":
            $ protagonista.sumar_rasgo("car", 1)
            soldado1 "¿Y a ti quién te dio vela en este entierro? Otro refugiado con aires de héroe, genial."
            "El soldado te mide con la mirada un momento — y decide que no vale la pena el problema. Suelta al pueblerino y se aleja, no sin antes escupir en el suelo cerca de tus pies."
            pueblerino_asustado "G-gracias... no todos aquí son así, ¿verdad?"
            fanatico1 "Admirable, en su forma ingenua. El orden encuentra su cauce de todos modos, tarde o temprano."
            "El predicador se retira sin más, como si la interrupción apenas mereciera su atención."

        "Reportar lo que viste a la guardia de la ciudad, sin intervenir directamente":
            "Encuentras a otro guardia más adelante y le cuentas lo que presenciaste. Recibes una mirada cansada, casi resignada."
            "Guardia" "Ya lo sé. Lo sabemos todos. No es tan simple resolverlo cuando la mitad del cuerpo de guardia mira para otro lado a cambio de su parte."
            "No hay una solución inmediata, pero al menos la información queda en algún lado."

        "Seguir de largo, no es tu pelea":
            "[nombre_protagonista] sigue caminando. Hay demasiadas batallas que pelear como para cargar con todas las que no son suyas."
            "El eco de la voz del pueblerino, pidiendo ayuda, se queda contigo más tiempo del que te gustaría admitir."

    return
