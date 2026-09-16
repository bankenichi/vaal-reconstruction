#!/usr/bin/env python3
"""
generate_pseudo_vaal.py  --  null-model string generator for the Vaal reconstruction.

Purpose: produce phonotactically Vaal-like strings that carry NO designed meaning,
so the decoding pipeline can be run on them to measure its false-positive rate
(how often it "finds" an attested root for a string that was never built from one).

Unbiasedness guarantees:
  1. The phonotactic model is trained ONLY on authentic Vaal surface forms
     (in-game strings + confirmed names). It never sees any source dictionary,
     so it cannot be steered toward real Maya/Nahuatl/K'iche'/Spanish roots.
  2. Fixed RNG seed -> the list is fully reproducible; no cherry-picking is possible.
  3. Filters remove corpus tokens, long substrings of corpus tokens, generated
     strings that embed a whole real root (>=4 chars), and ordinary Spanish
     loan-palette words. They do not select FOR or AGAINST decodability.

Default (no --rerun): writes the historical 2026-07 filenames for seed 1729.
Do not use default mode to overwrite a completed archive; that epoch is frozen.

--rerun: write pseudo_vaal_test_set_rerun.txt and per-seed
blind_test_worksheet_rerun_s{seed}.csv / blind_test_key_rerun_s{seed}.csv
for seeds 1729, 9001, 271828, 42, 55555. Distinct-string count equals trial
count (no cross-seed nonce repeats).

Re-run archive seed-1729: python3 generate_pseudo_vaal.py
Re-run de-duplicated battery: python3 generate_pseudo_vaal.py --rerun
"""
from __future__ import annotations

import argparse
import collections
import csv
import os
import random
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))

SEEDS = [1729, 9001, 271828, 42, 55555]
DEFAULT_SHUF = 2718
RERUN_N = 100

# --- Authentic Vaal SURFACE forms (romanized tokens as they appear in game / as names).
CORPUS = """
Atziri Otsuks Tzokan'te u'te A'te Yatle ik'el Kuxkal tlayeb kutsen Ela ukto Maax ka ti
a'tul cheyel mucane quxzeh Axba Kiibsa' ta' en Gyan'uks Donuks puxe daka jare fukuur soxsal
puyao te'moxti nochbe inib buxa Eche lu Aiokmo akal anab ascensionada atla cha'tsoke chikula'
ek elba Eztli Pilli Guatelitzi Ibil ich ikba'yucane ik'bala Ik'eche itsok itzil kifba kiimil
kilya ko'janti kujkuali liimek Ma'oxe mujuk' naach nochira pochiti qexcan sakilja ta'nuk tala
Teoyuxtlane til Tlaxye' Kextal uch' yuquia yutsal Xatlene Xibaqua Atzoatl Kuetzakala Quemalani
Xolotl Tizoc Cotan Axilo Mektul Ahuatotli Xomatl tatlat xomaplat xictep cutlotl azcado huatat
quiquate zahua moti taak'iin kahk tche ka'tse ipkaat koriek xecwa Napuatzi Doryani Zolin Zelina
Kamasa Kopec Ketzuli Tetzlapokal Arakaali Kishara
""".split()

# Real committed tokens used as PLANTS in the blind worksheet (known-good positives).
REAL_COMMITTED = [
    "Atziri", "ik'el", "mucane", "kutsen", "tlayeb", "Kuxkal", "tala", "ek", "Ela",
    "elba", "mujuk'", "naach", "kifba", "itsok", "kilya", "qexcan", "pochiti", "sakilja",
    "Kextal", "til", "Maax", "ti", "jare", "Otsuks", "kahk", "quxzeh", "Guatelitzi",
    "Eztli", "ta'nuk", "cha'tsoke",
]

# Archived leak list (NULL_HONESTY_OUTPUT.md N1) plus ordinary Spanish that
# slipped into the 2026-07 noise arm. Generator rejects these exact strings.
LEAK_EXACT = {
    "eztl", "noche", "ko'ja", "noch", "ikba", "guat", "kori", "quia", "tatl",
    "xolo", "ik'ec", "atzi", "ikul", "kisha", "gyan", "ecwa", "tzil", "ahua",
    "chbe", "ko'jan", "doryan", "ucan", "nada", "dorya", "quate", "ahuato",
    "mujuk", "chira", "ucane", "tzoka", "ascen", "ipka", "tzla", "otli",
    "atlen", "ektul", "xicte", "yucane", "icte", "anti", "kaat", "araka",
    "xomat", "tlene", "xatlen", "ictep", "donuk", "itzi", "kual", "puya",
    "ukuur", "pokal", "a'tse", "cheye", "puat", "te'mo", "kilja", "poka",
    "aiok", "xatl", "tlane", "mala", "kexta", "tzuli", "tlen", "kala", "tlat",
    "tzul", "ahuat", "mapla", "zeli", "tlax", "kuur", "an'uks",
}

# Ordinary Spanish (4-10 letters, Vaal-like CV shape) that a loan-palette
# decoder would correctly recover. These are not pure noise.
SPANISH_ORDINARY = {
    "noche", "nada", "mala", "malo", "casa", "cosa", "poco", "poca", "todo",
    "toda", "luna", "agua", "fuego", "mano", "boca", "cara", "vida", "tierra",
    "mucho", "mucha", "poco", "nino", "nina", "hijo", "hija", "padre", "madre",
    "suelo", "cielo", "fuego", "lejos", "cerca", "bueno", "buena", "grande",
    "noche", "dia", "dias", "hora", "hora", "otro", "otra", "otros", "otras",
    "este", "esta", "esto", "aqui", "alli", "alla", "como", "cuando", "donde",
    "quien", "cual", "cada", "todo", "nada", "algo", "alguien", "nunca",
    "siempre", "ahora", "antes", "despues", "luego", "entonces", "porque",
    "pero", "sino", "aunque", "entre", "sobre", "bajo", "hasta", "desde",
    "contra", "hacia", "segun", "durante", "mediante", "excepto", "salvo",
    "jefe", "jefa", "reina", "rey", "dios", "diosa", "templo", "altar",
    "sangre", "fuego", "agua", "tierra", "viento", "sol", "luna", "estrella",
    "noche", "dia", "guerra", "paz", "muerte", "vida", "alma", "cuerpo",
    "ojo", "ojos", "boca", "mano", "pies", "cabeza", "corazon", "nombre",
    "pueblo", "lugar", "casa", "camino", "puerta", "piedra", "arbol",
    "flor", "fruta", "maiz", "pan", "agua", "vino", "leche", "carne",
    "pescado", "ave", "perro", "gato", "serpiente", "aguila", "tigre",
    "cala", "calla", "calle", "carga", "carta", "causa", "cerca", "ciego",
    "claro", "coche", "color", "comer", "como", "compra", "comun", "conde",
    "copia", "coral", "corona", "correo", "corto", "costa", "crema", "cruz",
    "cuarto", "cubo", "cuenta", "cuerda", "cuerpo", "cuero", "cueva", "cura",
    "dama", "danza", "dato", "deuda", "dicha", "diente", "dieta", "diosa",
    "doble", "dolor", "drama", "duda", "dulce", "duro", "edad", "edificio",
    "ejemplo", "ejercito", "elefante", "elite", "embargo", "empleo", "empresa",
    "encima", "energia", "enfermo", "enojo", "entrada", "episodio", "equipo",
    "error", "escena", "escuela", "esfera", "esfuerzo", "espacio", "espada",
    "especie", "espejo", "espera", "esposa", "estado", "estilo", "estrella",
    "estudio", "etapa", "eterno", "evento", "examen", "exito", "extra",
    "faccion", "falda", "fama", "familia", "famoso", "fango", "faro", "fase",
    "favor", "fecha", "feliz", "feroz", "fiesta", "figura", "fila", "fin",
    "final", "finca", "firma", "flaco", "flecha", "flor", "fondo", "forma",
    "frase", "fresa", "frio", "fruta", "fuego", "fuente", "fuerza", "fuga",
    "funda", "furia", "futuro", "gala", "gana", "ganado", "garra", "gato",
    "gente", "gesto", "globo", "golpe", "goma", "gordo", "gota", "gozo",
    "grado", "gramo", "granja", "grano", "grasa", "grave", "grito", "grupo",
    "guante", "guerra", "guia", "guitarra", "gusto", "haber", "habito",
    "hacia", "hada", "hambre", "harina", "hasta", "hecho", "helado", "herida",
    "hermano", "heroe", "hielo", "hierro", "hija", "hijo", "hilo", "historia",
    "hogar", "hoja", "hombre", "hombro", "hondo", "honor", "hora", "hoy",
    "hueso", "huevo", "huir", "humano", "humo", "hundir", "idea", "iglesia",
    "igual", "imagen", "imperio", "indio", "infierno", "ingles", "inicio",
    "insecto", "invierno", "isla", "izquierdo", "jalar", "jardin", "jaula",
    "jefe", "joven", "juego", "jugo", "julio", "junio", "junto", "jurar",
    "justo", "labio", "lado", "lago", "lagrima", "lamento", "lampara", "lana",
    "largo", "lata", "leche", "lecho", "leer", "lejos", "lengua", "lento",
    "leon", "letra", "ley", "libertad", "libro", "limon", "linea", "liso",
    "lista", "llave", "lluvia", "lobo", "loco", "lodo", "lograr", "loma",
    "lomo", "loro", "lucha", "luego", "lugar", "lumbre", "luna", "lunes",
    "luto", "luz", "madre", "maestro", "magia", "maiz", "mal", "malo",
    "mama", "manana", "mando", "manejar", "manera", "manga", "mano", "manta",
    "manzana", "mapa", "maquina", "mar", "marca", "marcha", "marco", "marido",
    "masa", "mascara", "mata", "materia", "mayo", "mayor", "mazorca", "mecha",
    "media", "medico", "medida", "medio", "mejor", "melon", "memoria", "menor",
    "mensaje", "mente", "menu", "mercado", "mes", "mesa", "metal", "meter",
    "metro", "miedo", "miel", "miembro", "mientras", "milagro", "milla",
    "millon", "mina", "minuto", "mira", "mirada", "mismo", "mitad", "modelo",
    "modo", "mojado", "molino", "momento", "mono", "monte", "monton", "moral",
    "morder", "morir", "mosca", "mostrar", "motivo", "mover", "movil", "mucho",
    "mueble", "muerte", "muestra", "mujer", "mula", "mundo", "municion",
    "muerto", "museo", "musica", "nacer", "nacion", "nada", "nadie", "nariz",
    "nata", "natural", "navaja", "nave", "necio", "negar", "negocio", "negro",
    "nieve", "nino", "nivel", "noche", "nombre", "norte", "nota", "noticia",
    "nube", "nuca", "nudo", "nuevo", "numero", "nunca", "obra", "obrero",
    "oceano", "ocho", "octubre", "oculto", "ocupar", "oeste", "oficio",
    "ofrenda", "oido", "oir", "ojo", "ola", "oleo", "olor", "olvidar",
    "once", "onda", "onza", "opinion", "oponer", "oracion", "orden", "oreja",
    "organo", "orgullo", "oriente", "origen", "oro", "orquesta", "ortografia",
    "osar", "oscuro", "oso", "ostra", "otono", "otro", "oveja", "oxido",
    "oyente", "pacto", "padre", "paga", "pais", "paja", "palabra", "palacio",
    "palma", "palo", "paloma", "pan", "pana", "panal", "pandereta", "pantalla",
    "pano", "papa", "papel", "paquete", "par", "para", "parada", "parar",
    "parcial", "parecer", "pared", "pareja", "parentesco", "pariente", "paro",
    "parque", "parte", "partido", "pasar", "paseo", "pasion", "paso", "pasta",
    "pastel", "pata", "patata", "patio", "pato", "patria", "pausa", "pavo",
    "paz", "pecado", "pecho", "pedazo", "pedido", "pegar", "peine", "pelar",
    "pelea", "peligro", "pelo", "pelota", "pena", "penitencia", "pensamiento",
    "pensar", "peor", "pequeno", "pera", "perder", "perdon", "pereza",
    "perfil", "periodico", "perla", "permanecer", "permiso", "pero", "perro",
    "persona", "pesa", "pesar", "pesca", "pescado", "peso", "peste", "petalo",
    "petroleo", "pez", "piano", "picar", "pico", "pie", "piedra", "piel",
    "pierna", "pieza", "pila", "pimienta", "pino", "pinta", "pintar", "pinza",
    "piojo", "pipa", "pirata", "pisar", "piscina", "piso", "pista", "pistola",
    "pizarra", "placa", "plan", "planeta", "plano", "planta", "plata",
    "plato", "playa", "plaza", "plazo", "plomo", "pluma", "poblacion",
    "pobre", "poco", "poder", "poema", "poesia", "poeta", "policia", "polvo",
    "pollo", "pomada", "poner", "popa", "porcion", "porque", "portal",
    "portero", "posada", "poseer", "posible", "pozo", "prado", "precio",
    "preciso", "predicar", "premio", "prensa", "prisa", "prision", "problema",
    "proceso", "prodigio", "producto", "profeta", "programa", "prohibir",
    "promesa", "pronto", "propio", "prosa", "proteger", "provecho", "proximo",
    "prueba", "publico", "pueblo", "puente", "puerta", "puerto", "pues",
    "puesto", "pulgar", "pulir", "pulmon", "pulso", "punta", "punto",
    "punzada", "punal", "pupila", "pure", "puro", "queja", "quemar", "querer",
    "queso", "quien", "quieto", "quimica", "quince", "quinto", "quitar",
    "quizas", "rabo", "rama", "ramo", "rango", "rapido", "raro", "rata",
    "rato", "rayo", "raza", "razon", "realidad", "rebanada", "rebano",
    "recado", "recibir", "recibo", "reciente", "recio", "reclamo", "recoger",
    "recompensa", "recordar", "recreo", "recto", "recuerdo", "red", "redondo",
    "reducir", "reemplazo", "referir", "reflejo", "reforma", "regalo",
    "regar", "region", "regla", "regreso", "reina", "reino", "reir", "reja",
    "relato", "reloj", "remedio", "remo", "rengo", "renta", "reo", "reparar",
    "reparto", "repente", "repetir", "reposo", "reprender", "represa",
    "reproche", "reptil", "res", "reseca", "reserva", "residuo", "resistir",
    "resolucion", "respeto", "respiro", "responder", "resto", "resultado",
    "retraso", "retrato", "retroceso", "reunion", "revelar", "reves", "revista",
    "rey", "rezar", "riachuelo", "rico", "riego", "rienda", "riesgo", "rifa",
    "rigido", "rima", "rincon", "rio", "riqueza", "risa", "robar", "roble",
    "roca", "rodar", "rodilla", "rogar", "rojo", "romper", "ron", "ronda",
    "ropa", "rosa", "rostro", "roto", "rozar", "rubio", "rueda", "ruego",
    "ruido", "ruina", "ruleta", "rumbo", "rumor", "ruptura", "rural", "ruta",
    "sábado".replace("á", "a") if False else "sabado",
}

# Fold helper local to this file (generator must not import match_committed
# in a way that loads committed readings).
def fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("\u2019", "'").replace("\u2018", "'")
    return s


def spanish_set(extra_path: str | None = None) -> set[str]:
    """Ordinary Spanish forms the loan palette would recover as C, not noise."""
    out = {fold(w) for w in SPANISH_ORDINARY if 4 <= len(fold(w)) <= 10}
    out |= {fold(w) for w in LEAK_EXACT}
    # Optional: ilide Spanish headwords (local dict; never required to generate).
    candidates = []
    if extra_path:
        candidates.append(extra_path)
    env = os.environ.get("VAAL_DICT_DIR", "")
    if env:
        candidates.append(os.path.join(env, "ilide_SpanMaya_7c66.md"))
        candidates.append(os.path.join(env, "ilide_SpanMaya.md"))
    candidates += [
        os.path.join(HERE, "..", "sources", "dictionaries", "ilide_SpanMaya.md"),
        "/home/ubuntu/.cursor/projects/workspace/uploads/ilide_SpanMaya_7c66.md",
    ]
    for path in candidates:
        if not path or not os.path.isfile(path):
            continue
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                for line in f:
                    if ":" not in line:
                        continue
                    left = line.split(":", 1)[0].strip()
                    if " " in left or not left:
                        continue
                    fl = fold(left)
                    fl = re.sub(r"[^a-z']+", "", fl)
                    if 4 <= len(fl) <= 10 and any(v in fl for v in "aeiou"):
                        out.add(fl)
        except OSError:
            continue
        break
    return out


def build_model(words):
    K = 2
    START, END = "\x02", "\x03"
    model = collections.defaultdict(collections.Counter)
    for w in words:
        s = START * K + w + END
        for i in range(len(s) - K):
            model[s[i:i + K]][s[i + K]] += 1
    return model, K, START, END


def corpus_filters(words):
    """Reject corpus tokens AND long substrings of corpus tokens.

    The 2026-07 generator only rejected generated strings that *contained* a
    corpus token of length >=4. It missed generated strings that *are*
    substrings of a corpus token (eztl of eztli, ko'ja of ko'janti).
    """
    words_l = [w.lower() for w in words]
    big = [w for w in words_l if len(w) >= 4]
    # All substrings of length >=4 of every corpus token.
    subs = set()
    for w in words_l:
        for n in range(4, len(w) + 1):
            for i in range(0, len(w) - n + 1):
                subs.add(w[i:i + n])
    return words_l, big, subs


def ok_legacy(s, words_l, big, seen):
    """2026-07 filter. Reproduces the archived seed-1729 set. Incomplete (N1)."""
    if s is None:
        return False
    sl = s.lower()
    if not (4 <= len(sl) <= 10):
        return False
    if sl in seen:
        return False
    if sl in words_l:
        return False
    if "''" in sl or sl.startswith("'"):
        return False
    if not any(v in sl for v in "aeiou"):
        return False
    if any(rw in sl for rw in big):
        return False
    return True


def ok_rerun(s, words_l, big, subs, spanish, seen):
    """Re-run filter: also reject corpus substrings and ordinary Spanish."""
    if not ok_legacy(s, words_l, big, seen):
        return False
    sl = s.lower()
    if sl in subs:
        return False
    if fold(sl) in spanish:
        return False
    if sl in LEAK_EXACT:
        return False
    return True


def gen_one(rng, model, K, START, END, accept):
    for _ in range(4000):
        ctx = START * K
        out = []
        while len(out) <= 11:
            nxt = model.get(ctx)
            if not nxt:
                break
            ch = rng.choices(list(nxt), weights=list(nxt.values()))[0]
            if ch == END:
                break
            out.append(ch)
            ctx = (ctx + ch)[-K:]
        s = "".join(out).strip("'")
        if accept(s):
            return s
    return None


def write_set(pseudo, seed, shuf_seed, prefix="", set_path=None):
    """Write one seed's test set, worksheet, and key.

    prefix='' writes historical filenames.
    prefix='rerun_' writes the re-run filenames.
    """
    if prefix:
        ws_name = f"blind_test_worksheet_{prefix}s{seed}.csv"
        key_name = f"blind_test_key_{prefix}s{seed}.csv"
    else:
        ws_name = f"blind_test_worksheet_s{seed}.csv"
        key_name = f"blind_test_key_s{seed}.csv"
        if set_path is None:
            set_path = os.path.join(HERE, "pseudo_vaal_test_set.txt")
    if set_path:
        with open(set_path, "w", encoding="utf-8") as f:
            f.write(f"# 100 pseudo-Vaal strings (null model). Seed {seed}. See NULL_MODEL_PROTOCOL.md\n")
            for i, s in enumerate(pseudo, 1):
                f.write(f"{i:3d}. {s}\n")
    items = [("pseudo", s) for s in pseudo] + [("real", w) for w in REAL_COMMITTED]
    shuf = random.Random(shuf_seed)
    shuf.shuffle(items)
    ws_path = os.path.join(HERE, ws_name)
    key_path = os.path.join(HERE, key_name)
    with open(ws_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "string", "found", "confidence", "root", "lang", "gloss", "residue", "notes"])
        for i, (t, s) in enumerate(items, 1):
            w.writerow([i, s, "", "", "", "", "", "", ""])
    with open(key_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "type", "string"])
        for i, (t, s) in enumerate(items, 1):
            w.writerow([i, t, s])
    return ws_path, key_path


def generate_rerun(spanish):
    words_l, big, subs = corpus_filters(CORPUS)
    model, K, START, END = build_model(words_l)
    global_seen = set()
    all_rows = []
    by_seed = {}
    for seed in SEEDS:
        rng = random.Random(seed)
        pseudo = []
        attempts = 0
        while len(pseudo) < RERUN_N:
            attempts += 1
            if attempts > 200000:
                raise RuntimeError(f"failed to fill seed {seed} after {attempts} draws")
            s = gen_one(
                rng, model, K, START, END,
                lambda cand, _wl=words_l, _big=big, _subs=subs, _sp=spanish, _seen=global_seen: ok_rerun(
                    cand, _wl, _big, _subs, _sp, _seen
                ),
            )
            if s:
                global_seen.add(s.lower())
                pseudo.append(s)
                all_rows.append((seed, s))
        by_seed[seed] = pseudo
        write_set(pseudo, seed, seed + 1, prefix="rerun_")
    set_path = os.path.join(HERE, "pseudo_vaal_test_set_rerun.txt")
    with open(set_path, "w", encoding="utf-8") as f:
        f.write("# De-duplicated re-run pseudo-Vaal set. Distinct-string count == trial count.\n")
        f.write(f"# Seeds {SEEDS}. See EXPERIMENT_RERUN_PROTOCOL.md and NULL_MODEL_PROTOCOL.md\n")
        n = 0
        for seed in SEEDS:
            f.write(f"\n# seed {seed}\n")
            for s in by_seed[seed]:
                n += 1
                f.write(f"{n:3d}. {s}\n")
    n_distinct = len({s.lower() for _, s in all_rows})
    n_trials = len(all_rows)
    if n_distinct != n_trials:
        raise RuntimeError(f"distinct {n_distinct} != trials {n_trials}")
    print(f"rerun: wrote {n_trials} unique strings across seeds {SEEDS} (distinct={n_distinct})")
    print(f"  {set_path}")
    for seed in SEEDS:
        print(f"  blind_test_worksheet_rerun_s{seed}.csv / blind_test_key_rerun_s{seed}.csv")
    return by_seed


def generate_archive(seed, shuf_seed, spanish, force=False):
    """Reproduce the 2026-07 generator. Refuses to overwrite existing archives."""
    ws = os.path.join(HERE, f"blind_test_worksheet_s{seed}.csv")
    key = os.path.join(HERE, f"blind_test_key_s{seed}.csv")
    pset = os.path.join(HERE, "pseudo_vaal_test_set.txt")
    if not force and (os.path.exists(ws) or os.path.exists(key)):
        print(f"refusing to overwrite 2026-07 archive {ws} (pass --force to regenerate)",
              file=sys.stderr)
        return
    words_l, big, subs = corpus_filters(CORPUS)
    model, K, START, END = build_model(words_l)
    rng = random.Random(seed)
    seen = set()
    pseudo = []
    while len(pseudo) < 100:
        s = gen_one(
            rng, model, K, START, END,
            lambda cand, _wl=words_l, _big=big, _seen=seen: ok_legacy(cand, _wl, _big, _seen),
        )
        if s:
            seen.add(s.lower())
            pseudo.append(s)
    write_set(pseudo, seed, shuf_seed, prefix="", set_path=pset)
    print(f"wrote pseudo_vaal_test_set.txt (100), blind_test_worksheet_s{seed}.csv and blind_test_key_s{seed}.csv (130 items)")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("seed", nargs="?", type=int, default=None)
    p.add_argument("shuf_seed", nargs="?", type=int, default=None)
    p.add_argument("--rerun", action="store_true",
                   help="write de-duplicated re-run files; do not touch 2026-07 archives")
    p.add_argument("--force", action="store_true",
                   help="allow overwriting existing 2026-07 archive filenames (default: refuse)")
    p.add_argument("--spanish-list", default=None, help="optional extra Spanish word list path")
    args = p.parse_args(argv)
    spanish = spanish_set(args.spanish_list)
    if args.rerun:
        generate_rerun(spanish)
        return
    seed = args.seed if args.seed is not None else 1729
    shuf = args.shuf_seed if args.shuf_seed is not None else DEFAULT_SHUF
    generate_archive(seed, shuf, spanish, force=args.force)


if __name__ == "__main__":
    main()
