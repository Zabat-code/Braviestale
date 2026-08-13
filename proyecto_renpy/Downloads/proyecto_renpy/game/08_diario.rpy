########################################################
# SISTEMA DE DIARIO / BITÁCORA
# ------------------------------------------------------
# En vez de mostrar números de rango o barras de afinidad,
# cada personaje con arco narrativo tiene una función que
# devuelve una línea de texto describiendo EN PROSA dónde
# quedó ese hilo — de forma que el jugador, tras días sin
# visitar a alguien, recuerde el contexto sin ver un "7/10".
#
# Cada arco de personaje define su propia función
# resumen_diario_<nombre>() que revisa las variables de
# estado de ESE arco y devuelve la línea correspondiente.
# Este archivo solo provee el marco: la pantalla que las
# reúne todas, y el registro de qué funciones existen.
########################################################

init python:

    # Registro de arcos activos: cada entrada es
    # (nombre_mostrado, nombre_funcion_resumen)
    # Se completa a medida que se definen los arcos.
    REGISTRO_ARCOS_DIARIO = []

    def registrar_arco_diario(nombre_mostrado, funcion_resumen):
        REGISTRO_ARCOS_DIARIO.append((nombre_mostrado, funcion_resumen))


label ver_diario:

    call screen diario_screen

    return


screen diario_screen():
    modal True
    zorder 200

    frame:
        align (0.5, 0.5)
        xsize 1000
        ysize 700
        padding (30, 30)

        vbox:
            spacing 16

            text "Diario de [nombre_protagonista]" size 34 color "#f0e0b0"
            text "Día [dias_en_refugio] de 30 en la Ciudadela del Valle Hondo" size 20 color "#aaaaaa"

            null height 10

            viewport:
                scrollbars "vertical"
                mousewheel True
                xsize 940
                ysize 500

                vbox:
                    spacing 20
                    xsize 920

                    for nombre_mostrado, funcion_resumen in REGISTRO_ARCOS_DIARIO:
                        vbox:
                            spacing 4
                            text "[nombre_mostrado]" size 24 color "#e8c987"
                            text "[funcion_resumen()]" size 19 color "#dddddd"

            null height 10

            textbutton "Cerrar" xalign 0.5:
                action Return()
