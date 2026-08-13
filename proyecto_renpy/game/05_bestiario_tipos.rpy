########################################################
# SISTEMA DE TIPOS ELEMENTALES (círculo de ventajas)
# ------------------------------------------------------
# 5 tipos: Agua, Fuego, Piedra, Oscuridad, Luz
# Cada tipo vence a 2 y pierde ante 2 (sin empates de ciclo).
#
#   Agua      vence a  Fuego, Piedra       (apaga / erosiona)
#   Fuego     vence a  Piedra, Oscuridad   (funde / quema sombras)
#   Piedra    vence a  Oscuridad, Luz      (bloquea / absorbe)
#   Oscuridad vence a  Luz, Agua           (apaga / enturbia)
#   Luz       vence a  Agua, Fuego         (brilla a través / opaca)
########################################################

init python:

    TIPOS_ELEMENTALES = ["Agua", "Fuego", "Tierra", "Sombra", "Luz"]

    VENTAJAS_TIPO = {
        "Agua":       ["Fuego", "Tierra"],
        "Fuego":      ["Tierra", "Sombra"],
        "Tierra":     ["Sombra", "Luz"],
        "Sombra":  ["Luz", "Agua"],
        "Luz":        ["Agua", "Fuego"],
    }

    MULTIPLICADOR_VENTAJA = 1.5   # daño extra si atacas con ventaja de tipo
    MULTIPLICADOR_DESVENTAJA = 0.65  # daño reducido si atacas en desventaja

    def calcular_multiplicador_tipo(tipo_atacante, tipo_defensor):
        if tipo_defensor in VENTAJAS_TIPO.get(tipo_atacante, []):
            return MULTIPLICADOR_VENTAJA
        elif tipo_atacante in VENTAJAS_TIPO.get(tipo_defensor, []):
            return MULTIPLICADOR_DESVENTAJA
        else:
            return 1.0  # tipos neutrales entre sí


########################################################
# NIVELES POR ZONA
# ------------------------------------------------------
# Cada zona tiene un nivel fijo para sus monstruos comunes,
# y el jefe de esa zona es nivel_zona + 5.
########################################################

init python:

    NIVEL_ZONA = {
        "bosque_gris": 5,
        "bosque_profundo": 10,   # zona de la bruja, fase 2 del bosque
        "playa": 5,
        "desierto": 5,
        "rio": 5,
        "aire": 5,
        "cuevas": 5,
        "ciudad_horda": 15,
    }

    NIVEL_JEFE_ZONA = {k: v + 5 for k, v in NIVEL_ZONA.items()}

    def escalar_stats_por_nivel(hp_base, ataque_base, defensa_base, nivel):
        """Escala stats base (definidas a nivel 5) a cualquier nivel de zona."""
        factor = nivel / 5.0
        return (
            int(hp_base * factor),
            int(ataque_base * factor),
            int(defensa_base * factor),
        )


########################################################
# SISTEMA DE TIPO DE ARMA (independiente del sistema elemental)
# ------------------------------------------------------
# 4 tipos de arma: Corte, Punzante, Impacto, Proyectil.
# Cada monstruo tiene UNA debilidad (recibe más daño) y UNA
# resistencia (recibe menos daño) de arma, según su naturaleza
# física. Esto corre EN PARALELO al sistema elemental — un
# monstruo tiene ambos, tipo elemental Y perfil de arma.
#
# Lógica base:
#   Corte     -> bueno vs. carne blanda      / malo vs. hueso-caparazón
#   Punzante  -> bueno vs. armadura ligera   / malo vs. gelatinoso
#   Impacto   -> bueno vs. hueso-piedra      / malo vs. blindaje pesado
#   Proyectil -> bueno vs. volador/distancia / malo vs. escudos
#
# Nota de diseño (pendiente, no romper el juego): más adelante
# se decidirá por nivel qué arma/habilidad puede usar cada
# personaje jugable, para no dar acceso a las 4 desde el
# principio. Por ahora solo se define el perfil de cada
# monstruo; el jugador elige el arma en combate igual que elige
# hechizo.
########################################################

init python:

    TIPOS_ARMA = ["Corte", "Punzante", "Impacto", "Proyectil"]

    MULTIPLICADOR_ARMA_DEBIL = 1.5    # el monstruo es débil a esa arma
    MULTIPLICADOR_ARMA_RESISTE = 0.6  # el monstruo resiste esa arma

    def calcular_multiplicador_arma(tipo_arma, debilidad_monstruo, resistencia_monstruo):
        if tipo_arma == debilidad_monstruo:
            return MULTIPLICADOR_ARMA_DEBIL
        elif tipo_arma == resistencia_monstruo:
            return MULTIPLICADOR_ARMA_RESISTE
        else:
            return 1.0


########################################################
# CLASE ENEMIGO EXTENDIDA CON TIPO ELEMENTAL + PERFIL DE ARMA
########################################################

init python:

    class EnemigoTipado(Enemigo):
        def __init__(self, nombre, hp, ataque, defensa, agilidad, exp_otorga, oro_otorga, tipo,
                     sprite="enemigo_generico", nivel=5, debil_arma=None, resiste_arma=None):
            Enemigo.__init__(self, nombre, hp, ataque, defensa, agilidad, exp_otorga, oro_otorga, sprite)
            self.tipo = tipo                # tipo elemental: Agua/Fuego/Tierra/Aire/Sombra/Luz
            self.nivel = nivel
            self.debil_arma = debil_arma        # ej. "Corte"
            self.resiste_arma = resiste_arma    # ej. "Impacto"


########################################################
# TABLA DE MONSTRUOS — BOSQUE GRIS (Nivel 5)
########################################################

init python:

    def crear_monstruos_bosque(nivel=5):
        hp_f, atk_f, def_f = escalar_stats_por_nivel(1, 1, 1, nivel)  # factor de referencia
        f = nivel / 5.0
        return [
            EnemigoTipado("Goblin", int(28*f), int(7*f), int(3*f), 9, int(18*f), 3, "Tierra", "goblin", nivel, debil_arma="Corte", resiste_arma="Impacto"),
            EnemigoTipado("Goblin Arquero", int(20*f), int(9*f), int(1*f), 11, int(20*f), 4, "Tierra", "goblin_arquero", nivel, debil_arma="Corte", resiste_arma="Proyectil"),
            EnemigoTipado("Lobo Salvaje", int(18*f), int(6*f), int(2*f), 14, int(12*f), 2, "Sombra", "lobo", nivel, debil_arma="Impacto", resiste_arma="Punzante"),
            EnemigoTipado("Ent Menor", int(45*f), int(8*f), int(8*f), 2, int(25*f), 5, "Tierra", "ent_menor", nivel, debil_arma="Corte", resiste_arma="Impacto"),
            EnemigoTipado("Hada Corrupta", int(15*f), int(6*f), int(1*f), 12, int(16*f), 6, "Sombra", "hada_corrupta", nivel, debil_arma="Proyectil", resiste_arma="Corte"),
            EnemigoTipado("Araña Gigante", int(22*f), int(7*f), int(2*f), 10, int(19*f), 3, "Sombra", "arana_gigante", nivel, debil_arma="Punzante", resiste_arma="Impacto"),
            EnemigoTipado("Duende Silvano", int(16*f), int(5*f), int(1*f), 13, int(14*f), 8, "Luz", "duende_silvano", nivel, debil_arma="Impacto", resiste_arma="Corte"),
            EnemigoTipado("Oso Embrujado", int(38*f), int(10*f), int(4*f), 6, int(27*f), 4, "Tierra", "oso_embrujado", nivel, debil_arma="Corte", resiste_arma="Punzante"),
            EnemigoTipado("Espíritu del Musgo", int(24*f), int(5*f), int(3*f), 7, int(17*f), 3, "Agua", "espiritu_musgo", nivel, debil_arma="Impacto", resiste_arma="Punzante"),
            EnemigoTipado("Cuervo Presagio", int(14*f), int(6*f), int(1*f), 15, int(13*f), 2, "Sombra", "cuervo_presagio", nivel, debil_arma="Proyectil", resiste_arma="Impacto"),
        ]


########################################################
# TABLA DE MONSTRUOS — PLAYA (Nivel 5)
########################################################

init python:

    def crear_monstruos_playa(nivel=5):
        f = nivel / 5.0
        return [
            EnemigoTipado("Cangrejo Gigante", int(30*f), int(8*f), int(5*f), 5, int(19*f), 4, "Tierra", "cangrejo_gigante", nivel, debil_arma="Impacto", resiste_arma="Corte"),
            EnemigoTipado("Sirena Varada", int(20*f), int(7*f), int(2*f), 9, int(21*f), 6, "Agua", "sirena_varada", nivel, debil_arma="Punzante", resiste_arma="Proyectil"),
            EnemigoTipado("Espectro de Naufragio", int(19*f), int(8*f), int(1*f), 8, int(20*f), 5, "Sombra", "espectro_naufragio", nivel, debil_arma="Impacto", resiste_arma="Corte"),
            EnemigoTipado("Gaviota Colosal", int(16*f), int(6*f), int(1*f), 13, int(14*f), 2, "Luz", "gaviota_colosal", nivel, debil_arma="Proyectil", resiste_arma="Impacto"),
            EnemigoTipado("Cangrejo Ermitaño Encantado", int(24*f), int(6*f), int(4*f), 6, int(17*f), 5, "Agua", "cangrejo_ermitano", nivel, debil_arma="Impacto", resiste_arma="Punzante"),
            EnemigoTipado("Medusa Flotante", int(15*f), int(7*f), int(1*f), 8, int(16*f), 4, "Agua", "medusa_flotante", nivel, debil_arma="Proyectil", resiste_arma="Corte"),
            EnemigoTipado("Momia de Arena", int(32*f), int(7*f), int(5*f), 3, int(22*f), 5, "Tierra", "momia_arena", nivel, debil_arma="Impacto", resiste_arma="Punzante"),
            EnemigoTipado("Tiburón de Arena", int(26*f), int(9*f), int(3*f), 10, int(21*f), 5, "Tierra", "tiburon_arena", nivel, debil_arma="Corte", resiste_arma="Proyectil"),
            EnemigoTipado("Elemental de Sal", int(21*f), int(6*f), int(3*f), 7, int(18*f), 4, "Luz", "elemental_sal", nivel, debil_arma="Impacto", resiste_arma="Corte"),
            EnemigoTipado("Pulpo Playero", int(23*f), int(7*f), int(2*f), 9, int(19*f), 5, "Agua", "pulpo_playero", nivel, debil_arma="Corte", resiste_arma="Impacto"),
        ]


########################################################
# TABLA DE MONSTRUOS — DESIERTO (Nivel 5)
########################################################

init python:

    def crear_monstruos_desierto(nivel=5):
        f = nivel / 5.0
        return [
            EnemigoTipado("Escorpión Gigante", int(24*f), int(8*f), int(3*f), 9, int(19*f), 5, "Tierra", "escorpion_gigante", nivel, debil_arma="Impacto", resiste_arma="Punzante"),
            EnemigoTipado("Escarabajo Acorazado", int(35*f), int(6*f), int(7*f), 4, int(20*f), 4, "Tierra", "escarabajo_acorazado", nivel, debil_arma="Impacto", resiste_arma="Corte"),
            EnemigoTipado("Djinn Menor", int(22*f), int(9*f), int(2*f), 10, int(24*f), 8, "Fuego", "djinn_menor", nivel, debil_arma="Proyectil", resiste_arma="Corte"),
            EnemigoTipado("Momia Antigua", int(28*f), int(7*f), int(4*f), 5, int(23*f), 6, "Sombra", "momia_antigua", nivel, debil_arma="Impacto", resiste_arma="Corte"),
            EnemigoTipado("Serpiente de Fuego", int(18*f), int(9*f), int(1*f), 13, int(20*f), 5, "Fuego", "serpiente_fuego", nivel, debil_arma="Impacto", resiste_arma="Punzante"),
            EnemigoTipado("Buitre Carroñero", int(16*f), int(6*f), int(1*f), 12, int(14*f), 3, "Sombra", "buitre_carronero", nivel, debil_arma="Proyectil", resiste_arma="Impacto"),
            EnemigoTipado("Golem de Arena", int(40*f), int(8*f), int(8*f), 2, int(26*f), 5, "Tierra", "golem_arena", nivel, debil_arma="Impacto", resiste_arma="Corte"),
            EnemigoTipado("Espectro del Oasis", int(20*f), int(6*f), int(2*f), 8, int(18*f), 5, "Agua", "espectro_oasis", nivel, debil_arma="Impacto", resiste_arma="Corte"),
            EnemigoTipado("Salamandra de Dunas", int(19*f), int(8*f), int(2*f), 9, int(19*f), 5, "Fuego", "salamandra_dunas", nivel, debil_arma="Corte", resiste_arma="Proyectil"),
            EnemigoTipado("Nómada Maldito", int(26*f), int(7*f), int(3*f), 7, int(21*f), 6, "Sombra", "nomada_maldito", nivel, debil_arma="Corte", resiste_arma="Punzante"),
        ]


########################################################
# TABLA DE MONSTRUOS — RÍO / AGUA (Nivel 5)
########################################################

init python:

    def crear_monstruos_rio(nivel=5):
        f = nivel / 5.0
        return [
            EnemigoTipado("Ninfa del Río", int(20*f), int(6*f), int(2*f), 9, int(20*f), 6, "Agua", "ninfa_rio", nivel, debil_arma="Punzante", resiste_arma="Proyectil"),
            EnemigoTipado("Serpiente Acuática", int(19*f), int(8*f), int(1*f), 11, int(19*f), 4, "Agua", "serpiente_acuatica", nivel, debil_arma="Impacto", resiste_arma="Punzante"),
            EnemigoTipado("Kelpie", int(27*f), int(9*f), int(3*f), 8, int(23*f), 6, "Sombra", "kelpie", nivel, debil_arma="Corte", resiste_arma="Proyectil"),
            EnemigoTipado("Rana Gigante Tóxica", int(21*f), int(6*f), int(2*f), 7, int(17*f), 4, "Agua", "rana_toxica", nivel, debil_arma="Proyectil", resiste_arma="Punzante"),
            EnemigoTipado("Elemental de Agua", int(24*f), int(9*f), int(2*f), 8, int(24*f), 6, "Agua", "elemental_agua", nivel, debil_arma="Impacto", resiste_arma="Corte"),
            EnemigoTipado("Piraña Espectral", int(13*f), int(7*f), int(1*f), 14, int(13*f), 2, "Sombra", "pirana_espectral", nivel, debil_arma="Impacto", resiste_arma="Corte"),
            EnemigoTipado("Guardián de Coral", int(38*f), int(7*f), int(7*f), 3, int(25*f), 5, "Tierra", "guardian_coral", nivel, debil_arma="Impacto", resiste_arma="Punzante"),
            EnemigoTipado("Nix Susurrante", int(18*f), int(6*f), int(2*f), 10, int(19*f), 6, "Luz", "nix_susurrante", nivel, debil_arma="Proyectil", resiste_arma="Corte"),
            EnemigoTipado("Cangrejo de Río Blindado", int(30*f), int(6*f), int(6*f), 5, int(20*f), 4, "Tierra", "cangrejo_rio", nivel, debil_arma="Impacto", resiste_arma="Corte"),
            EnemigoTipado("Anguila Eléctrica Mística", int(17*f), int(9*f), int(1*f), 12, int(21*f), 5, "Fuego", "anguila_electrica", nivel, debil_arma="Punzante", resiste_arma="Impacto"),
        ]


########################################################
# TABLA DE MONSTRUOS — AIRE (Nivel 5)
########################################################

init python:

    def crear_monstruos_aire(nivel=5):
        f = nivel / 5.0
        return [
            EnemigoTipado("Halcón Espectral", int(16*f), int(8*f), int(1*f), 15, int(17*f), 4, "Luz", "halcon_espectral", nivel, debil_arma="Proyectil", resiste_arma="Impacto"),
            EnemigoTipado("Gárgola Menor", int(30*f), int(7*f), int(6*f), 5, int(21*f), 5, "Tierra", "gargola_menor", nivel, debil_arma="Impacto", resiste_arma="Corte"),
            EnemigoTipado("Espíritu del Viento", int(15*f), int(6*f), int(1*f), 16, int(16*f), 4, "Luz", "espiritu_viento", nivel, debil_arma="Proyectil", resiste_arma="Corte"),
            EnemigoTipado("Grifo Joven", int(26*f), int(9*f), int(3*f), 12, int(24*f), 7, "Luz", "grifo_joven", nivel, debil_arma="Proyectil", resiste_arma="Impacto"),
            EnemigoTipado("Murciélago Gigante", int(14*f), int(6*f), int(1*f), 14, int(13*f), 2, "Sombra", "murcielago_gigante", nivel, debil_arma="Impacto", resiste_arma="Proyectil"),
            EnemigoTipado("Elemental de Tormenta", int(22*f), int(9*f), int(2*f), 11, int(23*f), 6, "Fuego", "elemental_tormenta", nivel, debil_arma="Proyectil", resiste_arma="Corte"),
            EnemigoTipado("Cuervo de Guerra", int(17*f), int(7*f), int(2*f), 13, int(16*f), 3, "Sombra", "cuervo_guerra", nivel, debil_arma="Proyectil", resiste_arma="Corte"),
            EnemigoTipado("Wyvern Menor", int(32*f), int(10*f), int(4*f), 10, int(28*f), 8, "Fuego", "wyvern_menor", nivel, debil_arma="Punzante", resiste_arma="Corte"),
            EnemigoTipado("Sílfide Traviesa", int(15*f), int(6*f), int(1*f), 15, int(15*f), 5, "Luz", "silfide_traviesa", nivel, debil_arma="Proyectil", resiste_arma="Punzante"),
            EnemigoTipado("Buitre de las Cumbres", int(18*f), int(7*f), int(2*f), 12, int(17*f), 3, "Sombra", "buitre_cumbres", nivel, debil_arma="Proyectil", resiste_arma="Impacto"),
        ]


########################################################
# TABLA DE MONSTRUOS — CUEVAS (Nivel 5)
########################################################

init python:

    def crear_monstruos_cuevas(nivel=5):
        f = nivel / 5.0
        return [
            EnemigoTipado("Murciélago de Cueva", int(14*f), int(6*f), int(1*f), 14, int(12*f), 2, "Sombra", "murcielago_cueva", nivel, debil_arma="Impacto", resiste_arma="Proyectil"),
            EnemigoTipado("Troglodita", int(34*f), int(9*f), int(4*f), 5, int(24*f), 5, "Tierra", "troglodita", nivel, debil_arma="Corte", resiste_arma="Impacto"),
            EnemigoTipado("Gusano de Roca", int(28*f), int(8*f), int(5*f), 3, int(20*f), 4, "Tierra", "gusano_roca", nivel, debil_arma="Impacto", resiste_arma="Corte"),
            EnemigoTipado("Araña Cavernaria", int(20*f), int(7*f), int(2*f), 10, int(18*f), 4, "Sombra", "arana_cavernaria", nivel, debil_arma="Punzante", resiste_arma="Impacto"),
            EnemigoTipado("Slime Ácido", int(22*f), int(6*f), int(2*f), 6, int(17*f), 3, "Agua", "slime_acido", nivel, debil_arma="Proyectil", resiste_arma="Punzante"),
            EnemigoTipado("Kobold Minero", int(19*f), int(7*f), int(3*f), 9, int(16*f), 6, "Tierra", "kobold_minero", nivel, debil_arma="Corte", resiste_arma="Impacto"),
            EnemigoTipado("Espectro de las Profundidades", int(18*f), int(9*f), int(1*f), 11, int(22*f), 5, "Sombra", "espectro_profundidades", nivel, debil_arma="Impacto", resiste_arma="Corte"),
            EnemigoTipado("Basilisco Joven", int(26*f), int(8*f), int(4*f), 7, int(23*f), 6, "Tierra", "basilisco_joven", nivel, debil_arma="Impacto", resiste_arma="Punzante"),
            EnemigoTipado("Cristal Viviente", int(24*f), int(6*f), int(4*f), 4, int(19*f), 7, "Luz", "cristal_viviente", nivel, debil_arma="Impacto", resiste_arma="Proyectil"),
            EnemigoTipado("Enano Corrupto", int(25*f), int(8*f), int(3*f), 8, int(20*f), 5, "Sombra", "enano_corrupto", nivel, debil_arma="Corte", resiste_arma="Impacto"),
        ]


########################################################
# TABLAS DE ENCUENTRO POR ZONA (usa las funciones de arriba)
########################################################

init python:

    def tirar_encuentro_zona(nombre_zona):
        """Devuelve UN enemigo aleatorio de la zona indicada, ya al nivel correcto."""
        nivel = NIVEL_ZONA.get(nombre_zona, 5)

        generadores = {
            "bosque_gris": crear_monstruos_bosque,
            "bosque_profundo": crear_monstruos_bosque,
            "playa": crear_monstruos_playa,
            "desierto": crear_monstruos_desierto,
            "rio": crear_monstruos_rio,
            "aire": crear_monstruos_aire,
            "cuevas": crear_monstruos_cuevas,
        }

        gen = generadores.get(nombre_zona, crear_monstruos_bosque)
        pool = gen(nivel)
        return random.choice(pool)
