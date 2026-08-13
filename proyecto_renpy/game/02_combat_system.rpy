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
# INVENTARIO DE OBJETOS
# ------------------------------------------------------
# Diccionario simple: nombre del objeto -> cantidad. Los
# efectos de cada objeto están definidos en OBJETOS_INFO.
########################################################

default inventario = {"Poción Menor": 3, "Poción de Maná": 2, "Antídoto": 1}

init python:

    OBJETOS_INFO = {
        "Poción Menor": {
            "descripcion": "Restaura una porción de HP.",
            "tipo": "curacion_hp",
            "cantidad_efecto": 0.4,  # 40% del HP máximo
        },
        "Poción Mayor": {
            "descripcion": "Restaura una gran cantidad de HP.",
            "tipo": "curacion_hp",
            "cantidad_efecto": 0.75,
        },
        "Poción de Maná": {
            "descripcion": "Restaura una porción de MP.",
            "tipo": "curacion_mp",
            "cantidad_efecto": 0.5,
        },
        "Antídoto": {
            "descripcion": "Cura estados de veneno.",
            "tipo": "curar_veneno",
            "cantidad_efecto": 0,
        },
    }

    def agregar_objeto(nombre, cantidad=1):
        inventario[nombre] = inventario.get(nombre, 0) + cantidad

    def usar_objeto_en(nombre_objeto, personaje):
        """Aplica el efecto de un objeto sobre un Personaje/Companero
        y descuenta 1 unidad del inventario. Devuelve un texto
        describiendo el resultado."""
        info = OBJETOS_INFO.get(nombre_objeto)
        if info is None or inventario.get(nombre_objeto, 0) <= 0:
            return None

        inventario[nombre_objeto] -= 1
        if inventario[nombre_objeto] <= 0:
            del inventario[nombre_objeto]

        if info["tipo"] == "curacion_hp":
            cantidad = int(personaje.hp_max * info["cantidad_efecto"])
            personaje.curar(cantidad)
            return f"{personaje.nombre} recupera {cantidad} de HP."
        elif info["tipo"] == "curacion_mp":
            cantidad = int(personaje.mp_max * info["cantidad_efecto"])
            personaje.mp = min(personaje.mp_max, personaje.mp + cantidad)
            return f"{personaje.nombre} recupera {cantidad} de MP."
        elif info["tipo"] == "curar_veneno":
            return f"{personaje.nombre} se cura de cualquier veneno."
        return None


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

                        tipo_enemigo = getattr(objetivo_elegido, "tipo", None)
                        mult_elemento = calcular_multiplicador_tipo(tipo_protagonista, tipo_enemigo) if tipo_enemigo else 1.0

                        dano = max(1, protagonista.fue * 2 - objetivo_elegido.defensa + random.randint(-3, 3))
                        dano = int(dano * mult_arma * mult_elemento)
                        critico = random.random() < (0.05 + protagonista.per * 0.01)
                        if critico:
                            dano = int(dano * 1.8)
                        objetivo_elegido.recibir_dano(dano)

                    if mult_elemento > 1.0:
                        "¡Tu don de [tipo_protagonista] tiene ventaja sobre el tipo [tipo_enemigo] de [objetivo_elegido.nombre]!"
                    elif mult_elemento < 1.0:
                        "El tipo [tipo_enemigo] de [objetivo_elegido.nombre] resiste tu don de [tipo_protagonista]."

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
                if hechizo_elegido["tipo"] == "curacion":
                    call combate_seleccionar_aliado from _call_seleccionar_aliado_magia
                    if aliado_elegido:
                        python:
                            protagonista.mp -= hechizo_elegido["costo"]
                            cantidad_curada = int(aliado_elegido.hp_max * hechizo_elegido["multiplicador"])
                            aliado_elegido.curar(cantidad_curada)
                        "Lanzas [hechizo_elegido['nombre']] sobre [aliado_elegido.nombre]: recupera [cantidad_curada] de HP."
                else:
                    call combate_seleccionar_objetivo from _call_seleccionar_2
                    if objetivo_elegido:
                        python:
                            protagonista.mp -= hechizo_elegido["costo"]
                            tipo_hechizo = hechizo_elegido.get("elemento")
                            tipo_enemigo_magia = getattr(objetivo_elegido, "tipo", None)
                            mult_magia = calcular_multiplicador_tipo(tipo_hechizo, tipo_enemigo_magia) if (tipo_hechizo and tipo_enemigo_magia) else 1.0

                            dano = max(1, int(protagonista.inte * hechizo_elegido["multiplicador"]) - objetivo_elegido.defensa)
                            dano = int(dano * mult_magia)
                            objetivo_elegido.recibir_dano(dano)

                        if mult_magia > 1.0:
                            "¡[hechizo_elegido['nombre']] es especialmente efectivo contra [objetivo_elegido.nombre]!"
                        elif mult_magia < 1.0:
                            "[objetivo_elegido.nombre] resiste parte del daño de [hechizo_elegido['nombre']]."

                        "Lanzas [hechizo_elegido['nombre']] sobre [objetivo_elegido.nombre]: [dano] de daño."

        elif _return == "objeto":
            call combate_menu_objeto from _call_objeto_1
            if objeto_elegido:
                call combate_seleccionar_aliado from _call_seleccionar_aliado_1
                if aliado_elegido:
                    $ resultado_objeto = usar_objeto_en(objeto_elegido, aliado_elegido)
                    if resultado_objeto:
                        "[resultado_objeto]"

        elif _return == "huir":
            python:
                exito_huida = random.random() < (0.3 + protagonista.agi * 0.02)
            if exito_huida:
                "Logras huir del combate."
                $ combate_activo = False
                return
            else:
                "¡No lograste escapar!"

        # ---- Turno de los compañeros en party (automático) ----
        if any(e.esta_vivo() for e in enemigos_actuales):
            python:
                lista_companeros_combate = []
                for comp in [companero_doran, companero_mira, companero_theron, companero_wren]:
                    if comp is not None and comp.en_party and comp.esta_vivo():
                        lista_companeros_combate.append(comp)

                textos_turno_companeros = []
                for comp in lista_companeros_combate:
                    vivos_ahora = [e for e in enemigos_actuales if e.esta_vivo()]
                    if not vivos_ahora:
                        break
                    objetivo_comp = random.choice(vivos_ahora)

                    tipo_arma_comp = getattr(comp, "tipo_arma_equipada", "Corte")
                    debil_comp = getattr(objetivo_comp, "debil_arma", None)
                    resiste_comp = getattr(objetivo_comp, "resiste_arma", None)
                    mult_arma_comp = calcular_multiplicador_arma(tipo_arma_comp, debil_comp, resiste_comp)

                    tipo_enemigo_comp = getattr(objetivo_comp, "tipo", None)
                    mult_elem_comp = calcular_multiplicador_tipo(comp.tipo, tipo_enemigo_comp) if tipo_enemigo_comp else 1.0

                    dano_comp = max(1, comp.fue * 2 - objetivo_comp.defensa + random.randint(-3, 3))
                    dano_comp = int(dano_comp * mult_arma_comp * mult_elem_comp)
                    objetivo_comp.recibir_dano(dano_comp)

                    textos_turno_companeros.append(f"{comp.nombre} ataca a {objetivo_comp.nombre} e inflige {dano_comp} de daño.")

                texto_companeros_unido = "\n".join(textos_turno_companeros)

            if texto_companeros_unido:
                "[texto_companeros_unido]"

        # ---- Turno enemigo ----
        if any(e.esta_vivo() for e in enemigos_actuales):
            python:
                nombres_atacantes = []
                for e in enemigos_actuales:
                    if e.esta_vivo():
                        # Los enemigos reparten su ataque entre todos los
                        # combatientes vivos (protagonista + compañeros),
                        # eligiendo un objetivo al azar cada uno.
                        combatientes_vivos = [protagonista] + [c for c in lista_companeros_combate if c.esta_vivo()]
                        objetivo_enemigo = random.choice(combatientes_vivos)

                        dano_recibido = max(1, e.ataque - objetivo_enemigo.defe + random.randint(-2, 2))
                        objetivo_enemigo.recibir_dano(dano_recibido)
                        nombres_atacantes.append(e.nombre + " ataca a " + objetivo_enemigo.nombre)
                texto_atacantes = ", ".join(nombres_atacantes)

            "[texto_atacantes]."

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


label combate_menu_objeto:
    if not inventario:
        "No tienes objetos en tu inventario."
        $ objeto_elegido = None
        return
    call screen combate_objeto_screen
    $ objeto_elegido = _return
    return


label combate_seleccionar_aliado:
    # Objetos se pueden usar en el protagonista o en cualquier
    # compañero vivo actualmente en la party.
    python:
        aliados_disponibles = [protagonista]
        for comp in [companero_doran, companero_mira, companero_theron, companero_wren]:
            if comp is not None and comp.en_party and comp.esta_vivo():
                aliados_disponibles.append(comp)

    if len(aliados_disponibles) == 1:
        $ aliado_elegido = aliados_disponibles[0]
        return

    call screen combate_seleccion_aliado_screen(aliados_disponibles)
    $ aliado_elegido = _return
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
            spacing 30

            vbox:
                spacing 6
                text "[nombre_protagonista]" size 24 color "#ffffff"
                text "HP: [protagonista.hp]/[protagonista.hp_max]" size 18 color "#ff8888"
                bar value protagonista.hp range protagonista.hp_max xsize 220

                text "MP: [protagonista.mp]/[protagonista.mp_max]" size 18 color "#88aaff"
                bar value protagonista.mp range protagonista.mp_max xsize 220

            vbox:
                spacing 4
                for comp in [companero_doran, companero_mira, companero_theron, companero_wren]:
                    if comp is not None and comp.en_party:
                        if comp.esta_vivo():
                            text "[comp.nombre] — HP: [comp.hp]/[comp.hp_max]" size 16 color "#cceecc"
                        else:
                            text "[comp.nombre] — Derrotado" size 16 color "#886666"

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

    # Lista de hechizos disponibles. El multiplicador para hechizos
    # de daño se aplica sobre Intelecto; los de curación usan un
    # porcentaje de HP máximo del objetivo en vez de dañar.
    python:
        hechizos_disponibles = [
            {"nombre": "Bola de Fuego", "costo": 8, "multiplicador": 1.6, "tipo": "dano", "elemento": "Fuego"},
            {"nombre": "Chispa", "costo": 4, "multiplicador": 0.9, "tipo": "dano", "elemento": "Fuego"},
            {"nombre": "Latigazo de Agua", "costo": 6, "multiplicador": 1.3, "tipo": "dano", "elemento": "Agua"},
            {"nombre": "Golpe de Piedra", "costo": 6, "multiplicador": 1.3, "tipo": "dano", "elemento": "Tierra"},
            {"nombre": "Ráfaga Cortante", "costo": 7, "multiplicador": 1.4, "tipo": "dano", "elemento": "Aire"},
            {"nombre": "Toque de Sombra", "costo": 9, "multiplicador": 1.7, "tipo": "dano", "elemento": "Sombra"},
            {"nombre": "Destello", "costo": 7, "multiplicador": 1.4, "tipo": "dano", "elemento": "Luz"},
            {"nombre": "Curar Heridas", "costo": 10, "multiplicador": 0.5, "tipo": "curacion"},
        ]

    frame:
        align (0.5, 0.5)
        xsize 560
        ysize 500
        padding (20, 20)

        vbox:
            spacing 8
            text "Elige un hechizo (MP: [protagonista.mp])" size 26

            viewport:
                scrollbars "vertical"
                mousewheel True
                xsize 520
                ysize 380

                vbox:
                    spacing 8
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


screen combate_objeto_screen():
    modal True
    zorder 150

    frame:
        align (0.5, 0.5)
        xsize 520
        padding (20, 20)

        vbox:
            spacing 10
            text "Elige un objeto" size 26

            for nombre_obj, cantidad in inventario.items():
                textbutton "[nombre_obj] (x[cantidad]) — [OBJETOS_INFO[nombre_obj]['descripcion']]":
                    action Return(nombre_obj)

            textbutton "Cancelar" action Return(None)


screen combate_seleccion_aliado_screen(aliados_disponibles):
    modal True
    zorder 150

    frame:
        align (0.5, 0.5)
        xsize 500
        padding (20, 20)

        vbox:
            spacing 10
            text "¿A quién se lo das?" size 28

            for aliado in aliados_disponibles:
                textbutton "[aliado.nombre] — HP: [aliado.hp]/[aliado.hp_max]" action Return(aliado)

            textbutton "Cancelar" action Return(None)
