########################################################
# ARCO DE WREN — "NUNCA ME QUEDO, HASTA AHORA"
# ------------------------------------------------------
# Dinámica: Wren mantiene distancia profesional con TODOS
# sus contratos como mecanismo de protección — no es la
# primera vez que se encariña con un grupo y luego tiene que
# irse, o peor, quedarse a verlos morir. El arco profundiza
# esa herida específica sin nombrarla de inmediato, hasta que
# el protagonista gana su confianza con trato genuino (no
# con oro), y ella misma decide, sin que se lo pidan, dejar
# de tratar esto como "solo un contrato más".
########################################################

# Estados:
#   "profesional"  -> trato estrictamente contractual
#   "grietas"      -> deja ver, sin querer, que algo pesa detrás
#   "confesion"    -> comparte por qué nunca se queda
#   "elegido"      -> decide quedarse por elección, no por trato
default estado_arco_wren = "profesional"
default wren_visitas_profesional = 0

init python:

    def resumen_diario_wren():
        if estado_arco_wren == "profesional":
            return "Wren cumple su parte del trato al pie de la letra, ni un paso más. No sé mucho de ella más allá de que es buena en lo suyo."
        elif estado_arco_wren == "grietas":
            return "Hay algo que Wren evita decir sobre por qué nunca se queda mucho tiempo en un mismo grupo. Tal vez si insisto, lo suelte."
        elif estado_arco_wren == "confesion":
            return "Wren me contó por qué mantiene tanta distancia con quienes la contratan. Tiene sentido, aunque sea triste."
        elif estado_arco_wren == "elegido":
            return "Wren decidió quedarse. No por el oro esta vez — por elección propia. Eso significa más de lo que ella misma admite."
        return ""

    registrar_arco_diario("Wren", resumen_diario_wren)


########################################################
# INTERACCIÓN PRINCIPAL — visitar a Wren desde el hub
########################################################

label interactuar_wren:

    if not (companero_wren is not None and companero_wren.en_party):
        "Wren no está disponible por ahora."
        return

    if estado_arco_wren == "profesional":
        jump wren_escena_profesional
    elif estado_arco_wren == "grietas":
        jump wren_escena_grietas
    elif estado_arco_wren == "confesion":
        jump wren_escena_confesion
    else:
        jump wren_escena_elegido


########################################################
# ESTADO: PROFESIONAL
########################################################

label wren_escena_profesional:

    scene bg enfermeria_templo with dissolve
    show wren at center

    $ wren_visitas_profesional += 1

    if wren_visitas_profesional == 1:
        wren "[nombre_protagonista]. ¿Necesitas algo, o solo estás de paso? No es que me moleste, solo prefiero saber qué esperar."

        menu:
            "¿Cómo interactúa [nombre_protagonista]?"

            "Preguntarle si necesita ayuda con algo, sin motivo particular":
                wren "¿Ayuda? Curioso. La mayoría de mis contratos solo aparecen cuando necesitan algo de mí, no al revés."
                "Lo dice sin acusación real, más como una observación distante — pero algo en su mirada sugiere que la tomó nota."

            "Simplemente charlar un rato, sin agenda":
                wren "No estoy acostumbrada a las visitas sin motivo. Pero está bien, supongo. No todos los días alguien 'solo quiere charlar'."
                "Mantiene la conversación cordial, pero cuidadosamente superficial — nada que revele demasiado."

    else:
        wren "De nuevo por aquí, ¿eh? Empiezo a pensar que te gusta molestarme mientras trabajo."
        "Lo dice en tono ligero, casi bromista, aunque la distancia profesional sigue firmemente en su lugar."

        menu:
            "¿[nombre_protagonista] intenta ir más allá de lo superficial?"

            "Preguntarle hace cuánto trabaja como mercenaria":
                wren "Suficiente tiempo como para saber que no vale la pena encariñarse con la gente que contrata mis servicios. Sin ofender."
                "Hay algo automático en la respuesta, como una frase que ha repetido muchas veces, a sí misma más que a nadie más."
                $ estado_arco_wren = "grietas"

            "No presionar, dejarla trabajar en paz":
                "[nombre_protagonista] decide no insistir esta vez. Wren parece agradecerlo, a su manera reservada."

    return


########################################################
# ESTADO: GRIETAS
########################################################

label wren_escena_grietas:

    scene bg enfermeria_templo with dissolve
    show wren at center

    wren "Oye... lo que dije la otra vez, sobre no encariñarme. No fue por ti, quiero decir. Es más una regla general que me hago a mí misma."

    menu:
        "¿Cómo responde [nombre_protagonista]?"

        "Preguntarle qué la llevó a esa regla":
            wren "..."
            "Se queda un momento en silencio, sopesando si vale la pena contarlo."
            wren "Tuve un grupo, antes. Buena gente. Los curé, peleé con ellos, empecé a considerarlos algo más que un contrato. Y entonces un trabajo salió mal, y yo fui la única que volvió."
            "Su voz se mantiene firme, casi demasiado controlada, la forma en que alguien habla de algo que ya ha llorado a solas muchas veces."
            $ estado_arco_wren = "confesion"

        "Decirle que no tiene que explicarse":
            wren "No es que necesite tu permiso para explicarme. Pero... gracias, de todos modos, por no exigirlo."
            "El tema queda sin resolver del todo, aunque algo se suavizó apenas en cómo te mira ahora."

    return


########################################################
# ESTADO: CONFESION — bisagra del arco
########################################################

label wren_escena_confesion:

    scene bg enfermeria_templo with dissolve
    show wren at center

    wren "Desde entonces, cobro por adelantado y no dejo que nadie se acerque más de lo necesario. Es más fácil así. Duele menos, cuando duele menos gente."

    "Lo dice con una claridad práctica que no logra esconder del todo cuánto sigue pesando."

    menu:
        "¿Qué le dice [nombre_protagonista]?"

        "\"No todos los trabajos terminan igual\"":
            wren "Eso espero. De verdad. Pero llevo tiempo diciéndomelo y todavía no me atrevo a apostar por ello del todo."
            "Aun así, hay algo en su expresión que sugiere que, por primera vez en mucho tiempo, quiere creerlo."
            $ estado_arco_wren = "elegido"

        "No decir nada, solo quedarte un rato en silencio con ella":
            "No hay palabras que arreglen lo que Wren cargó todos estos años. [nombre_protagonista] simplemente se queda, sin exigir que ella hable más de lo que ya hizo."
            wren "...gracias por eso. La mayoría llena estos silencios con consejos que no pedí."
            $ estado_arco_wren = "elegido"

    return


########################################################
# ESTADO: ELEGIDO (arco cerrado — Wren decide quedarse por
# elección propia, no por el contrato original)
########################################################

label wren_escena_elegido:

    scene bg enfermeria_templo with dissolve
    show wren at center

    wren "[nombre_protagonista]. Quería decirte algo, antes de que se me pase el valor."

    "Se toma un momento, algo inusual en ella, siempre tan directa."

    wren "Ya cumplí lo que el contrato pedía, hace tiempo. Pero sigo aquí. Y no es por el oro."

    "Es lo más cerca que Wren ha estado de admitir, en voz alta, que este grupo dejó de ser un trabajo para convertirse en algo que decidió proteger por su cuenta."

    wren "No esperes que lo repita seguido, eso sí."

    "Lo dice con media sonrisa, la guardia baja solo un poco — lo suficiente para que se note, no tanto como para sentirse expuesta del todo."

    return
