---
name: cowsay
description: >-
  Cowsay global para agentes: una vaca (o tux, moose, cat, koala) con caja redondeada, ánimo y título, renderizada por un binario determinista. Usar con /cowsay [texto|animal], en "modo vaca", y como cierre de los skills k-- (ÉXITO/FALLO).
license: MIT
metadata:
  author: kodexArg
  version: "2.0.0"
  homepage: https://github.com/kodexArg/cowsay
---

# cowsay

Binario: `bin/cowsay` junto a este archivo (Python 3 stdlib, un archivo). Instalado global: `~/.agents/skills/cowsay/bin/cowsay`; si `cowsay` en el PATH apunta ahí, alcanza con `cowsay`. **El binario es ley**: nunca se dibuja la caja ni el animal a mano; se muestra solo su stdout, en un bloque de código.

## Uso

```bash
C=~/.agents/skills/cowsay/bin/cowsay
$C --ok "Publicado: https://app.ejemplo.com"     # ╭─ ✔ ÉXITO ─╮  ojos ^^
$C --fail "El build rompió en tests"            # ╭─ ✘ FALLO ─╮  ojos xx
$C --warn -t "3 ramas" "quedaron sin borrar"    # título propio
$C --think -f cat "¿main o prod?"               # burbuja de pensamiento
$C -f tux <<'COW'
Texto largo, varias líneas.
COW
$C -l                                            # animales disponibles
```

- Ancho: se omite `-W`; el binario usa la terminal y tope 72. Emojis y acentos cuentan bien. URLs y rutas no se cortan.
- Animal: `-f <nombre>`, o `COWSAY_COW` para fijarlo. Solo los que lista `-l`.
- Idioma: el de la conversación.

## En el chat

| Pedido | Qué pasa |
| --- | --- |
| `/cowsay <texto>` | Una vez, ese texto. |
| `/cowsay <animal>` | Cambia el animal (`COWSAY_COW`) para el resto de la sesión. |
| `/cowsay` | Modo vaca: cada respuesta final sale por el binario, hasta "basta vaca". |
| "pensá" | `--think`. |

## Cierre de los skills k--

Una sola llamada, con el ánimo del resultado. La vaca dice **siempre una frase de qué se hizo** (nunca solo ÉXITO + URL) y **dónde quedó** (URL de PR, issue o deploy).

```bash
$C --ok "Arreglamos el token que expiraba antes de tiempo.
https://github.com/o/r/pull/42"
```

Si el binario falla, se reporta stderr y código de salida en texto plano, sin inventar arte.

Original cowsay: Tony Monroe — https://github.com/cowsay-org/cowsay
