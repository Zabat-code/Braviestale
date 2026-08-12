########################################################
# CAPÍTULO 1 — "LA FORJA ROTA"
# ------------------------------------------------------
# Estructura:
#   1. Tutorial (ver 01_stats_system.rpy)
#   2. Ataque goblin/ogro sobre la aldea natal -> huida
#   3. Bosque Gris (exploración + combates aleatorios)
#   4. Casa de la Bruja
#   5. Escape de la bruja
#   6. Ciudad refugio: misiones secundarias con los 4 romances
#   7. Clímax: ataque a la ciudad -> rescate condicionado
#      por afinidad -> cierre del capítulo
########################################################

label start:

    call inicializar_romances from _call_init_romances
    call tutorial_creacion_personaje from _call_tutorial

    jump ataque_aldea


########################################################
# 2. ATAQUE A LA ALDEA
########################################################

label ataque_aldea:

    scene bg herreria_interior night with fade

    "Te despiertan gritos. No los gritos ocasionales de una pelea de taberna — gritos de verdad."

    play sound "sfx/alarma_aldea.ogg"

    show padre_herrero at center with dissolve
    padre "¡[nombre_protagonista], despierta! ¡Nos atacan!"

    scene bg aldea_incendio with vpunch
    play music "music/tension.ogg" fadein 1.0

    "Sales corriendo. El cielo nocturno está teñido de naranja. Las casas arden. Entre el humo, distingues siluetas verdes, torpes y numerosas — goblins — y una figura mucho más grande abriéndose paso entre ellas."

    "Un ogro."

    show doran at left
    show mira at right
    doran "¡[nombre_protagonista]! ¡Por aquí, rápido!"
    mira "¡No hay tiempo, tenemos que salir del pueblo AHORA!"

    padre "¡Vayan al Bosque Gris, yo los alcanzo, tengo que sacar a más gente de aquí!"

    menu:
        "Tu padre te grita que corras. ¿Qué haces?"

        "Obedeces y corres con Doran y Mira":
            $ protagonista.sumar_rasgo("vol", 1)
            "Confías en que tu padre sabe lo que hace. Corres."

        "Intentas quedarte a ayudar, aunque sea un segundo más":
            $ protagonista.sumar_rasgo("car", 1)
            padre "¡HE DICHO QUE CORRAS! ¡No voy a perderte a ti también!"
            "Algo en su voz —desesperación pura— te hace obedecer al fin."

    call crear_party_inicial from _call_party_inicial

    "Corres junto a Doran y Mira, dejando atrás el único hogar que has conocido, mientras el fuego devora la aldea a tus espaldas."

    jump bosque_gris_llegada


########################################################
# 3. BOSQUE GRIS — exploración + combates aleatorios
########################################################

label bosque_gris_llegada:

    scene bg bosque_entrada with fade
    stop music fadeout 2.0
    play music "music/bosque_ambiente.ogg" fadein 2.0 loop

    "El Bosque Gris. Ni siquiera los cazadores más veteranos del pueblo se adentran demasiado en él después del anochecer."

    doran "Tenemos que seguir moviéndonos. Si esas cosas nos siguieron, no quiero estar aquí parados."

    mira "Mira, allá... un sendero. Puede que nos lleve a alguna parte."

    "Avanzan por el bosque durante lo que parecen horas. El sonido de ramas rotas y criaturas nocturnas no ayuda a calmar los nervios."

    call bosque_gris_exploracion from _call_bosque_exploracion

    # Nota: bosque_gris_exploracion desemboca en combate_jefe_troll,
    # que a su vez maneja las pociones, el puente, y hace jump
    # a casa_bruja_llegada por su cuenta (ver 06_troll_puente.rpy).
    return


label bosque_gris_exploracion:
    # Loop de exploración con encuentros aleatorios.
    # Dos tramos fijos, cada uno dispara un chequeo de encuentro
    # aleatorio antes de continuar. Tras el segundo, llegan al
    # claro donde espera el jefe (Troll del Bosque).

    "Llegan al Sendero de los Robles Caídos."
    call intentar_encuentro_aleatorio("bosque_gris") from _call_encuentro_bosque_1

    if not protagonista.esta_vivo():
        jump combate_derrota

    "Llegan al Claro Silencioso."
    call intentar_encuentro_aleatorio("bosque_gris") from _call_encuentro_bosque_2

    if not protagonista.esta_vivo():
        jump combate_derrota

    "El bosque se abre en un claro extraño, rodeado de ruinas cubiertas de musgo. El camino termina aquí — o alguien se los va a impedir."

    call combate_jefe_troll from _call_jefe_troll

    # A partir de aquí, el guion continúa desde escena_puente,
    # que ya redirige a casa_bruja_llegada por su cuenta.
    return


########################################################
# 4. CASA DE LA BRUJA
########################################################

label casa_bruja_llegada:

    scene bg cabana_bruja_exterior with dissolve

    doran "¿Una cabaña? Aquí, en medio de la nada?"

    mira "No me da buena espina, pero... no tenemos muchas más opciones. Estamos exhaustos."

    menu:
        "¿Qué deciden hacer?"

        "Tocar la puerta y pedir ayuda":
            jump casa_bruja_interior_directo

        "Observar desde lejos antes de acercarse":
            $ protagonista.sumar_rasgo("per", 1)
            "Esperan un momento, atentos a cualquier señal de peligro. No ven nada anormal — solo humo saliendo de la chimenea."
            jump casa_bruja_interior_directo


label casa_bruja_interior_directo:

    scene bg cabana_bruja_interior with fade

    "La puerta cede sin necesidad de tocarla dos veces. Dentro, el calor de una chimenea contrasta con el frío exterior."

    show bruja_personaje at center with dissolve
    bruja "Vaya, vaya... visitantes. No es común que alguien llegue tan lejos en el bosque sin que algo los haya cazado ya."

    doran "Somos del pueblo cercano. Nos atacaron esta noche... goblins, y un ogro."

    bruja "Ah. Eso explica el humo que huelo desde aquí desde hace horas."

    "La bruja los observa con una calma que resulta más inquietante que cualquier amenaza."

    bruja "Pueden quedarse a descansar. Pero nada es gratis en este bosque, queridos... ni siquiera la hospitalidad."

    menu:
        "¿Cómo responde [nombre_protagonista]?"

        "Aceptar sin cuestionar, están demasiado cansados para discutir":
            $ protagonista.sumar_rasgo("vit", 1)
            bruja "Sabia decisión. O quizás solo cansada. Da igual."

        "Preguntar qué es lo que quiere a cambio":
            $ protagonista.sumar_rasgo("inte", 1)
            bruja "Curioso. La mayoría no pregunta hasta que ya es tarde. Me agradas."
            "Sonríe de una forma que no termina de ser reconfortante."

    "Duermen unas horas, los primeros momentos de descanso real desde el ataque."

    jump escape_bruja


########################################################
# 5. ESCAPE DE LA BRUJA
########################################################

label escape_bruja:

    scene bg cabana_bruja_interior night with fade

    "[nombre_protagonista] despierta de golpe. Algo no está bien."

    "A través de una rendija en la puerta de la habitación contigua, ve a la bruja preparando algo sobre una mesa — símbolos, un caldero, ingredientes que no quieres identificar."

    show bruja_personaje at center
    bruja "Tres jóvenes perdidos en mi bosque, justo cuando necesitaba... material fresco. Qué afortunada soy."

    "El corazón se te acelera. No fue hospitalidad. Fue una trampa."

    menu:
        "¿Cómo escapan?"

        "Despiertas a Doran y Mira en silencio, buscando la salida sin hacer ruido":
            $ protagonista.sumar_rasgo("per", 2)
            "Logran moverse sin despertar sospechas... hasta que Mira tropieza con un frasco de vidrio."
            jump escape_bruja_persecucion

        "Los despiertas de golpe y corren hacia la puerta principal":
            $ protagonista.sumar_rasgo("fue", 1)
            "No hay tiempo para sutilezas. Corren."
            jump escape_bruja_persecucion


label escape_bruja_persecucion:

    play sound "sfx/vidrio_roto.ogg"

    show bruja_personaje at center with vpunch
    bruja "¡Oh, no, no, no! ¡No se van a ir así como así, después de todo lo que me costó atraerlos!"

    "La bruja invoca algo — sombras que se retuercen entre los árboles, tomando forma."

    "¡CORRAN!"

    scene bg bosque_noche_persecucion with vpunch
    play music "music/persecucion.ogg" fadein 0.5 loop

    call intentar_encuentro_aleatorio("bosque_gris") from _call_encuentro_persecucion

    "Corren sin mirar atrás, el corazón latiendo con fuerza, las ramas golpeando sus brazos y rostros."

    jump punto_descanso_cueva


########################################################
# PUNTO DE DESCANSO — LA CUEVA DE LOS OTROS ALDEANOS
# ------------------------------------------------------
# Duración de la huida es indefinida (sin contador de días).
# Este es el punto donde el jugador puede optar por quedarse
# más tiempo antes de continuar. Se encuentran rastros de
# otros sobrevivientes de Aldenbrock, sin mostrarlos en
# pantalla — solo objetos que confirman que lograron escapar.
########################################################

label punto_descanso_cueva:

    scene bg cueva_entrada with dissolve
    stop music fadeout 2.0

    "Tras perder de vista a las sombras que los perseguían, el grupo encuentra una grieta en la roca lo bastante grande para ocultarse. Dentro, el silencio es casi un alivio físico."

    "La cueva no está vacía de historia. Hay restos de una fogata ya fría, un pedazo de tela sucia que alguna vez fue una capa de lana teñida del color que usaban en Aldenbrock los días de mercado."

    "Y ahí, apoyada contra la pared: una espada. Sin filo, la hoja mellada por un golpe torpe — pero inconfundible. El sello de la fragua de Bram está grabado en la base, apenas visible bajo el óxido."

    "[nombre_protagonista] la reconoce de inmediato. Su padre la hizo, hace apenas unas semanas, para alguien del pueblo."

    "Quien haya estado aquí, la dejó atrás —tal vez dañada más allá de lo útil, tal vez porque ya no podía cargar con nada más. Pero estuvo aquí. Sobrevivió, al menos hasta este punto."

    if companero_doran.en_party and companero_mira.en_party:
        doran "Eso significa que no fuimos los únicos. Alguien más logró salir de ahí."
        mira "Ojalá eso también signifique que llegaron más lejos que esto."
    elif companero_doran.en_party:
        doran "Mira lo habría reconocido al instante, ella conocía a todos los que compraban en la fragua de tu padre..."
        "El nombre de Mira queda flotando en el aire, un vacío que todavía duele."
    else:
        mira "Doran se habría reído de esto — reconocería esa espada aunque estuviera hecha polvo."
        "El silencio después de decirlo pesa más de lo que esperaban."

    "Deciden descansar ahí esa noche. No hay prisa que valga más que un cuerpo exhausto — el camino que queda todavía es largo."

    jump encuentro_bruja_segunda_vez


########################################################
# SEGUNDO ENCUENTRO CON LA BRUJA (aún no revelada como Arpía)
# ------------------------------------------------------
# Combate OBLIGATORIO de ganar. Reintento inmediato si se
# pierde — no hay checkpoint anterior.
########################################################

init python:

    def crear_bruja_jefe(nivel=10):
        f = nivel / 10.0
        return EnemigoTipado(
            "La Bruja del Bosque", hp=int(160*f), ataque=int(14*f), defensa=int(4*f),
            agilidad=10, exp_otorga=int(110*f), oro_otorga=int(50*f),
            tipo="Sombra", sprite="bruja_personaje", nivel=nivel,
            debil_arma="Impacto", resiste_arma="Punzante"
        )


label encuentro_bruja_segunda_vez:

    scene bg bosque_entrada with fade
    play music "music/tension.ogg" fadein 1.0 loop

    "Al día siguiente, retomando el camino hacia la ciudad, algo se interpone en el sendero — una silueta encorvada, esperándolos con una calma que no debería sentirse tan amenazante."

    show bruja_personaje at center
    bruja "Creyeron que podían simplemente... irse. Qué adorable."

    "No hay escapatoria esta vez. La bruja los había estado buscando todo este tiempo."

    jump combate_jefe_bruja


label combate_jefe_bruja:

    $ bruja_jefe = crear_bruja_jefe(nivel=10)

    call combate([bruja_jefe]) from _call_combate_bruja_jefe

    if not protagonista.esta_vivo():
        "El mundo se oscurece por un instante — pero algo te hace abrir los ojos de nuevo, con otra oportunidad de enfrentarla."
        jump combate_jefe_bruja

    scene bg bosque_entrada with vpunch

    "La bruja retrocede, herida, siseando algo ininteligible antes de desaparecer entre los árboles más densos del bosque."

    bruja "Esto no ha terminado, pequeños insolentes..."

    "Se va sin dar más explicaciones. [nombre_protagonista] no sabe qué fue exactamente lo que enfrentaron, pero algo le dice que no era del todo humano."

    "Sin más obstáculos a la vista, el grupo retoma el camino."

    scene bg bosque_noche_persecucion with dissolve

    "Finalmente, tras lo que parece una eternidad, ven luces a la distancia. Antorchas. Una muralla."

    "Una ciudad."

    jump llegada_ciudad


########################################################
# 6. CIUDAD REFUGIO — misiones y romances
########################################################

label llegada_ciudad:

    scene bg ciudad_puerta_dia with fade
    stop music fadeout 2.0
    play music "music/ciudad_ambiente.ogg" fadein 2.0 loop


    "Ciudadela del Valle Hondo. Nunca habían estado tan lejos de casa."

    show guardia_npc at center
    guardia "¡Alto! ¿Quiénes son y qué...? Espera. ¿Ustedes son del pueblo del herrero, cerca del Bosque Gris?"

    doran "Sí... hubo un ataque. Necesitamos refugio."

    guardia "Por los dioses. No son los primeros en llegar así. Adelante, adelante — hay más gente de su pueblo dentro, en el Refugio del Templo."

    "Entran a la ciudad. El alivio de estar a salvo se mezcla con el peso de no saber qué fue de tantos otros — incluido tu padre."

    jump refugio_templo


label refugio_templo:

    scene bg templo_refugio with dissolve

    "El Templo ha abierto sus puertas como refugio para los sobrevivientes de los ataques recientes. Hay rostros conocidos entre la multitud... y rostros nuevos."

    "Es aquí donde, en los días siguientes, [nombre_protagonista] conoce a quienes marcarán el resto de su historia."

    call inicializar_arco_doran from _call_init_arco_doran

    jump hub_ciudad


########################################################
# HUB DE LA CIUDAD — punto central de misiones secundarias
# ------------------------------------------------------
# Elenco de reclutamiento en la ciudad:
#   - Elyra: romance conocido directamente en el hub (guardia).
#   - Sable: NO aparece en el hub directamente. Se descubre
#     en medio de la cadena de misiones de Theron (ver abajo)
#     — es la "descubierta en medio de una misión".
#   - Theron: se une completando su cadena de misiones (no es
#     romanceable, es reclutamiento puro de party).
#   - Wren: contratable en el Gremio de Aventureros a cambio
#     de oro; se queda permanentemente solo si además
#     completas su cadena de misión personal.
########################################################

label hub_ciudad:

    scene bg ciudad_plaza with fade

    if dias_en_refugio == 0:
        "Los días pasan. La ciudad se convierte, a la fuerza, en un nuevo hogar temporal."
    elif dias_en_refugio == 2 and not escena_callejon_vista:
        # Evento orgánico: ocurre una sola vez, al segundo día en
        # la ciudad, sin ser una opción de menú — el jugador se
        # topa con la escena de camino a la plaza.
        $ escena_callejon_vista = True
        call escena_soldados_fanaticos from _call_callejon
        "Día [dias_en_refugio] de 30 en la Ciudadela del Valle Hondo."
    else:
        "Día [dias_en_refugio] de 30 en la Ciudadela del Valle Hondo."

    menu:
        "¿A quién visita [nombre_protagonista] hoy?"

        "Doran" if companero_doran.en_party:
            call interactuar_doran from _call_interactuar_doran
            jump hub_ciudad

        "Mira" if companero_mira.en_party:
            call interactuar_mira from _call_interactuar_mira
            jump hub_ciudad

        "Elyra — la arquera de la guardia" if not mision_elyra_paso1_hecho:
            jump mision_elyra_paso1

        "Elyra — de nuevo en la muralla" if mision_elyra_paso1_hecho and not mision_elyra_completa:
            jump mision_elyra_paso2

        "Elyra" if mision_elyra_completa:
            call mision_elyra_paso3 from _call_elyra_paso3
            jump hub_ciudad

        "Theron — el erudito de la biblioteca del templo" if not mision_theron_completa:
            jump mision_theron

        "Theron" if mision_theron_completa and companero_theron.en_party:
            call interactuar_theron from _call_interactuar_theron
            jump hub_ciudad

        "Sable" if mision_theron_fase2_completa:
            call visitar_sable_paso2 from _call_sable_paso2
            jump hub_ciudad

        "El Gremio de Aventureros" if not gremio_visitado:
            jump gremio_aventureros

        "Wren" if gremio_visitado and companero_wren is not None and companero_wren.en_party:
            call interactuar_wren from _call_interactuar_wren
            jump hub_ciudad

        "Buscar noticias sobre el compañero perdido" if companero_perdido_id is not None:
            jump mision_recuperar_companero_perdido

        "La herrería de Thrain":
            call visitar_herreria_thrain from _call_thrain
            jump hub_ciudad

        "La biblioteca pública (Lyanwë)":
            call visitar_biblioteca_lyanwe from _call_lyanwe
            jump hub_ciudad

        "El Coliseo":
            call visitar_coliseo from _call_coliseo
            jump hub_ciudad

        "Darle el hacha de Gorrak a Doran" if arma_gorrak_obtenida and not arma_gorrak_dada_a_doran:
            call entregar_hacha_a_doran from _call_entregar_hacha
            jump hub_ciudad

        "Ir a entrenar en el bosque cercano a la ciudad (combate)":
            call intentar_encuentro_aleatorio("camino_ciudad") from _call_encuentro_hub
            $ dias_en_refugio += 1
            jump chequeo_limite_dias

        "Descansar y dejar pasar el día":
            $ dias_en_refugio += 1
            jump chequeo_limite_dias

        "Consultar el Diario":
            call ver_diario from _call_ver_diario
            jump hub_ciudad

        "Continuar la historia (marchar hacia el clímax)" if dias_en_refugio >= 5:
            jump climax_ataque_ciudad

    jump hub_ciudad


label chequeo_limite_dias:
    # El contador de 30 días de la ciudad es estricto: al llegar
    # al límite, la invasión se dispara automáticamente sin
    # importar en qué estado esté el jugador.
    if dias_en_refugio >= 30:
        "Han pasado treinta días desde que llegaron a la Ciudadela del Valle Hondo."
        jump climax_ataque_ciudad
    else:
        jump hub_ciudad


default mision_elyra_completa = False
default mision_elyra_paso1_hecho = False
default mision_theron_completa = False
default mision_theron_fase2_completa = False
default gremio_visitado = False
default mision_wren_completa = False
default dias_en_refugio = 0
default escena_callejon_vista = False


# ---- MISIÓN: ELYRA (romance — se conoce directamente en la ciudad) ----
# Cadena de 2 pasos: primer acercamiento en la muralla, luego
# una segunda visita más personal (fuera de horario de guardia).

label mision_elyra_paso1:
    scene bg muralla_ciudad with dissolve
    show elyra_personaje at center

    elyra "¿Otro refugiado curioseando por la muralla? No es un buen momento, estamos cortos de arqueros."

    "Elyra no baja la guardia mientras habla, los ojos siempre puestos en el horizonte más allá de la muralla."

    menu:
        "¿Cómo interactúa [nombre_protagonista]?"

        "Ofrecerte a ayudar con la guardia":
            $ protagonista.sumar_rasgo("fue", 1)
            call sumar_afinidad_a("elyra", 15) from _call_af_elyra_1
            elyra "¿Ayuda? Ja. Está bien, novato. Veamos si sabes sostener un arco siquiera."
            "Pasan la tarde entrenando puntería. Elyra corrige tu postura sin miramientos, pero cuando por fin aciertas al blanco, deja escapar algo parecido a una sonrisa."
            elyra "No está mal. Para ser de pueblo."

        "Preguntarle sobre la ciudad y su gente":
            call sumar_afinidad_a("elyra", 8) from _call_af_elyra_2
            elyra "Directo al punto, ¿eh? Está bien... te debo una charla, supongo."
            elyra "La Ciudadela ha visto oleadas de refugiados antes. Nunca se acostumbra uno del todo, pero se sobrevive."
            "Habla con una calma práctica, la de alguien que ha visto llegar el mismo miedo en muchos rostros distintos."

    $ mision_elyra_paso1_hecho = True
    $ dias_en_refugio += 1
    jump chequeo_limite_dias


label mision_elyra_paso2:
    scene bg muralla_ciudad night with dissolve

    "Encuentras a Elyra fuera de su turno, sentada en lo alto de la muralla, mirando las luces distantes del bosque."

    show elyra_personaje at center
    elyra "No sueles verme sin el arco encima. Aprovecha, no dura."

    menu:
        "¿De qué habla [nombre_protagonista] con ella?"

        "Preguntarle por qué eligió ser guardia":
            call sumar_afinidad_a("elyra", 15) from _call_af_elyra_3
            elyra "Mi familia murió en un ataque parecido al de tu pueblo, hace años. Decidí que no volvería a quedarme quieta viendo arder algo que quiero proteger."
            "Lo dice sin dramatismo, como quien ya hizo las paces con ello hace tiempo — o como quien ha practicado decirlo así."
            "[nombre_protagonista] entiende ese peso mejor de lo que hubiera querido."

        "Quedarte en silencio, solo acompañándola un rato":
            call sumar_afinidad_a("elyra", 10) from _call_af_elyra_4
            "No dicen nada por un buen rato. A veces no hace falta."
            elyra "...gracias por no llenar el silencio de preguntas. La mayoría no sabe hacer eso."

    $ mision_elyra_completa = True
    $ dias_en_refugio += 1
    jump chequeo_limite_dias


# ---- MISIÓN: THERON (reclutamiento por cadena de misiones) ----
# Fase 2 de esta cadena es donde aparece Sable — no obvia desde el
# principio, lo cual cumple con "la descubres en medio de una misión".
label mision_theron:
    scene bg biblioteca_templo with dissolve
    show theron_personaje at center

    theron "Oh. Hola. No solemos tener visitas por aquí, la biblioteca no es... popular."

    "Está rodeado de pergaminos abiertos y velas casi consumidas — parece llevar ahí más horas de las que admitiría."

    menu:
        "¿Cómo interactúa [nombre_protagonista]?"

        "Mostrarle el libro de runas que encontraste en la fragua":
            $ protagonista.sumar_rasgo("inte", 1)
            theron "Espera... ¿de dónde sacaste esto? Estas runas son... esto es fascinante."
            "Pasan horas juntos, Theron explicando fragmentos de runas antiguas con un entusiasmo genuino que contrasta con su tono apagado de hace un momento."
            theron "Hay alguien más que debería ver esto — una viajera que pasó por aquí hace días decía reconocer símbolos parecidos. La vi por última vez cerca de la taberna."
            theron "No suelo hablar con desconocidos, pero esto... esto vale la excepción."
            jump mision_theron_fase2_sable

        "Preguntar si sabe algo sobre lo que atacó tu pueblo":
            theron "Ogros liderando goblins de forma organizada... eso no es normal. Alguien, o algo, los está dirigiendo."
            theron "He leído sobre grupos que buscan comunicarse con bestias mediante magia prohibida. Historias viejas, se suponía. Empiezo a dudarlo."
            "Theron se queda pensativo, pero no menciona nada más por ahora."
            $ mision_theron_completa = True
            $ dias_en_refugio += 1
            jump chequeo_limite_dias


# ---- FASE 2 DE LA MISIÓN DE THERON: aquí aparece Sable ----
label mision_theron_fase2_sable:

    scene bg taberna_ciudad with dissolve

    "Siguiendo la pista de Theron, [nombre_protagonista] llega a la taberna, buscando a una viajera de la que nadie parece saber demasiado."

    show sable_personaje at center
    sable "¿Buscas a alguien con símbolos raros tatuados en la mente, eh? Vaya forma de presentarte. Soy Sable."

    "No es lo que esperabas encontrar siguiendo el consejo de un bibliotecario — pero ahí está: una mercenaria forastera, con miradas que dicen haber visto más mundo del que deja entrever."

    menu:
        "¿Cómo interactúa [nombre_protagonista] con Sable?"

        "Preguntarle directamente por las runas":
            call sumar_afinidad_a("sable", 15) from _call_af_sable_1
            sable "Directo al grano. Me gusta eso. Sí, las he visto antes... en lugares que preferiría no recordar."
            sable "Cazadora de recompensas, antes mercenaria de guerra. Los símbolos como esos suelen marcar a quienes trabajan con cosas que no deberían tocarse."
            "Sable te cuenta fragmentos de su pasado, a cambio de que le cuentes el tuyo. Un intercambio justo, a su manera."

        "Ser cauteloso, no sabes nada de ella todavía":
            call sumar_afinidad_a("sable", 8) from _call_af_sable_2
            sable "Listo para desconfiar de una desconocida. Sabio. O aburrido. Aún no decido cuál."
            sable "Está bien, guárdate las preguntas. Si cambias de opinión, sigo por aquí una temporada."

    theron "¿La encontraste? Excelente — con su ayuda y las runas del libro, podría llegar a entender de dónde viene todo esto."

    "Con el tiempo, tanto Theron como Sable terminan por acercarse al grupo de refugiados, cada uno a su manera."

    $ mision_theron_completa = True
    $ mision_theron_fase2_completa = True
    $ dias_en_refugio += 1

    python:
        companero_theron.disponible = True
        companero_theron.en_party = True

    "Theron se une oficialmente al grupo."

    jump chequeo_limite_dias


# ---- GREMIO DE AVENTUREROS: Wren, contratable ----
label gremio_aventureros:

    scene bg gremio_aventureros_interior with dissolve

    "El Gremio de Aventureros de la Ciudadela del Valle Hondo — un lugar de paso para mercenarios, cazarrecompensas y curanderos de guerra que venden sus servicios al mejor postor."

    show wren_personaje at center
    wren "¿Buscas contratar ayuda? No vengo barata, pero sé lo que hago. Sanadora de campo, para lo que necesites."

    menu:
        "¿Qué hace [nombre_protagonista]?"

        "Contratarla (cuesta oro)":
            if oro_jugador >= 40:
                $ oro_jugador -= 40
                python:
                    companero_wren.disponible = True
                    companero_wren.en_party = True
                wren "Trato hecho. No te decepcionaré."
                "Wren se une al grupo — al menos, por ahora. Los mercenarios contratados no siempre se quedan para siempre, a menos que encuentren una razón propia para hacerlo."
                jump mision_wren_permanencia
            else:
                wren "Vuelve cuando tengas con qué pagar, novato."
                "No tienes suficiente oro todavía."
                # No se marca gremio_visitado — puede volver a intentarlo
                # más adelante si junta el oro necesario.
                jump hub_ciudad

        "Preguntar por qué trabaja en el gremio":
            wren "Todos tenemos que comer, ¿no? El gremio paga, y paga bien. No hago demasiadas preguntas sobre para quién trabajo después."
            "No parece dispuesta a unirse sin que haya algo de por medio."
            $ gremio_visitado = True
            $ dias_en_refugio += 1
            jump chequeo_limite_dias


# ---- MISIÓN DE PERMANENCIA DE WREN ----
# Si se completa, Wren se queda en la party de forma permanente
# incluso después del Cap. 1. Si no, puede irse más adelante.
label mision_wren_permanencia:

    scene bg enfermeria_templo with dissolve

    wren "Ya que estoy aquí, hay heridos de tu pueblo que necesitan más manos. ¿Me ayudas?"

    menu:
        "¿Cómo responde [nombre_protagonista]?"

        "Quedarte a ayudar con los heridos, sin que te paguen por ello":
            $ protagonista.sumar_rasgo("vol", 1)
            wren "Tienes buenas manos para esto. Y no me extraña ya que no lo hiciste por el oro..."
            "Pasan la tarde atendiendo a otros refugiados. Wren empieza a mirarte distinto — ya no como un simple contrato."
            wren "La mayoría de mis contratos terminan el día que se acaba la paga. Esto... esto es distinto."
            $ mision_wren_completa = True

        "Decir que ya cumpliste con contratarla, que eso no era parte del trato":
            wren "Ja. Justo, supongo. Está bien, un trato es un trato."
            "Wren coopera en combate, pero no parece haber una razón más profunda para quedarse."

    $ gremio_visitado = True
    $ dias_en_refugio += 1
    jump chequeo_limite_dias

########################################################
# 7. CLÍMAX — Ataque a la ciudad y rescate condicionado
# ------------------------------------------------------
# Lógica: se determinan los personajes "salvables" según
# su nivel de afinidad. Solo puedes rescatar a UN número
# limitado (ej. 2) durante el caos, forzando al jugador a
# elegir con base en lo que desarrolló.
########################################################

label climax_ataque_ciudad:

    scene bg ciudad_plaza night with vpunch
    play sound "sfx/alarma_aldea.ogg"
    play music "music/tension.ogg" fadein 0.5 loop

    "Los gritos regresan. Esta vez, no hay escapatoria hacia otro bosque."

    doran "¡[nombre_protagonista]! ¡Son ellos! ¡Los goblins y el ogro nos siguieron hasta aquí!"

    mira "¡No puede ser, cruzamos todo el bosque para esto!"

    scene bg ciudad_incendio with vpunch

    "El caos se apodera de las calles de la Ciudadela del Valle Hondo. La gente corre en todas direcciones. En medio del desastre, [nombre_protagonista] sabe que no podrá ayudar a todos."

    python:
        # Determinar quiénes son "rescatables" según afinidad.
        # Umbral: vinculo_medio o superior (afinidad >= 35) habilita
        # la escena de rescate de ese personaje.
        candidatos_rescate = []
        for id_clave in lista_romances_ids:
            personaje_romance = romances_dict[id_clave]
            if personaje_romance.conocido and personaje_romance.afinidad >= 35:
                candidatos_rescate.append(id_clave)

    if len(candidatos_rescate) == 0:
        jump climax_sin_candidatos
    else:
        jump climax_seleccion_rescate


label climax_sin_candidatos:

    "No conociste lo suficiente a nadie en la ciudad como para saber dónde buscarlos entre el caos. Solo puedes correr, con Doran y Mira, hacia la salida."

    jump climax_final_general


label climax_seleccion_rescate:
    # Solo Elyra y Sable pasan por este sistema de rescate condicionado
    # por afinidad (son los 2 únicos romances). Theron y Wren, si fueron
    # reclutados antes, ya están integrados a la party y se dan por
    # evacuados junto al grupo automáticamente — no requieren rescate.
    #
    # El jugador puede intentar rescatar como máximo a 2 personajes
    # (en este caso, el máximo posible ya que solo hay 2 candidatos).

    $ rescatados = []
    $ intentos_rescate_restantes = 2

    label loop_rescate:

        if intentos_rescate_restantes <= 0 or len(candidatos_rescate) == len(rescatados):
            jump climax_final_general

        "Quedan [intentos_rescate_restantes] oportunidades para intentar un rescate entre el caos."

        menu:
            "¿A quién intenta salvar [nombre_protagonista]?"

            "Ir a buscar a Elyra, en la muralla" if "elyra" in candidatos_rescate and "elyra" not in rescatados:
                $ objetivo_rescate = "elyra"
                jump escena_rescate_individual

            "Ir a buscar a Sable, en la taberna" if "sable" in candidatos_rescate and "sable" not in rescatados:
                $ objetivo_rescate = "sable"
                jump escena_rescate_individual

            "Detenerte aquí y huir con lo que tienes":
                jump climax_final_general


label escena_rescate_individual:

    python:
        rp = romances_dict[objetivo_rescate]
        nivel_af = rp.nivel_afinidad()

    scene bg ciudad_incendio with vpunch

    "[nombre_protagonista] corre entre el fuego y el caos, buscando a [rp.nombre]."

    # El resultado del rescate puede ponderarse por afinidad:
    # vínculo fuerte = rescate limpio; vínculo medio = rescate con complicación
    # (deja espacio para tensión narrativa incluso si "calificó").

    if nivel_af == "vinculo_fuerte":
        call combate([crear_goblin()]) from _call_combate_rescate_fuerte
        if protagonista.esta_vivo():
            "Gracias al vínculo forjado en estos días, [rp.nombre] confía en ti de inmediato y corren juntos hacia la salida."
            python:
                rp.salvado_final_cap1 = True
                rescatados.append(objetivo_rescate)
    else:
        call combate([crear_goblin(), crear_goblin_arquero()]) from _call_combate_rescate_medio
        if protagonista.esta_vivo():
            "El rescate es más caótico de lo esperado — [rp.nombre] duda un instante antes de seguirte, pero logran escapar juntos."
            python:
                rp.salvado_final_cap1 = True
                rescatados.append(objetivo_rescate)

    if not protagonista.esta_vivo():
        jump combate_derrota

    $ intentos_rescate_restantes -= 1
    jump loop_rescate


label climax_final_general:

    scene bg ciudad_puerta_noche_escape with fade

    "Con quienes lograron reunir, [nombre_protagonista] y el resto del grupo alcanzan las puertas traseras de la ciudad, ya medio derrumbadas."

    python:
        nombres_rescatados = [romances_dict[i].nombre for i in rescatados]
        # Theron y Wren, si están en party, evacúan junto al grupo sin
        # pasar por la escena de rescate condicionado (ya son del equipo).
        if companero_theron is not None and companero_theron.en_party:
            nombres_rescatados.append("Theron")
        if companero_wren is not None and companero_wren.en_party:
            nombres_rescatados.append("Wren")

    if nombres_rescatados:
        $ texto_rescatados = ", ".join(nombres_rescatados)
        "Junto a ustedes corren también [texto_rescatados], sobrevivientes de la noche que la Ciudadela del Valle Hondo no olvidará."
    else:
        "Corren solos, sin haber podido llegar a tiempo por nadie más."

    "Pero el camino a la salida no está despejado. Entre ustedes y la puerta trasera, una masa de monstruos se ha reunido — goblins, lobos, criaturas que no deberían estar cerca unas de otras, todas avanzando con la misma disciplina antinatural."

    "Al frente de la horda, una figura envuelta en una capa oscura observa, sin prisa, como quien contempla una obra terminada."

    jump climax_horda_mago_domador


########################################################
# CLÍMAX FINAL — HORDA + MAGO DOMADOR
# ------------------------------------------------------
# Combate en 2 fases: primero la horda (varios enemigos
# reciclados de zonas anteriores), luego el Mago Domador,
# que cambia de tipo elemental a mitad de la segunda fase.
# Si el protagonista aceptó el don de Sombra del viajero
# misterioso en el tutorial, se desbloquean diálogos únicos
# de reconocimiento mutuo.
########################################################

define mago_domador = Character("El Mago Domador", color="#4a3a5c")

init python:

    def crear_horda_climax(nivel=15):
        f = nivel / 15.0
        return [
            EnemigoTipado("Goblin de Guerra", int(35*f), int(10*f), int(4*f), 10, int(0), 0, "Tierra", "goblin", nivel, debil_arma="Corte", resiste_arma="Impacto"),
            EnemigoTipado("Lobo de la Horda", int(25*f), int(9*f), int(3*f), 15, int(0), 0, "Sombra", "lobo", nivel, debil_arma="Impacto", resiste_arma="Punzante"),
            EnemigoTipado("Goblin de Guerra", int(35*f), int(10*f), int(4*f), 10, int(0), 0, "Tierra", "goblin", nivel, debil_arma="Corte", resiste_arma="Impacto"),
        ]

    def crear_mago_domador(nivel=20):
        f = nivel / 20.0
        return EnemigoTipado(
            "El Mago Domador", hp=int(280*f), ataque=int(20*f), defensa=int(8*f),
            agilidad=12, exp_otorga=int(300*f), oro_otorga=int(150*f),
            tipo="Sombra", sprite="mago_domador", nivel=nivel,
            debil_arma="Punzante", resiste_arma="Corte"
        )


label climax_horda_mago_domador:

    scene bg ciudad_incendio with vpunch
    play music "music/jefe_tema.ogg" fadein 1.0 loop

    mago_domador "Vaya, vaya. Cuantos rostros conocidos huyendo de lo inevitable. Ríndanse el favor de no hacerlo más largo de lo necesario."

    doran "¡¿Quién rayos es ese?!"

    "Nadie tiene una respuesta. Solo la certeza de que él sí sabe exactamente quiénes son."

    "FASE 1 — LA HORDA"

    $ horda_climax = crear_horda_climax(nivel=15)
    call combate(horda_climax) from _call_combate_horda_climax

    if not protagonista.esta_vivo():
        jump combate_derrota

    scene bg ciudad_incendio with vpunch

    "Con la horda diezmada, el Mago Domador por fin decide que el espectáculo ha durado suficiente."

    mago_domador "Admirable resistencia. Veamos si sostienen el ritmo un poco más."

    if don_elegido_de_viajero:
        # Diálogo único: reconocimiento mutuo si el protagonista
        # aceptó el don de Sombra del viajero en el tutorial.
        "Algo en la voz del Mago Domador se detiene un instante — como si acabara de reconocer algo."

        mago_domador "...espera. Esa sombra que llevas dentro. La reconozco. Debería — yo mismo te la di."

        "El velo cae de golpe: el viajero de la posada, el que le dio el don esa noche en Aldenbrock, ERA él."

        mago_domador "No esperaba que el don floreciera tan pronto. Ni que volviéramos a encontrarnos así, la verdad."

        menu:
            "¿Qué le responde [nombre_protagonista]?"

            "\"Me usaste. Desde el principio.\"":
                mago_domador "Te di algo real, eso no lo voy a negar como falso. Lo que hagas con ello siempre fue decisión tuya. Hoy, por ejemplo."
                "Su tono no tiene la burla que esperabas — casi suena a que lo dice en serio."

            "\"¿Por qué mi pueblo? ¿Por qué nosotros?\"":
                mago_domador "Eso, querido, es una pregunta para otro día. Si sobrevives a este, tal vez llegues a escuchar la respuesta completa."
                "No es un consuelo. Pero es, al menos, la promesa de que hay una respuesta esperando en algún lado."

    else:
        mago_domador "No preguntas quién soy. Sabio, o simplemente no te importa lo suficiente. Da igual — pronto lo sabrán todos."

    "FASE 2 — EL MAGO DOMADOR"

    "El Mago Domador extiende los brazos, y el aire a su alrededor se retuerce — su energía cambia, inestable, alternando entre distintas naturalezas elementales como quien prueba distintas armas."

    $ mago_domador_enemigo = crear_mago_domador(nivel=20)
    call combate([mago_domador_enemigo]) from _call_combate_mago_domador

    if not protagonista.esta_vivo():
        jump combate_derrota

    scene bg ciudad_incendio with vpunch

    mago_domador "...suficiente. No vine aquí a caer, solo a confirmar algo."

    "Herido, el Mago Domador retrocede, la capa ondeando mientras las sombras a su alrededor lo cubren poco a poco."

    if don_elegido_de_viajero:
        mago_domador "Nos volveremos a ver, [nombre_protagonista]. Ese don que llevas... apenas está despertando."
    else:
        mago_domador "Esto no termina esta noche. No para ustedes. No para mí."

    "Desaparece entre las sombras, dejando tras de sí a la horda diezmada y una ciudad ardiendo."

    jump climax_cierre_capitulo


label climax_cierre_capitulo:

    scene bg ciudad_puerta_noche_escape with fade

    "A la distancia, el fuego consume lo que quedaba de su segundo hogar. El ogro que lideraba el ataque en la aldea original... está aquí también. Esto no es casualidad."

    doran "Esto nos sigue. Nos está buscando a NOSOTROS."

    mira "¿Por qué? ¿Qué querrían de un pueblo de herreros y granjeros?"

    "[nombre_protagonista] no tiene respuesta. Solo la certeza de que esto apenas comienza."

    scene black with fade

    centered "{b}FIN DEL CAPÍTULO 1{/b}\n\n\"La Forja Rota\""

    return
