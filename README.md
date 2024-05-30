# Project-race
Tento projekt je závodní hra s tématikou Formule 1. Program obsahuje tři minihry (Yellow flag, Green flag a Pitstop).

## Potřebné rozšíření
Pro hraní této hry jsou potřeba tato rozšíření:
- `pygame`
- `sys`
  ### Jak nainstaluji potřebná rozšíření?
- Použijte následující příkazy k instalaci rozšíření:
  ```bash
  pip install pygame
  pip install sys

## Minihry

### Yellow flag
V této minihře jedete po nekonečné trati a musíte se vyhýbat překážkám.

Cílem je vydržet co nejdéle a nasbírat co nejvyšší skóre.

Ve hře můžete:
- **Zrychlit** - zrychlí se rychlost i přičítání bodů.
- **Zpomalit** - zpomalí se rychlost i přičítání bodů.

Typy překážek:
- **Pneumatika** - odebere jeden život.
- **Štěrk** - odebere 10 bodů.

### Green flag
V této minihře musíte co nejrychleji projet tři kola na jednoduché trati.

Pokud se pokusíte zkrátit zatáčku, hra vás vrátí na začátek kola.

### Pitstop
V této minihře jedete po stejné trati jako v Green flag.

Při každém zatočení se snižuje životnost pneumatik.

Cílem hry je ujet co nejdelší vzdálenost.

## Ovládání
- Menu se ovládá čísly na horní části klávesnice a klávesou Escape.
- Ve hrách se pohybujete šipkami.

## Spuštění
1. Otevřete složku `projekt_race` ve Visual Studio.
2. Spusťte soubor `main.py`.

> **Poznámka:** Hra funguje pouze tehdy, když se otevře přímo složka `projekt_race`, nikoliv hlavní složka `project-race`.

## Ukázka
![Yellow flag](project_race/YFmenu_picture.png)
![Green flag](project_race/GFmenu_picture.png)
![Pitstop](project_race/Pmenu_picture.png)
