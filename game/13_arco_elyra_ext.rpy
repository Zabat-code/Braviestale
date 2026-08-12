########################################################
# ARCO DE ELYRA — EXTENSIÓN (PASO 3 + DIARIO)
# ------------------------------------------------------
# Los pasos 1 y 2 ya existen en 04_chapter1_script.rpy
# (mision_elyra_paso1 y mision_elyra_paso2), usando el
# sistema de afinidad numérica (interes_elyra.afinidad),
# necesario para el clímax de rescate. Este archivo agrega
# un tercer paso — más romántico, opcional — y la función
# de resumen para el Diario.
########################################################

default elyra_paso3_disponible = False
default elyra_paso3_hecho = False

init python:

    def resumen_diario_elyra():
        if not mision_elyra_paso1_hecho:
            return "Hay una arquera en la muralla, Elyra, que no parece muy dispuesta a perder el tiempo con refugiados curiosos. Tal vez valga la pena acercarse."
        elif not mision_elyra_completa:
            return "Elyra empieza a bajar la guardia, aunque sigue siendo reservada. Quizás si insisto un poco más, se abra del todo."
        elif not elyra_paso3_hecho:
            return "Elyra me contó por qué eligió ser guardia — perdió a su familia en un ataque como el de mi pueblo. Siento que hay algo más entre nosotros ahora, aunque no lo hemos nombrado."
        else:
            return "Lo que sea que esté pasando entre Elyra y yo, ya no puedo fingir que es solo amistad. No sé bien qué hacer con eso, pero tampoco quiero ignorarlo."
        return ""

    registrar_arco_diario("Elyra", resumen_diario_elyra)


########################################################
# PASO 3 — más allá de la amistad (opcional, romance)
########################################################

label mision_elyra_paso3:

    if not mision_elyra_completa:
        "Todavía no has pasado suficiente tiempo con Elyra para esto."
        return

    scene bg muralla_ciudad night with dissolve
    show elyra_personaje at center

    elyra "Volviste. No sé si debería sorprenderme a estas alturas."

    "Hay algo distinto en cómo te mira esta vez — menos guardia levantada, más pregunta sin formular."

    menu:
        "¿Qué hace [nombre_protagonista]?"

        "Decirle abiertamente que disfruta su compañía, más allá de la amistad":
            $ protagonista.sumar_rasgo("car", 1)
            call sumar_afinidad_a("elyra", 20) from _call_af_elyra_paso3_a

            elyra "..."

            "Se queda callada un momento, algo poco común en ella."

            elyra "No suelo dejar que nadie se acerque tanto. Supongo que ya es tarde para fingir que no lo noté también."

            "Es lo más cerca que Elyra ha estado de admitir algo, y ambos lo saben."

        "Simplemente disfrutar el momento juntos, sin decir nada todavía":
            call sumar_afinidad_a("elyra", 12) from _call_af_elyra_paso3_b

            "No hace falta llenar el silencio con palabras. Se quedan ahí, mirando las luces distantes del bosque, y es suficiente por ahora."

            elyra "...gracias por quedarte. No sueles necesitar razones para eso, ¿verdad?"

    $ elyra_paso3_hecho = True

    return
