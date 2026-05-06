# Phonetic Card Battle

An offline educational mini-game built with **Python** and **Pygame** for learning English phonetics.

## Overview

Based on the textbook *"Bài giảng Ngữ âm và âm vị học tiếng Anh"* (Lecture on English Phonetics and Phonology), this game teaches the **44 English phonemes** through interactive card-sorting gameplay.

### Phoneme Inventory (Table 1 & Table 3)
| Category | Count | Examples |
|---|---|---|
| Consonants | 24 | /p/, /b/, /t/, /d/, /k/, /g/, /f/, /v/, /θ/, /ð/, /s/, /z/, /ʃ/, /ʒ/, /tʃ/, /dʒ/, /m/, /n/, /ŋ/, /h/, /l/, /r/, /j/, /w/ |
| Pure Vowels | 12 | /iː/, /ɪ/, /e/, /æ/, /ɑː/, /ɒ/, /ɔː/, /ʊ/, /uː/, /ʌ/, /ɜː/, /ə/ |
| Diphthongs | 8 | /eɪ/, /aɪ/, /ɔɪ/, /əʊ/, /aʊ/, /ɪə/, /eə/, /ʊə/ |

## Level 1 – Voicing Classification

Drag each **consonant phoneme card** into the correct zone:

- **Voiceless** – No vocal-cord vibration (e.g. /p/, /t/, /k/, /f/, /s/)
- **Voiced** – Vocal cords vibrate (e.g. /b/, /d/, /g/, /v/, /z/)
- **Nasal** – Air escapes through the nose (e.g. /m/, /n/, /ŋ/)

Incorrect placements pause the game and show a corrective explanation citing the phonetic properties from **Section 1.14** of the textbook.

## Requirements

- Python 3.8+
- Pygame 2.x

## Installation & Run

```bash
pip install pygame
python phonetic_battle.py
```

## Controls

- **Drag & Drop** – Move cards to zones
- **Click / Any Key** – Dismiss correction overlay
- **R** – Replay after completing the level
- **Q / Esc** – Quit

## Academic Reference

All phoneme data, classification, and corrective explanations are sourced from:
- *Table 3: English Consonant Phonemes* (Section 1.14)
- *Section 1.14.1 – Place of Articulation*
- *Section 1.14.2 – Manners of Articulation*
- *Section 1.14.3 – Voicing*
- *Section 1.15 – Pure Vowels*
- *Section 1.16 – Diphthongs*
