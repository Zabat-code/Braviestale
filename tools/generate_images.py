#!/usr/bin/env python3
"""Pipeline de generacion de imagenes para Braviestale (OFFLINE-SAFE).

Este script NO genera arte por si solo: requiere un MOTOR de imagen
(GPU local con ComfyUI/SD, o una API de imagen con KEY). Lo que hace:
  1. Lee game/asset_prompts.json (prompts ya escritos en estilo Overlord).
  2. Expande a N variantes por prompt principal (default 2 -> 40 imagenes
     para los 20 primeros prompts, o todos si hay suficientes).
  3. Llama al motor configurado y guarda los PNG en game/images/ con los
     nombres que Ren'Py espera (bg_xxx.png, nombre.png).

MOTORES SOPORTADOS (pon el que tengas en ENGINE + credenciales):
  - "openai": necesita OPENAI_API_KEY; usa images.generate (gpt-image/DALL-E).
  - "replicate": necesita REPLICATE_API_TOKEN; modelo flux.
  - "comfyui": apunta a un servidor local http://127.0.0.1:8188 (GPU).
  - "none": solo escribe el plan JSON (assets_plan.json) y NO genera.

Uso:
  set OPENAI_API_KEY=sk-...
  python tools/generate_images.py --engine openai --variants 2 --limit 40

Sin KEY/GPU el script cae en modo "plan": deja assets_plan.json listo para
correr mañana con el motor conectado. Esto es lo que se ejecuta offline hoy.
"""
import os, sys, json, argparse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPTS = os.path.join(BASE, "proyecto_renpy", "game", "asset_prompts.json")
PLAN = os.path.join(BASE, "proyecto_renpy", "game", "assets_plan.json")
OUTDIR = os.path.join(BASE, "proyecto_renpy", "game", "images")

def slug(tag):
    # "bg herreria_interior" -> "bg_herreria_interior"
    return tag.replace(" ", "_")

def build_plan(limit, variants):
    with open(PROMPTS, encoding="utf-8") as f:
        data = json.load(f)
    entries = data["entries"]
    # prioriza personajes (sprites) y luego fondos clave
    chars = [e for e in entries if e["kind"] == "character"]
    bgs = [e for e in entries if e["kind"] == "background"]
    ordered = chars + bgs
    plan = []
    count = 0
    for e in ordered:
        for v in range(variants):
            if count >= limit:
                break
            name = f"{slug(e['id'])}" + (f"_{v+1}" if variants > 1 else "")
            plan.append({
                "out": os.path.join(OUTDIR, name + ".png"),
                "prompt": e["prompt"],
                "kind": e["kind"],
                "source_id": e["id"],
                "variant": v + 1,
            })
            count += 1
        if count >= limit:
            break
    os.makedirs(OUTDIR, exist_ok=True)
    with open(PLAN, "w", encoding="utf-8") as f:
        json.dump({"count": len(plan), "items": plan}, f, ensure_ascii=False, indent=2)
    return plan

def generate(plan, engine):
    if engine == "none":
        print(f"[PLAN] {len(plan)} imagenes planeadas -> {PLAN} (motor 'none', no se generan)")
        return
    # ---- Aqui conectas tu motor real ----
    # Ejemplo OpenAI (requiere openai>=1.0 y OPENAI_API_KEY):
    if engine == "openai":
        from openai import OpenAI
        client = OpenAI()
        for it in plan:
            r = client.images.generate(model="gpt-image-1", prompt=it["prompt"], size="1024x1024", n=1)
            url = r.data[0].url or r.data[0].b64_json
            # descarga/decodifica y guarda en it["out"]
            print("  gen", it["out"])
    elif engine == "replicate":
        print("[WARN] replicate no implementado en este stub; conecta tu token")
    elif engine == "comfyui":
        print("[WARN] comfyui no implementado en este stub; apunta a tu servidor GPU")
    else:
        raise SystemExit(f"motor desconocido: {engine}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", default="none", choices=["none", "openai", "replicate", "comfyui"])
    ap.add_argument("--variants", type=int, default=2)
    ap.add_argument("--limit", type=int, default=40)
    args = ap.parse_args()
    plan = build_plan(args.limit, args.variants)
    print(f"Plan: {len(plan)} imagenes (engine={args.engine})")
    generate(plan, args.engine)
    print("Listo. Con engine='none' solo se escribio el plan; conecta un motor para generar.")

if __name__ == "__main__":
    main()
