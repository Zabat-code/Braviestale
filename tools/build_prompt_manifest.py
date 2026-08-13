#!/usr/bin/env python3
"""Build a structured image-prompt manifest from prompts_imagenes_capitulo1.txt.
Output: game/asset_prompts.json  (list of {id,kind,tag,prompt}) ready for any
image generator. Generation itself needs a GPU/API (ComfyUI/SD/FLUX) -- not
available offline on this machine, so this script only organizes the data.
"""
import os, re, json

SRC = r"F:\ia.proyectos\BRAviestale\Braviestale\prompts_imagenes_capitulo1.txt"
OUT = r"F:\ia.proyectos\BRAviestale\Braviestale\proyecto_renpy\game\asset_prompts.json"

base = ("anime fantasy digital painting, production quality like Overlord, "
        "clean proportions, cinematic lighting, detailed textures, visual novel, "
        "no text, no watermark")

entries = []
cur_id = None; cur_kind = None; cur_tag = None; buf = []
section = None

with open(SRC, encoding="utf-8") as f:
    for line in f:
        s = line.strip()
        m = re.match(r"^\[(.*?)\]\s*$", s)
        if m:
            # flush previous
            if cur_id is not None:
                prompt = " ".join(buf).strip()
                entries.append({"id": cur_id, "kind": cur_kind, "tag": cur_tag,
                                "prompt": (prompt + " " + base).strip()})
            cur_id = m.group(1).strip()
            cur_kind = "character" if any(k in cur_id for k in
                        ["padre","amigo","doran","mira","director","sacerdote",
                         "viajero","guardia","bruja","theron","wren","elyra",
                         "sable","thrain","lyanwe","gorrak","maestro","soldado",
                         "fanatico","pueblerino"]) else "background"
            cur_tag = "character" if cur_kind == "character" else "bg"
            buf = []
            continue
        if s.startswith("[bg ") or s.startswith("[padre") or s == "":
            # section headers inside [] like [bg herreria_interior] already handled;
            # this catches "SECCION" lines
            if s.startswith("SECCIÓN") or s.startswith("==="):
                continue
        if cur_id is not None:
            # skip pure section banners
            if re.match(r"^SECCI[ÓO]N", s) or set(s) <= set("=-"):
                continue
            buf.append(s)

# flush last
if cur_id is not None:
    prompt = " ".join(buf).strip()
    entries.append({"id": cur_id, "kind": cur_kind, "tag": cur_tag,
                    "prompt": (prompt + " " + base).strip()})

# Only keep entries that have a real prompt (skip empty banners)
entries = [e for e in entries if len(e["prompt"]) > len(base) + 5]

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump({"count": len(entries), "entries": entries}, f,
              ensure_ascii=False, indent=2)

print(f"Wrote {len(entries)} image prompts -> {OUT}")
