########################################################
# SISTEMA DE COMBATE — JRPG CLÁSICO POR TURNOS
# ------------------------------------------------------
# Menú: Atacar / Magia / Objeto / Huir
# Se dispara en "zonas salvajes" (bosque, caminos, etc.)
# mediante encuentros aleatorios (random encounter).
########################################################

init python:

    import random

    class Enemigo(object):
        def __init__(self, nombre, hp, ataque, defensa, agilidad, exp_otorga, oro_otorga, sprite="enemigo_generico"):
            self.nombre = nombre
            self.hp_max = hp
            self.hp = hp
            self.ataque = ataque
            self.defensa = defensa
            self.agilidad = agilidad
            self.exp_otorga = exp_otorga
            self.oro_otorga = oro_otorga
            self.sprite = sprite

        def esta_vivo(self):
            return self.hp > 0

        def recibir_dano(self, cantidad):
            self.hp = max(0, self.hp - cantidad)


    # ---- Plantillas de enemigos de zona ----
    def crear_goblin():
        return Enemigo("Goblin", hp=28, ataque=7, defensa=3, agilidad=9, exp_otorga=18, oro_otorga=12, sprite="goblin")

    def crear_goblin_arquero():
        return Enemigo("Goblin Arquero", hp=20, ataque=9, defensa=1, agilidad=11, exp_otorga=20, oro_otorga=14, sprite="goblin_arquero")

    def crear_ogro():
        return Enemigo("Ogro", hp=70, ataque=15, defensa=6, agilidad=3, exp_otorga=55, oro_otorga=40, sprite="ogro")

    def crear_lobo_salvaje():
        return Enemigo("Lobo Salvaje", hp=18, ataque=6, defensa=2, agilidad=14, exp_otorga=12, oro_otorga=6, sprite="lobo")

    def crear_bandido():
        return Enemigo("Bandido", hp=32, ataque=8, defensa=4, agilidad=8, exp_otorga=22, oro_otorga=25, sprite="bandido")


    # Tablas de encuentro por zona (se usan con random.choice / weighted)
    TABLA_ENCUENTROS = {
        "bosque_gris": [
            (crear_goblin, 45),
            (crear_goblin_arquero, 25),
            (crear_lobo_salvaje, 25),
            (crear_ogro, 5),
        ],
        "camino_ciudad": [
            (crear_bandido, 50),
            (crear_lobo_salvaje, 35),
            (crear_goblin, 15),
        ],
    }

    def tirar_encuentro(zona):
        tabla = TABLA_ENCUENTROS.get(zona, [(crear_goblin, 100)])
        poblacion = [t[0] for t in tabla]
        pesos = [t[1] for t in tabla]
        elegido = random.choices(poblacion, weights=pesos, k=1)[0]
        return elegido()

    def probabilidad_encuentro_aleatorio(pasos_sin_combate, base=0.12):
        # Sube la probabilidad mientras más pasos pasan sin encuentro,
        # para evitar rachas largas sin combate (pity system simple).
        return min(0.6, base + (pasos_sin_combate * 0.03))


default pasos_sin_combate = 0
default combate_activo = False
default enemigos_actuales = []
default log_combate = []
default oro_jugador = 30


########################################################
# LABEL: disparador de encuentro aleatorio al explorar
# Se llama desde las pantallas de "zona salvaje" (bosque, camino)
########################################################

label intentar_encuentro_aleatorio(zona="bosque_gris"):
    python:
        prob = probabilidad_encuentro_aleatorio(pasos_sin_combate)
        disparado = random.random() < prob

    if disparado:
        $ pasos_sin_combate = 0
        $ enemigo = tirar_encuentro(zona)
        call combate([enemigo]) from _call_combate_random
    else:
        $ pasos_sin_combate += 1

    return


########################################################
# LABEL: combate principal
# Recibe una lista de objetos Enemigo
########################################################

label combate(lista_enemigos):
    $ enemigos_actuales = lista_enemigos
    $ combate_activo = True
    $ log_combate = []

    scene bg combate_generico with vpunch

    play sound "sfx/combate_inicio.ogg"

    "¡Un enemigo aparece en tu camino!"

    $ nombres = ", ".join([e.nombre for e in enemigos_actuales])
    "[nombres] se interpone entre tú y el camino."

    label loop_turno_jugador:

        if not protagonista.esta_vivo():
            jump combate_derrota

        if all(not e.esta_vivo() for e in enemigos_actuales):
            jump combate_victoria

        call screen combate_hud

        if _return == "atacar":
            call combate_menu_arma from _call_arma_1
            if arma_elegida:
                call combate_seleccionar_objetivo from _call_seleccionar_1
                if objetivo_elegido:
                    python:
                        debil = getattr(objetivo_elegido, "debil_arma", None)
                        resiste = getattr(objetivo_elegido, "resiste_arma", None)
                        mult_arma = calcular_multiplicador_arma(arma_elegida, debil, resiste)

                        dano = max(1, protagonista.fue * 2 - objetivo_elegido.defensa + random.randint(-3, 3))
                        dano = int(dano * mult_arma)
                        critico = random.random() < (0.05 + protagonista.per * 0.01)
                        if critico:
                            dano = int(dano * 1.8)
                        objetivo_elegido.recibir_dano(dano)

                    if mult_arma > 1.0:
                        "¡[objetivo_elegido.nombre] es vulnerable a armas de tipo [arma_elegida]!"
                    elif mult_arma < 1.0:
                        "[objetivo_elegido.nombre] resiste el daño de armas de tipo [arma_elegida]."

                    if critico:
                        "¡Golpe crítico! Infliges [dano] de daño a [objetivo_elegido.nombre]."
                    else:
                        "Atacas a [objetivo_elegido.nombre] e infliges [dano] de daño."

        elif _return == "magia":
            call combate_menu_magia from _call_magia_1
            if hechizo_elegido:
                call combate_seleccionar_objetivo from _call_seleccionar_2
                if objetivo_elegido:
                    python:
                        protagonista.mp -= hechizo_elegido["costo"]
                        dano = max(1, int(protagonista.inte * hechizo_elegido["multiplicador"]) - objetivo_elegido.defensa)
                        objetivo_elegido.recibir_dano(dano)
                    "Lanzas [hechizo_elegido['nombre']] sobre [objetivo_elegido.nombre]: [dano] de daño."

        elif _return == "objeto":
            "(Aquí se conecta el inventario — usar poción, etc.)"

        elif _return == "huir":
            python:
                exito_huida = random.random() < (0.3 + protagonista.agi * 0.02)
            if exito_huida:
                "Logras huir del combate."
                $ combate_activo = False
                return
            else:
                "¡No lograste escapar!"

        # ---- Turno enemigo ----
        if any(e.esta_vivo() for e in enemigos_actuales):
            python:
                nombres_atacantes = []
                for e in enemigos_actuales:
                    if e.esta_vivo():
                        dano_recibido = max(1, e.ataque - protagonista.defe + random.randint(-2, 2))
                        protagonista.recibir_dano(dano_recibido)
                        nombres_atacantes.append(e.nombre)
                texto_atacantes = ", ".join(nombres_atacantes)

            "[texto_atacantes] te ataca. Recibes daño."

        jump loop_turno_jugador

    return


label combate_seleccionar_objetivo:
    $ vivos = [e for e in enemigos_actuales if e.esta_vivo()]
    if len(vivos) == 1:
        $ objetivo_elegido = vivos[0]
        return
    call screen combate_seleccion_objetivo_screen(vivos)
    $ objetivo_elegido = _return
    return


label combate_menu_magia:
    if protagonista.mp < 5:
        "No tienes suficiente maná para lanzar hechizos."
        $ hechizo_elegido = None
        return
    call screen combate_magia_screen
    $ hechizo_elegido = _return
    return


label combate_menu_arma:
    # El protagonista siempre tiene acceso a los 4 tipos de arma
    # en combate (a diferencia de los compañeros, que tienen un
    # tipo_arma_equipada fijo). Selecciona el tipo antes de
    # elegir objetivo.
    call screen combate_arma_screen
    $ arma_elegida = _return
    return


label combate_victoria:
    $ combate_activo = False
    play sound "sfx/victoria.ogg"

    python:
        exp_total = sum(e.exp_otorga for e in enemigos_actuales)
        oro_total = sum(e.oro_otorga for e in enemigos_actuales)
        oro_jugador += oro_total
        subio_nivel = protagonista.ganar_exp(exp_total)

    "¡Victoria! Ganas [exp_total] puntos de experiencia y [oro_total] monedas de oro."

    if subio_nivel:
        play sound "sfx/subir_nivel.ogg"
        "¡[nombre_protagonista] ha subido de nivel! Ahora es nivel [protagonista.nivel]."
        call pantalla_reparto_libre(puntos=0) from _call_reparto_subida

    return


label combate_derrota:
    $ combate_activo = False
    scene bg pantalla_derrota with fade
    "Todo se vuelve oscuro. [nombre_protagonista] cae ante el enemigo..."
    "(Aquí se define el flujo de Game Over o reintento, según el diseño del capítulo)"
    return


########################################################
# PANTALLAS DE COMBATE (HUD, menú de magia, objetivo)
########################################################

screen combate_hud():
    zorder 100

    frame:
        align (0.5, 1.0)
        yoffset -20
        xsize 1100
        ysize 260
        padding (20, 20)

        hbox:
            spacing 40

            vbox:
                spacing 6
                text "[nombre_protagonista]" size 26 color "#ffffff"
                text "HP: [protagonista.hp]/[protagonista.hp_max]" size 20 color "#ff8888"
                bar value protagonista.hp range protagonista.hp_max xsize 260

                text "MP: [protagonista.mp]/[protagonista.mp_max]" size 20 color "#88aaff"
                bar value protagonista.mp range protagonista.mp_max xsize 260

            vbox:
                spacing 6
                for e in enemigos_actuales:
                    if e.esta_vivo():
                        text "[e.nombre] — HP: [e.hp]/[e.hp_max]" size 20 color "#ffdddd"

            vbox:
                spacing 10
                textbutton "Atacar" action Return("atacar")
                textbutton "Magia" action Return("magia")
                textbutton "Objeto" action Return("objeto")
                textbutton "Huir" action Return("huir")


screen combate_seleccion_objetivo_screen(vivos):
    modal True
    zorder 150

    frame:
        align (0.5, 0.5)
        xsize 500
        padding (20, 20)

        vbox:
            spacing 10
            text "Elige un objetivo" size 28

            for e in vivos:
                textbutton "[e.nombre] (HP [e.hp])" action Return(e)


screen combate_magia_screen():
    modal True
    zorder 150

    # Lista de hechizos de ejemplo — ajustar según diseño de habilidades
    python:
        hechizos_disponibles = [
            {"nombre": "Bola de Fuego", "costo": 8, "multiplicador": 1.6},
            {"nombre": "Chispa", "costo": 4, "multiplicador": 0.9},
        ]

    frame:
        align (0.5, 0.5)
        xsize 500
        padding (20, 20)

        vbox:
            spacing 10
            text "Elige un hechizo (MP: [protagonista.mp])" size 26

            for h in hechizos_disponibles:
                textbutton "[h['nombre']] — Costo: [h['costo']] MP":
                    action If(protagonista.mp >= h["costo"], true=Return(h), false=NullAction())
                    sensitive (protagonista.mp >= h["costo"])

            textbutton "Cancelar" action Return(None)


screen combate_arma_screen():
    modal True
    zorder 150

    frame:
        align (0.5, 0.5)
        xsize 500
        padding (20, 20)

        vbox:
            spacing 10
            text "Elige tu tipo de arma" size 26

            for tipo_arma in TIPOS_ARMA:
                textbutton "[tipo_arma]" action Return(tipo_arma)

            textbutton "Cancelar" action Return(None)
