########################################################
# SISTEMA DE ESTADÍSTICAS (10 RASGOS)
# ------------------------------------------------------
# Diseño: el tutorial narrativo (huida del ataque goblin/ogro)
# presenta situaciones. Cada elección del jugador otorga puntos
# a 1-2 rasgos. Al final del tutorial, los puntos acumulados
# se convierten en los valores iniciales de la ficha.
########################################################

define STAT_MIN = 1
define STAT_MAX = 99
define STAT_CAP_INICIAL = 15   # techo de cualquier stat al salir del tutorial

# ---- Los 10 rasgos ----
# FUE - Fuerza:      daño físico cuerpo a cuerpo
# DEF - Defensa:     reducción de daño físico recibido
# AGI - Agilidad:    orden de turno / evasión
# VIT - Vitalidad:   HP máximo
# INT - Intelecto:   daño y efectividad mágica
# SAB - Sabiduría:   MP máximo / regeneración de maná
# PER - Percepción:  probabilidad de golpe crítico / detectar emboscadas
# SUE - Suerte:      loot, evasión de estados, crítico enemigo reducido
# CAR - Carisma:     afinidad con la party, precios de tienda, diálogos
# VOL - Voluntad:    resistencia a estados alterados (miedo, veneno, etc.)

default persistent.tutorial_completado = False

init python:

    class Personaje(object):
        def __init__(self, nombre, apodo=""):
            self.nombre = nombre
            self.apodo = apodo

            # Rasgos base (se rellenan en el tutorial)
            self.fue = 5
            self.defe = 5
            self.agi = 5
            self.vit = 5
            self.inte = 5
            self.sab = 5
            self.per = 5
            self.sue = 5
            self.car = 5
            self.vol = 5

            self.nivel = 1
            self.exp = 0
            self.exp_siguiente = 100

            self.hp_max = 0
            self.hp = 0
            self.mp_max = 0
            self.mp = 0

            self.armas = []
            self.arma_equipada = None
            self.habilidades = []

            self.recalcular_derivados()

        def recalcular_derivados(self):
            # HP y MP derivan de VIT / SAB, escalando con nivel
            self.hp_max = 20 + (self.vit * 4) + (self.nivel * 5)
            self.mp_max = 10 + (self.sab * 3) + (self.nivel * 2)
            self.hp = min(self.hp, self.hp_max) if self.hp else self.hp_max
            self.mp = min(self.mp, self.mp_max) if self.mp else self.mp_max

        def sumar_rasgo(self, rasgo, cantidad):
            valor_actual = getattr(self, rasgo)
            nuevo = min(valor_actual + cantidad, STAT_MAX)
            setattr(self, rasgo, nuevo)

        def ganar_exp(self, cantidad):
            self.exp += cantidad
            subio = False
            while self.exp >= self.exp_siguiente:
                self.exp -= self.exp_siguiente
                self.subir_nivel()
                subio = True
            return subio

        def subir_nivel(self):
            self.nivel += 1
            self.exp_siguiente = int(self.exp_siguiente * 1.35)
            # Puntos de rasgo para repartir manualmente al subir de nivel
            store.puntos_rasgo_disponibles += 3
            self.recalcular_derivados()
            # cura completa al subir de nivel (estilo JRPG clásico)
            self.hp = self.hp_max
            self.mp = self.mp_max

        def esta_vivo(self):
            return self.hp > 0

        def recibir_dano(self, cantidad):
            self.hp = max(0, self.hp - cantidad)

        def curar(self, cantidad):
            self.hp = min(self.hp_max, self.hp + cantidad)


default puntos_rasgo_disponibles = 0

# Instancia del protagonista, se construye en el tutorial
default protagonista = None
default nombre_protagonista = "Kael"


########################################################
# LABEL: TUTORIAL DE CREACIÓN DE PERSONAJE
# ------------------------------------------------------
# Se ejecuta ANTES del ataque goblin/ogro. Ambientado en
# la herrería de tu padre, un día normal. Cada bloque de
# diálogo con elecciones otorga puntos a rasgos específicos.
########################################################

label tutorial_creacion_personaje:

    scene bg herreria_interior with fade

    "Antes de que el mundo se rompiera, hubo una mañana como cualquier otra."

    "El calor del fragua. El sonido del martillo golpeando metal al rojo vivo. El olor a carbón y sudor."

    show padre_herrero at center
    padre "¡Arriba, holgazán! El sol ya está en lo alto y el pedido del alcalde no se forja solo."

    "Te llamas—"

    $ nombre_protagonista = renpy.input("¿Cómo se llama nuestro protagonista?", default="Kael")
    $ nombre_protagonista = nombre_protagonista.strip() or "Kael"

    $ protagonista = Personaje(nombre_protagonista)

    "[nombre_protagonista], hijo de Bram el herrero, de Aldenbrock. Toda tu vida ha transcurrido entre el yunque y los caminos de tierra de tu aldea."

    # -------------------------------------------------
    # BLOQUE 1: la forja — FUE vs PER
    # -------------------------------------------------
    padre "Toma el martillo. Termina tú esta hoja, ya que tanto insistes en aprender el oficio."

    menu:
        "¿Cómo forjas la hoja?"

        "Con toda tu fuerza, golpes grandes y directos":
            $ protagonista.sumar_rasgo("fue", 3)
            "Golpeas con fuerza bruta. El metal cede rápido, aunque el filo queda un poco irregular."
            padre "Fuerte el brazo... pero la paciencia también se forja, muchacho."

        "Con golpes precisos, estudiando cada ángulo":
            $ protagonista.sumar_rasgo("per", 3)
            "Observas el metal antes de cada golpe, buscando el punto exacto. El trabajo es lento, pero limpio."
            padre "Así se hace. Un buen herrero ve lo que otros no ven."

    # -------------------------------------------------
    # BLOQUE 2: interacción con el pueblo — CAR vs SUE
    # -------------------------------------------------
    scene bg pueblo_dia with dissolve

    "Sales a entregar la espada terminada a la guardia del pueblo."

    show guardia_npc at center
    "Guardia" "Ah, el hijo del herrero. ¿Otra vez huyendo de esa fragua?"

    menu:
        "¿Cómo respondes?"

        "Bromeas y le sacas una sonrisa":
            $ protagonista.sumar_rasgo("car", 3)
            "Guardia" "Ja, tienes la lengua tan afilada como las hojas de tu padre. Toma, esto es tuyo."
            "El guardia te da una moneda extra, de buena gana."

        "Te encoges de hombros y sigues tu camino, atento a todo lo demás":
            $ protagonista.sumar_rasgo("sue", 3)
            "No pierdes el tiempo en charlas. Notas algo brillante entre la paja de un carro cercano: una moneda perdida."
            $ protagonista.sumar_rasgo("sue", 1)
            "La recoges sin que nadie note."

    # -------------------------------------------------
    # BLOQUE 3: entrenamiento improvisado con tus amigos — AGI vs DEF
    # -------------------------------------------------
    scene bg claro_entrenamiento with dissolve

    "Tus amigos [amigo1_nombre] y [amigo2_nombre] te esperan en el claro, como cada tarde, para el entrenamiento con espadas de madera."

    show amigo1 at left
    show amigo2 at right

    "[amigo1_nombre]" "¡Por fin! Prepárate, hoy no pienso dejarte ganar."

    menu:
        "¿Cómo enfrentas el combate de práctica?"

        "Esquivas y te mueves constantemente, buscando aberturas":
            $ protagonista.sumar_rasgo("agi", 3)
            "Te mueves como el agua, esquivando cada golpe con margen de sobra."
            "[amigo2_nombre]" "¡Eh! ¡Deja de moverte tanto y pelea de una vez!"

        "Te plantas firme y bloqueas cada golpe":
            $ protagonista.sumar_rasgo("defe", 3)
            "No retrocedes ni un paso. Cada golpe de madera rebota contra tu guardia."
            "[amigo1_nombre]" "Eres una pared, ¿eh? Está bien, lo admito."

    # -------------------------------------------------
    # BLOQUE 4: un libro viejo en la fragua — INT vs SAB
    # -------------------------------------------------
    scene bg herreria_interior with dissolve

    "De vuelta en casa, encuentras un viejo libro entre las herramientas de tu padre. Está lleno de símbolos extraños, runas casi borradas por el tiempo."

    menu:
        "¿Qué haces con el libro?"

        "Intentas descifrar los símbolos por lógica, comparando patrones":
            $ protagonista.sumar_rasgo("inte", 3)
            "Te concentras en las runas. No entiendes el idioma, pero empiezas a notar patrones repetidos."

        "Cierras los ojos e intentas sentir si el libro 'responde' a algo":
            $ protagonista.sumar_rasgo("sab", 3)
            "Un cosquilleo extraño recorre tus dedos al tocar la portada. Como si el libro reconociera tu tacto."

    padre "¡[nombre_protagonista]! Deja eso donde estaba, no es un juguete."

    "Guardas el libro, pero no olvidas esa sensación."

    # -------------------------------------------------
    # BLOQUE 5: la cena — VOL vs VIT (elección de carácter)
    # -------------------------------------------------
    scene bg herreria_interior with dissolve

    "Esa noche, durante la cena, tu padre te cuenta —como cada tanto— sobre los peligros que rondan más allá de los límites del pueblo."

    show padre_herrero at center
    padre "Dicen que hay más movimiento goblin cerca del Bosque Gris este año. No es normal."

    menu:
        "¿Cómo reaccionas?"

        "Escuchas con calma, decidido a no dejarte intimidar por lo que venga":
            $ protagonista.sumar_rasgo("vol", 3)
            "No es miedo lo que sientes, sino una calma extraña. Sea lo que sea, lo enfrentarás."

        "Terminas tu plato sin preocuparte demasiado, tu cuerpo aguanta cualquier cosa":
            $ protagonista.sumar_rasgo("vit", 3)
            "Nunca has sido de los que se enferman o se cansan fácil. Un poco de peligro no te quita el apetito."

    "Te vas a dormir sin saber que sería la última noche tranquila en mucho tiempo."

    # -------------------------------------------------
    # BLOQUE 6: EL DON ELEMENTAL
    # -------------------------------------------------
    call elegir_tipo_protagonista from _call_tipo_protagonista

    # -------------------------------------------------
    # BLOQUE 7: TIEMPO LIBRE / COMBATE INTRODUCTORIO / ARMAS
    # -------------------------------------------------
    scene bg bosque_entrada day with dissolve

    "Al día siguiente, con el don ya asentado bajo la piel, [nombre_protagonista] aprovecha un rato libre para ir a recoger más madera al bosque cercano — una excusa tan buena como cualquiera para alejarse un rato de la fragua."

    "El bosque, tan cerca del pueblo, siempre se sintió seguro. Hoy, algo entre los árboles no se siente del todo igual."

    call intentar_encuentro_aleatorio("bosque_gris") from _call_encuentro_tutorial

    if not protagonista.esta_vivo():
        jump combate_derrota

    "Un par de goblins, nada que [nombre_protagonista] no pueda manejar solo — pero el simple hecho de que estén tan cerca del pueblo ya es motivo de inquietud."

    scene bg herreria_interior with dissolve

    "De vuelta en la fragua, le cuenta a Bram lo que encontró."

    padre "¿Goblins, tan cerca? No me gusta cómo suena eso."

    "Se queda pensativo un momento, limpiándose las manos en el delantal de cuero."

    padre "Ven acá. Si vas a andar topándote con esas cosas, mejor que lleves algo más que buenas intenciones."

    menu:
        "Bram te pregunta qué tipo de arma prefieres llevar primero"

        "Algo para golpear de cerca, con filo":
            "Bram te entrega una espada recién terminada, el acero todavía frío de haber sido templado hace apenas un día."
            padre "Esta la hice pensando en alguien con tu estilo. Cuídala."

        "Algo para golpear desde lejos":
            "Bram saca de un estante un arma de proyectiles, más ligera que cualquier espada, pero no menos letal en las manos correctas."
            padre "Tu abuelo prefería esto a cualquier espada. Decía que prefería ver venir el peligro antes de tenerlo encima."

    "De cualquier forma, antes de que puedas responder del todo, Bram ya está envolviendo AMBAS armas — la espada y el arma a distancia — en un paño grueso."

    padre "Llévate las dos. Nunca se sabe cuál necesitarás primero."

    python:
        protagonista.armas = ["Espada (Corte)", "Arma a distancia (Proyectil)"]
        protagonista.arma_equipada = "Corte"

    "[nombre_protagonista] guarda ambas armas, sin saber todavía cuán pronto tendría que usarlas de verdad."

    # -------------------------------------------------
    # CIERRE DEL TUTORIAL: asignar puntos restantes libremente
    # -------------------------------------------------
    $ protagonista.recalcular_derivados()

    call pantalla_reparto_libre(puntos=6) from _call_reparto_tutorial

    $ persistent.tutorial_completado = True

    "Con tus rasgos ya definidos por los años vividos en Aldenbrock, la historia está a punto de comenzar."

    return


########################################################
# PANTALLA: reparto libre de puntos de rasgo
# Se usa tanto al final del tutorial como al subir de nivel.
########################################################

label pantalla_reparto_libre(puntos=3):
    $ puntos_rasgo_disponibles += puntos
    call screen reparto_rasgos_screen
    return


screen reparto_rasgos_screen():
    modal True
    zorder 200

    frame:
        align (0.5, 0.5)
        xsize 900
        ysize 620
        padding (30, 30)

        vbox:
            spacing 12

            text "Reparte tus puntos de rasgo" size 34 color "#f0e0b0"
            text "Puntos disponibles: [puntos_rasgo_disponibles]" size 24 color "#ffffff"

            null height 10

            for rasgo, etiqueta in [
                ("fue", "Fuerza"), ("defe", "Defensa"), ("agi", "Agilidad"),
                ("vit", "Vitalidad"), ("inte", "Intelecto"), ("sab", "Sabiduría"),
                ("per", "Percepción"), ("sue", "Suerte"), ("car", "Carisma"), ("vol", "Voluntad")
            ]:
                hbox:
                    spacing 15
                    xsize 820

                    text "[etiqueta]" size 22 xsize 180 color "#dddddd"
                    text "[getattr(protagonista, rasgo)]" size 22 xsize 60 color "#ffdd88"

                    textbutton "-":
                        action If(
                            getattr(protagonista, rasgo) > STAT_MIN,
                            true=[SetField(protagonista, rasgo, getattr(protagonista, rasgo) - 1), SetVariable("puntos_rasgo_disponibles", puntos_rasgo_disponibles + 1)],
                            false=NullAction()
                        )

                    textbutton "+":
                        action If(
                            puntos_rasgo_disponibles > 0,
                            true=[SetField(protagonista, rasgo, getattr(protagonista, rasgo) + 1), SetVariable("puntos_rasgo_disponibles", puntos_rasgo_disponibles - 1)],
                            false=NullAction()
                        )

            null height 20

            textbutton "Confirmar" xalign 0.5:
                action If(
                    puntos_rasgo_disponibles == 0,
                    true=[Function(protagonista.recalcular_derivados), Return()],
                    false=NullAction()
                )
                sensitive (puntos_rasgo_disponibles == 0)
