########################################################
# PERSONAJES Y ELENCO DE PARTY (6 personajes jugables)
# ------------------------------------------------------
# Estructura del elenco:
#   1-2. Doran y Mira   — por defecto, amigos de la aldea.
#        Uno de los dos se separa en la persecución del bosque
#        (ver 06_troll_puente.rpy) y se recupera después con
#        una misión de aldeano.
#   3-4. Dos personajes que se UNEN completando sus misiones
#        en la ciudad (uno de ellos es romanceable: la
#        "descubierta en medio de una misión").
#   5.   Un personaje CONTRATABLE en el Gremio de Aventureros
#        (paga por unirse; se queda permanentemente si además
#        completas su cadena de misión personal).
#   6.   El segundo romance: conocido directamente en la ciudad
#        (no requiere gremio ni misión oculta para aparecer).
#
# De los 6, SOLO 2 son romanceables:
#   - Uno se conoce en la ciudad (interacción directa, hub).
#   - Otra se descubre en medio de una misión (no es obvio
#     desde el principio que es reclutable/romanceable).
########################################################

# ---- Definición de los Character() de RenPy ----
define kael = Character("[nombre_protagonista]", color="#e8c987")
define padre = Character("Bram", color="#a9866b")
define narrador = Character(None, kind=nvl)

define doran = Character("Doran", color="#8fb996")
define mira = Character("Mira", color="#d98fb9")
define bruja = Character("La Bruja del Bosque", color="#9b6bd6")
define guardia = Character("Guardia", color="#7a7a7a")

# ---- Los 2 interés románticos (de los 6 personajes de party) ----
define elyra = Character("Elyra", color="#f2a65a")     # conocida en la ciudad (hub directo)
define sable = Character("Sable", color="#c75a5a")     # descubierta en medio de una misión

# ---- Personajes de party no romanceables ----
define theron = Character("Theron", color="#5aa9f2")   # se une completando su cadena de misiones
define wren = Character("Wren", color="#5ac788")       # contratable en el Gremio de Aventureros


init python:

    class InteresRomantico(object):
        def __init__(self, id_clave, nombre):
            self.id_clave = id_clave
            self.nombre = nombre
            self.afinidad = 0          # 0 a 100
            self.conocido = False      # ¿el jugador ya interactuó con este personaje?
            self.salvado_final_cap1 = None  # se define en el clímax

        def sumar_afinidad(self, cantidad):
            self.conocido = True
            self.afinidad = max(0, min(100, self.afinidad + cantidad))

        def nivel_afinidad(self):
            if self.afinidad >= 70:
                return "vinculo_fuerte"
            elif self.afinidad >= 35:
                return "vinculo_medio"
            elif self.afinidad > 0:
                return "vinculo_leve"
            else:
                return "desconocido"


default interes_elyra = None
default interes_sable = None

# Solo 2 romances ahora (antes eran 4)
default lista_romances_ids = ["elyra", "sable"]


label inicializar_romances:
    python:
        interes_elyra = InteresRomantico("elyra", "Elyra")
        interes_sable = InteresRomantico("sable", "Sable")

        romances_dict = {
            "elyra": interes_elyra,
            "sable": interes_sable,
        }
    return


# Helper para sumar afinidad desde cualquier parte del guion
label sumar_afinidad_a(id_clave, cantidad):
    $ romances_dict[id_clave].sumar_afinidad(cantidad)
    return


########################################################
# CLASE COMPAÑERO — miembros de party jugables
########################################################

init python:

    class Companero(Personaje):
        """Extiende Personaje para los 6 miembros de party jugables."""
        def __init__(self, nombre, fue, defe, agi, vit, inte, sab, per, sue, car, vol, tipo="Tierra"):
            Personaje.__init__(self, nombre)
            self.fue, self.defe, self.agi = fue, defe, agi
            self.vit, self.inte, self.sab = vit, inte, sab
            self.per, self.sue, self.car, self.vol = per, sue, car, vol
            self.tipo = tipo
            self.en_party = False       # ¿está actualmente en el grupo activo?
            self.disponible = False     # ¿ya fue reclutado/desbloqueado?
            self.tipo_arma_equipada = "Corte"  # tipo de arma que porta este compañero (fijo salvo evento especial)
            self.recalcular_derivados()
            self.hp = self.hp_max
            self.mp = self.mp_max


# ---- Los 6 personajes jugables ----
default companero_doran = None    # por defecto — tipo Piedra (Tierra)
default companero_mira = None     # por defecto — tipo Agua
default companero_theron = None   # se une por cadena de misiones
default companero_wren = None     # contratable en el Gremio de Aventureros
default companero_elyra_pj = None # romance 1 — ciudad
default companero_sable_pj = None # romance 2 — descubierta en misión

# Estado de la separación Doran/Mira en la persecución (ver 06_troll_puente.rpy)
default companero_perdido_id = None    # "doran" o "mira": quién se separó
default companero_recuperado = False   # ¿ya se completó la misión de rescate?


label crear_party_inicial:
    python:
        companero_doran = Companero(
            "Doran", fue=9, defe=8, agi=4, vit=8, inte=2, sab=2, per=4, sue=3, car=5, vol=6,
            tipo="Tierra"
        )
        companero_mira = Companero(
            "Mira", fue=3, defe=3, agi=7, vit=4, inte=9, sab=8, per=6, sue=4, car=6, vol=4,
            tipo="Agua"
        )
        companero_doran.en_party = True
        companero_doran.disponible = True
        companero_mira.en_party = True
        companero_mira.disponible = True
    return


########################################################
# TIPO ELEMENTAL DEL PROTAGONISTA
# ------------------------------------------------------
# Elección explícita durante el tutorial. Doran ya es
# Piedra y Mira ya es Agua, así que el protagonista elige
# entre los 3 tipos restantes para no solaparse con ellos.
########################################################

default tipo_protagonista = None

########################################################
# EL DON ELEMENTAL — ELECCIÓN DEL TIPO DEL PROTAGONISTA
# ------------------------------------------------------
# En este mundo, algunos nacen con un elemento; otros deben
# recibir la bendición de un don de quien ya lo posee. El
# protagonista llega a la edad de elegir esa misma noche.
# Solo se obtiene UN don, fijo de ahí en adelante.
########################################################

define director_escuela = Character("Director Aldric", color="#8a9bb0")
define sacerdote_iglesia = Character("Hermana Ysolde", color="#e8d9a0")
define viajero_misterioso = Character("El Viajero", color="#5a4a6b")

default tipo_protagonista = None
default don_elegido_de_viajero = False  # marca si el don vino del viajero (= Mago Domador)


label elegir_tipo_protagonista:

    scene bg herreria_interior night with dissolve

    padre "[nombre_protagonista], ya tienes edad de recibir tu don. Todo el que vive en Aldenbrock lo recibe, tarde o temprano, de alguien que ya lo posee."

    padre "Yo puedo dártelo esta misma noche, si es fuego lo que quieres llevar contigo. Pero también está el Director de la escuela, o la Hermana Ysolde en la iglesia... y dicen que hay un viajero de paso por el pueblo, aunque de él sé poco y nada."

    "Es una decisión que se supone debería tomarse con calma, con tiempo. [nombre_protagonista] no tiene ese lujo del todo — pero tampoco quiere decidir a la ligera."

    menu:
        "¿A quién acude [nombre_protagonista] por su don?"

        "Pedírselo a tu propio padre — FUEGO":
            $ tipo_protagonista = "Fuego"
            padre "¿Estás seguro? Es un peso, no solo un regalo. Pero si es lo que quieres... ven aquí."
            "Bram apoya una mano curtida sobre tu pecho. El calor que sientes no viene de la fragua esta vez — viene de dentro."
            padre "Ya está. Llévalo con cuidado, como todo lo que sale de esta casa."
            "El calor de la fragua nunca te quemó como a otros. Ahora entiendes por qué."

        "Ir a ver al Director de la escuela — AIRE":
            $ tipo_protagonista = "Aire"
            scene bg escuela_pueblo with dissolve
            show director_escuela at center
            director_escuela "¿Un don, a esta hora? Bueno, no serías el primero en decidirse de golpe. Acércate."
            "El Director traza un gesto simple en el aire frente a ti, casi aburrido de la rutina — y sin embargo, algo cambia."
            director_escuela "Listo. El aire responde distinto a quien lo lleva dentro. Ya lo notarás."
            "Sientes el viento nocturno de un modo distinto al salir — más cercano, casi como si pudiera escucharte."

        "Ir a la iglesia por el don de la Hermana Ysolde — LUZ":
            $ tipo_protagonista = "Luz"
            scene bg iglesia_pueblo with dissolve
            show sacerdote_iglesia at center
            sacerdote_iglesia "Que la luz te acompañe incluso cuando decidas no seguirla, hijo. Ven, arrodíllate."
            "La ceremonia es breve pero solemne. Cuando la Hermana Ysolde apoya las manos sobre tu cabeza, una calidez distinta a la del fuego te recorre — más quieta, más paciente."
            sacerdote_iglesia "Ya está hecho. Que sepas usarla con la misma calma con la que la recibiste."

        "Aceptar el don del viajero misterioso de paso por el pueblo — SOMBRA":
            $ tipo_protagonista = "Sombra"
            $ don_elegido_de_viajero = True
            scene bg posada_pueblo night with dissolve
            show viajero_misterioso at center
            "Encuentras al viajero en un rincón apartado de la posada, envuelto en una capa que no parece de por aquí. No preguntas su nombre; él tampoco ofrece dárselo."
            viajero_misterioso "Un don, dices. Curioso que vengas a mí y no a los tuyos. Está bien. No todos los caminos empiezan donde deberían."
            "Su voz es tranquila, casi demasiado tranquila. Extiende una mano y, sin ceremonia ni gesto solemne, algo frío y silencioso se instala en tu pecho."
            viajero_misterioso "Ya llevas la sombra contigo. Espero que la uses mejor que la mayoría."
            "Antes de que puedas preguntar nada más, el viajero ya se ha perdido entre la gente de la posada, como si nunca hubiera estado ahí."
            "[nombre_protagonista] no vuelve a verlo esa noche. No sabe que no será la última vez que se crucen."

    return
