# Snake TUI

Snake mais dans le terminal.

![](./gameplay.png)

## Installation

- Sur Macos :
```bash
git clone https://OrAxelerator/pixel-snake-tui.git
cd pixel-snake-tui
pip install -e .
```

- Sur Linux pip peut installez mais je conseille pipx
> Installaton pipx sur linux :
>  sudo apt install pipx
>  pipx ensurepath
>  pipx install .

- Sur Windows : 
```bash
git clone https://OrAxelerator/pixel-snake-tui.git
cd pixel-snake-tui
python -m pip install .
```

## Lancement

```bash
snake
```

Options :

```bash
snake -apple 4
snake -no-colision
snake -apple 4 -no-colision
```

Touches :

- Fleches ou `h` `j` `k` `l` : deplacer le serpent
- `esc` : pause
- `r` : relancer
- `q` : quitter

Devrait marcher sur tous les OS, sauf peut-etre Windows.

---

Issu de cette video : https://www.youtube.com/watch?v=lziU_yT0iDc


---

[LICENSE MIT](./LICENSE.md)
