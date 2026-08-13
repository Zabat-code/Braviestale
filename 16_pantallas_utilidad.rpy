########################################################
# PANTALLA: ESTADO DEL PERSONAJE
# ------------------------------------------------------
# Muestra los 10 rasgos, nivel, HP/MP, arma equipada y tipo
# elemental del protagonista, fuera de combate.
########################################################

label ver_estado_personaje:
    call screen estado_personaje_screen
    return


screen estado_personaje_screen():
    modal True
    zorder 200

    frame:
        align (0.5, 0.5)
        xsize 900
        ysize 680
        padding (30, 30)

        vbox:
            spacing 10

            text "[nombre_protagonista]" size 34 color "#f0e0b0"
            text "Nivel [protagonista.nivel] — EXP [protagonista.exp]/[protagonista.exp_siguiente]" size 20 color "#cccccc"
            text "Don elemental: [tipo_protagonista]" size 20 color "#88ccff"

            null height 8

            hbox:
                spacing 40

                vbox:
                    spacing 4
                    text "HP: [protagonista.hp]/[protagonista.hp_max]" size 20 color "#ff8888"
                    bar value protagonista.hp range protagonista.hp_max xsize 300

                vbox:
                    spacing 4
                    text "MP: [protagonista.mp]/[protagonista.mp_max]" size 20 color "#88aaff"
                    bar value protagonista.mp range protagonista.mp_max xsize 300

            null height 15

            text "Rasgos" size 26 color "#f0e0b0"

            grid 2 5:
                spacing 8
                xsize 840

                for etiqueta, valor in [
                    ("Fuerza", protagonista.fue), ("Defensa", protagonista.defe),
                    ("Agilidad", protagonista.agi), ("Vitalidad", protagonista.vit),
                    ("Intelecto", protagonista.inte), ("Sabiduría", protagonista.sab),
                    ("Percepción", protagonista.per), ("Suerte", protagonista.sue),
                    ("Carisma", protagonista.car), ("Voluntad", protagonista.vol),
                ]:
                    hbox:
                        xsize 410
                        spacing 10
                        text "[etiqueta]:" size 19 color "#dddddd" xsize 160
                        text "[valor]" size 19 color "#ffdd88"

            null height 15

            text "Mejoras de arma" size 26 color "#f0e0b0"
            hbox:
                spacing 25
                for tipo_arma in TIPOS_ARMA:
                    text "[tipo_arma]: +[bonus_dano_arma(tipo_arma)]" size 18 color "#cceecc"

            null height 15

            textbutton "Cerrar" xalign 0.5 action Return()


########################################################
# PANTALLA: INVENTARIO (fuera de combate)
# ------------------------------------------------------
# Permite ver y usar objetos sin estar en batalla — útil
# para curarse antes de un jefe, por ejemplo.
########################################################

label ver_inventario:
    call screen inventario_screen
    return


screen inventario_screen():
    modal True
    zorder 200

    frame:
        align (0.5, 0.5)
        xsize 700
        ysize 560
        padding (25, 25)

        vbox:
            spacing 12

            text "Inventario" size 32 color "#e8c987"

            null height 6

            if not inventario:
                text "No tienes objetos." size 20 color "#aaaaaa"
            else:
                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    xsize 650
                    ysize 400

                    vbox:
                        spacing 10
                        for nombre_obj, cantidad in inventario.items():
                            hbox:
                                spacing 15
                                xsize 630

                                vbox:
                                    xsize 420
                                    text "[nombre_obj] (x[cantidad])" size 21 color "#ffffff"
                                    text "[OBJETOS_INFO[nombre_obj]['descripcion']]" size 15 color "#aaaaaa"

                                textbutton "Usar":
                                    action Return(nombre_obj)

            null height 10
            textbutton "Cerrar" xalign 0.5 action Return(None)


label usar_objeto_fuera_de_combate:
    call screen inventario_screen
    $ objeto_a_usar = _return

    if objeto_a_usar:
        python:
            aliados_disponibles_fc = [protagonista]
            for comp in [companero_doran, companero_mira, companero_theron, companero_wren]:
                if comp is not None and comp.en_party and comp.esta_vivo():
                    aliados_disponibles_fc.append(comp)

        call screen combate_seleccion_aliado_screen(aliados_disponibles_fc)
        $ aliado_para_objeto = _return

        if aliado_para_objeto:
            $ resultado_uso = usar_objeto_en(objeto_a_usar, aliado_para_objeto)
            if resultado_uso:
                "[resultado_uso]"

    return


########################################################
# PANTALLA: PARTY
# ------------------------------------------------------
# Vista conjunta de todos los compañeros reclutados, su HP
# actual, y su tipo. Complementa al Diario (que muestra el
# arco narrativo en prosa) con el estado mecánico.
########################################################

label ver_party:
    call screen party_screen
    return


screen party_screen():
    modal True
    zorder 200

    frame:
        align (0.5, 0.5)
        xsize 900
        ysize 640
        padding (30, 30)

        vbox:
            spacing 14

            text "Tu Grupo" size 34 color "#f0e0b0"

            null height 6

            viewport:
                scrollbars "vertical"
                mousewheel True
                xsize 840
                ysize 480

                vbox:
                    spacing 16

                    # Protagonista siempre presente
                    frame:
                        xsize 820
                        padding (15, 12)
                        vbox:
                            spacing 4
                            text "[nombre_protagonista] (tú)" size 24 color "#ffdd88"
                            text "Nivel [protagonista.nivel] — Don: [tipo_protagonista]" size 17 color "#cccccc"
                            text "HP: [protagonista.hp]/[protagonista.hp_max]  |  MP: [protagonista.mp]/[protagonista.mp_max]" size 17 color "#dddddd"

                    for comp in [companero_doran, companero_mira, companero_theron, companero_wren]:
                        if comp is not None and comp.en_party:
                            frame:
                                xsize 820
                                padding (15, 12)
                                vbox:
                                    spacing 4
                                    text "[comp.nombre]" size 24 color "#cceecc"
                                    text "Nivel [comp.nivel] — Tipo: [comp.tipo] — Arma: [comp.tipo_arma_equipada]" size 17 color "#cccccc"
                                    if comp.esta_vivo():
                                        text "HP: [comp.hp]/[comp.hp_max]  |  MP: [comp.mp]/[comp.mp_max]" size 17 color "#dddddd"
                                    else:
                                        text "Derrotado — necesita curación" size 17 color "#cc8888"

                    if companero_perdido_id is not None:
                        frame:
                            xsize 820
                            padding (15, 12)
                            $ nombre_perdido_party = "Doran" if companero_perdido_id == "doran" else "Mira"
                            text "[nombre_perdido_party] — Separado del grupo" size 22 color "#886666"

            null height 10
            textbutton "Cerrar" xalign 0.5 action Return()


########################################################
# SISTEMA DE GUARDADO AUTOMÁTICO ANTES DE JEFES
# ------------------------------------------------------
# Guarda en un slot dedicado justo antes de cada combate de
# jefe obligatorio, para que el jugador pueda recuperar el
# progreso si cierra el juego tras una derrota o accidente.
########################################################

label guardado_automatico_previo_jefe(nombre_jefe="jefe"):
    $ nombre_slot_auto = "auto-" + nombre_jefe
    $ renpy.save(nombre_slot_auto, extra_info="Antes de " + nombre_jefe)
    return
