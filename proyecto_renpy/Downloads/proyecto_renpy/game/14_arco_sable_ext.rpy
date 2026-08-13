########################################################
# ARCO DE SABLE — EXTENSIÓN (PASO 2 + DIARIO)
# ------------------------------------------------------
# El primer encuentro con Sable ya existe en
# 04_chapter1_script.rpy (mision_theron_fase2_sable), usando
# el sistema de afinidad numérica (interes_sable.afinidad),
# necesario para el clímax de rescate. Este archivo agrega
# un segundo paso — más personal — y la función de resumen
# para el Diario.
########################################################

default sable_paso2_disponible = False
default sable_paso2_hecho = False

init python:

    def resumen_diario_sable():
        if not mision_theron_fase2_completa:
            return "Theron mencionó a una viajera con conocimientos sobre runas antiguas, vista cerca de la taberna. Podría valer la pena buscarla."
        elif not sable_paso2_hecho:
            return "Conocí a Sable, una mercenaria forastera con más historia detrás de la que deja ver. Me gustaría saber más, si ella lo permite."
        else:
            return "Sable bajó la guardia conmigo, al menos un poco. No sé cuánto de lo que me contó comparte con alguien más, y eso ya dice algo."
        return ""

    registrar_arco_diario("Sable", resumen_diario_sable)


########################################################
# PASO 2 — la taberna, de noche, sin la excusa de Theron
########################################################

label visitar_sable_paso2:

    if not mision_theron_fase2_completa:
        "Todavía no conoces a Sable."
        return

    scene bg taberna_ciudad night with dissolve
    show sable_personaje at center

    sable "Mira quién decidió venir sin que un bibliotecario lo mande. Siéntate, si quieres. No muerdo, la mayoría de las veces."

    menu:
        "¿De qué hablan?"

        "Preguntarle directamente por su pasado como mercenaria de guerra":
            call sumar_afinidad_a("sable", 18) from _call_af_sable_paso2_a

            sable "Directo, otra vez. Está bien, te lo debo, supongo."

            "Sable cuenta, sin dramatizar ni suavizar, fragmentos de guerras que peleó por dinero, decisiones de las que no está orgullosa, y la razón real por la que terminó viajando sola."

            sable "No busco redención contándote esto, para que quede claro. Solo... hace tiempo que no hablaba de eso con nadie que no fuera a usarlo en mi contra."

        "Simplemente compartir una bebida y dejar que ella dirija la conversación":
            call sumar_afinidad_a("sable", 10) from _call_af_sable_paso2_b

            "Pasan un rato sin agenda particular. Sable habla de lugares que ha visto, sin entrar en detalles demasiado personales, pero con una soltura que sugiere que, a su manera, disfruta la compañía."

            sable "No es común que alguien se quede solo por quedarse. Lo tendré en cuenta."

    $ sable_paso2_hecho = True

    return
