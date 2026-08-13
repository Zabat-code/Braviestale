########################################################
# SISTEMA DE TIENDAS
# ------------------------------------------------------
# Dos tiendas temáticas:
#   - THRAIN (herrería): mejoras permanentes de daño por
#     tipo de arma (Corte/Punzante/Impacto/Proyectil).
#   - LA BOTICA: pociones y objetos consumibles, incluyendo
#     variedad nueva (Poción Mayor, etc.) más allá de lo que
#     ya existía en el inventario inicial.
########################################################

# ---- Mejoras de arma (bonus de daño plano permanente) ----
default mejoras_arma = {"Corte": 0, "Punzante": 0, "Impacto": 0, "Proyectil": 0}

init python:

    COSTO_BASE_MEJORA = 35       # costo de la primera mejora de un tipo de arma
    INCREMENTO_COSTO_MEJORA = 20  # cada mejora siguiente del mismo tipo cuesta más
    BONUS_POR_MEJORA = 3          # daño plano extra por nivel de mejora

    def costo_siguiente_mejora(tipo_arma):
        nivel_actual = mejoras_arma.get(tipo_arma, 0)
        return COSTO_BASE_MEJORA + (nivel_actual * INCREMENTO_COSTO_MEJORA)

    def comprar_mejora_arma(tipo_arma):
        costo = costo_siguiente_mejora(tipo_arma)
        if oro_jugador >= costo:
            store.oro_jugador -= costo
            mejoras_arma[tipo_arma] = mejoras_arma.get(tipo_arma, 0) + 1
            return True
        return False

    def bonus_dano_arma(tipo_arma):
        return mejoras_arma.get(tipo_arma, 0) * BONUS_POR_MEJORA


########################################################
# CATÁLOGO DE OBJETOS DE LA BOTICA
# ------------------------------------------------------
# Se apoya en OBJETOS_INFO (ya definido en 02_combat_system.rpy)
# para descripciones/efectos, y agrega objetos nuevos ahí mismo
# si no existían todavía.
########################################################

init python:

    # Objetos nuevos que no estaban en el inventario inicial —
    # se agregan al diccionario OBJETOS_INFO ya existente.
    OBJETOS_INFO["Poción Mayor"] = {
        "descripcion": "Restaura una gran cantidad de HP.",
        "tipo": "curacion_hp",
        "cantidad_efecto": 0.75,
    }
    OBJETOS_INFO["Elixir Completo"] = {
        "descripcion": "Restaura todo el HP y MP.",
        "tipo": "curacion_total",
        "cantidad_efecto": 1.0,
    }

    CATALOGO_BOTICA = [
        {"nombre": "Poción Menor", "precio": 12},
        {"nombre": "Poción Mayor", "precio": 30},
        {"nombre": "Poción de Maná", "precio": 15},
        {"nombre": "Antídoto", "precio": 10},
        {"nombre": "Elixir Completo", "precio": 60},
    ]

    def comprar_objeto_botica(nombre_objeto, precio):
        if oro_jugador >= precio:
            store.oro_jugador -= precio
            agregar_objeto(nombre_objeto, 1)
            return True
        return False


# Extiendo usar_objeto_en para soportar "curacion_total" (Elixir).
# Nota: esto redefine la función ya creada en 02_combat_system.rpy,
# agregando el nuevo caso sin romper los anteriores.
init python:

    def usar_objeto_en(nombre_objeto, personaje):
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
        elif info["tipo"] == "curacion_total":
            personaje.hp = personaje.hp_max
            personaje.mp = personaje.mp_max
            return f"{personaje.nombre} recupera todo su HP y MP."
        elif info["tipo"] == "curar_veneno":
            return f"{personaje.nombre} se cura de cualquier veneno."
        return None


########################################################
# LABEL: LA BOTICA
########################################################

define boticaria = Character("Old Nessa", color="#a89060")

label visitar_botica:

    scene bg botica_ciudad with dissolve
    show boticaria_npc at center

    boticaria "Bienvenido a mi tienda, querido. Tengo justo lo que necesitas para no morir por ahí afuera — a buen precio, además."

    jump menu_botica


label menu_botica:

    call screen botica_screen

    if _return == "salir":
        boticaria "Vuelve cuando necesites más. La muerte no espera a que te reabastezcas."
        return
    else:
        jump menu_botica


screen botica_screen():
    modal True
    zorder 150

    frame:
        align (0.5, 0.5)
        xsize 700
        ysize 560
        padding (25, 25)

        vbox:
            spacing 12

            text "La Botica" size 32 color "#e8c987"
            text "Oro disponible: [oro_jugador]" size 22 color "#ffdd88"

            null height 10

            viewport:
                scrollbars "vertical"
                mousewheel True
                xsize 650
                ysize 380

                vbox:
                    spacing 10
                    for item in CATALOGO_BOTICA:
                        hbox:
                            spacing 15
                            xsize 630

                            vbox:
                                xsize 420
                                text "[item['nombre']]" size 22 color "#ffffff"
                                text "[OBJETOS_INFO[item['nombre']]['descripcion']]" size 16 color "#aaaaaa"
                                text "Tienes: [inventario.get(item['nombre'], 0)]" size 14 color "#888888"

                            textbutton "Comprar — [item['precio']] oro":
                                action If(
                                    oro_jugador >= item["precio"],
                                    true=Function(comprar_objeto_botica, item["nombre"], item["precio"]),
                                    false=NullAction()
                                )
                                sensitive (oro_jugador >= item["precio"])

            null height 10

            textbutton "Salir de la tienda" xalign 0.5 action Return("salir")


########################################################
# EXTENSIÓN DE THRAIN — MEJORAS DE ARMA
########################################################

label thrain_ofrecer_mejoras:

    scene bg herreria_ciudad with dissolve
    show thrain at center

    thrain "¿Quieres que le saque más filo o más peso a tu equipo? Puedo reforzarlo, si traes el oro suficiente."

    jump menu_mejoras_thrain


label menu_mejoras_thrain:

    call screen mejoras_arma_screen

    if _return == "salir":
        thrain "Vuelve cuando quieras. El acero no se pule solo."
        return
    else:
        jump menu_mejoras_thrain


screen mejoras_arma_screen():
    modal True
    zorder 150

    frame:
        align (0.5, 0.5)
        xsize 700
        ysize 520
        padding (25, 25)

        vbox:
            spacing 12

            text "Mejoras de Thrain" size 32 color "#e8c987"
            text "Oro disponible: [oro_jugador]" size 22 color "#ffdd88"
            text "Cada mejora aumenta el daño de ese tipo de arma permanentemente." size 16 color "#aaaaaa"

            null height 10

            for tipo_arma in TIPOS_ARMA:
                hbox:
                    spacing 15
                    xsize 630

                    vbox:
                        xsize 420
                        text "[tipo_arma]" size 22 color "#ffffff"
                        text "Nivel actual: [mejoras_arma[tipo_arma]] (+[bonus_dano_arma(tipo_arma)] daño)" size 16 color "#aaaaaa"

                    textbutton "Mejorar — [costo_siguiente_mejora(tipo_arma)] oro":
                        action If(
                            oro_jugador >= costo_siguiente_mejora(tipo_arma),
                            true=Function(comprar_mejora_arma, tipo_arma),
                            false=NullAction()
                        )
                        sensitive (oro_jugador >= costo_siguiente_mejora(tipo_arma))

            null height 15

            textbutton "Salir de la herrería" xalign 0.5 action Return("salir")
