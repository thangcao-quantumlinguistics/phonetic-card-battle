"""
Phonetic Card Battle  –  Level 1: Voicing Classification
=========================================================
An offline educational mini-game built with Python / Pygame.

Phoneme inventory and classification strictly follow:
    "Bài giảng Ngữ âm và âm vị học tiếng Anh"
    Chapter 1 – Articulatory Phonetics
    Table 3: English Consonant Phonemes (Section 1.14)

44 English phonemes:
    24 consonants  ·  12 pure vowels (monophthongs)  ·  8 diphthongs

Level 1 asks the player to drag consonant cards into three zones:
    Voiceless  |  Voiced  |  Nasal
based on the voicing property from Table 3.

Incorrect placements pause the game and show a corrective explanation
citing the phonetic properties from Section 1.14.
"""

import pygame
import sys
import random
import textwrap

# ──────────────────────────────────────────────────────────────────────
# PHONEME DATA DICTIONARY  (extracted from PDF – Table 3, Sections 1.14–1.16)
# ──────────────────────────────────────────────────────────────────────

CONSONANTS = {
    # ── Plosives (Stops) ──────────────────────────────────────────────
    "p": {"place": "Bilabial",      "manner": "Plosive",      "voicing": "Voiceless",
          "example": "pen /pen/",
          "desc": "/p/ is a voiceless bilabial plosive (stop). The lips are pressed together "
                  "to shut off the oral cavity; the velum is raised to block the nasal cavity."},
    "b": {"place": "Bilabial",      "manner": "Plosive",      "voicing": "Voiced",
          "example": "bat /bæt/",
          "desc": "/b/ is a voiced bilabial plosive (stop). Produced like /p/ but with "
                  "vocal-cord vibration."},
    "t": {"place": "Alveolar",      "manner": "Plosive",      "voicing": "Voiceless",
          "example": "top /tɒp/",
          "desc": "/t/ is a voiceless alveolar plosive (stop). The tongue blade presses "
                  "against the alveolar ridge while the velum is raised."},
    "d": {"place": "Alveolar",      "manner": "Plosive",      "voicing": "Voiced",
          "example": "dog /dɒɡ/",
          "desc": "/d/ is a voiced alveolar plosive (stop). Produced like /t/ but with "
                  "vocal-cord vibration."},
    "k": {"place": "Velar",         "manner": "Plosive",      "voicing": "Voiceless",
          "example": "cat /kæt/",
          "desc": "/k/ is a voiceless velar plosive (stop). The tongue back presses "
                  "against the velum; the velum is raised."},
    "g": {"place": "Velar",         "manner": "Plosive",      "voicing": "Voiced",
          "example": "go /ɡəʊ/",
          "desc": "/g/ is a voiced velar plosive (stop). Produced like /k/ but with "
                  "vocal-cord vibration."},

    # ── Fricatives ────────────────────────────────────────────────────
    "f": {"place": "Labiodental",   "manner": "Fricative",    "voicing": "Voiceless",
          "example": "fan /fæn/",
          "desc": "/f/ is a voiceless labiodental fricative. The lower lip touches the "
                  "upper teeth, creating a narrow passage for the airflow."},
    "v": {"place": "Labiodental",   "manner": "Fricative",    "voicing": "Voiced",
          "example": "van /væn/",
          "desc": "/v/ is a voiced labiodental fricative. Produced like /f/ but with "
                  "vocal-cord vibration."},
    "θ": {"place": "Dental",        "manner": "Fricative",    "voicing": "Voiceless",
          "example": "think /θɪŋk/",
          "desc": "/θ/ is a voiceless dental (interdental) fricative. The tongue tip is "
                  "inserted between or touches behind the upper teeth."},
    "ð": {"place": "Dental",        "manner": "Fricative",    "voicing": "Voiced",
          "example": "this /ðɪs/",
          "desc": "/ð/ is a voiced dental (interdental) fricative. Produced like /θ/ but "
                  "with vocal-cord vibration."},
    "s": {"place": "Alveolar",      "manner": "Fricative",    "voicing": "Voiceless",
          "example": "sun /sʌn/",
          "desc": "/s/ is a voiceless alveolar fricative. The tongue blade approaches the "
                  "alveolar ridge, creating a narrow channel."},
    "z": {"place": "Alveolar",      "manner": "Fricative",    "voicing": "Voiced",
          "example": "zoo /zuː/",
          "desc": "/z/ is a voiced alveolar fricative. Produced like /s/ but with "
                  "vocal-cord vibration."},
    "ʃ": {"place": "Alveopalatal",  "manner": "Fricative",    "voicing": "Voiceless",
          "example": "ship /ʃɪp/",
          "desc": "/ʃ/ is a voiceless alveopalatal fricative. The tongue is raised towards "
                  "the back of the alveolar ridge and the front of the hard palate."},
    "ʒ": {"place": "Alveopalatal",  "manner": "Fricative",    "voicing": "Voiced",
          "example": "measure /ˈmeʒə/",
          "desc": "/ʒ/ is a voiced alveopalatal fricative. Produced like /ʃ/ but with "
                  "vocal-cord vibration."},
    "h": {"place": "Glottal",       "manner": "Fricative",    "voicing": "Voiceless",
          "example": "hat /hæt/",
          "desc": "/h/ is a voiceless glottal fricative. The vocal cords are drawn together "
                  "but the airflow is still strong enough to pass through the narrowed "
                  "glottis. Although classified as voiceless, /h/ is partly voiced before "
                  "a vowel (Section 1.14.3)."},

    # ── Affricates ────────────────────────────────────────────────────
    "tʃ": {"place": "Alveopalatal", "manner": "Affricate",    "voicing": "Voiceless",
           "example": "cheap /tʃiːp/",
           "desc": "/tʃ/ is a voiceless alveopalatal affricate. Formed by combining an "
                   "alveolar stop with a fricative; the tongue blade first presses against "
                   "then moves away from the back of the alveolar ridge (Section 1.14.2d)."},
    "dʒ": {"place": "Alveopalatal", "manner": "Affricate",    "voicing": "Voiced",
           "example": "judge /dʒʌdʒ/",
           "desc": "/dʒ/ is a voiced alveopalatal affricate. Produced like /tʃ/ but with "
                   "vocal-cord vibration. Both components share the same place (alveopalatal) "
                   "and voicing – they are homorganic (Section 1.14.2d)."},

    # ── Nasals ────────────────────────────────────────────────────────
    "m": {"place": "Bilabial",      "manner": "Nasal",        "voicing": "Voiced",
          "example": "man /mæn/",
          "desc": "/m/ is a voiced bilabial nasal. The lips are pressed together to shut "
                  "off the oral cavity; the velum is LOWERED so air escapes through the "
                  "nasal cavity (Section 1.14.2b)."},
    "n": {"place": "Alveolar",      "manner": "Nasal",        "voicing": "Voiced",
          "example": "no /nəʊ/",
          "desc": "/n/ is a voiced alveolar nasal. The tongue blade presses against the "
                  "alveolar ridge; the velum is lowered so air escapes through the nose "
                  "(Section 1.14.2b)."},
    "ŋ": {"place": "Velar",         "manner": "Nasal",        "voicing": "Voiced",
          "example": "sing /sɪŋ/",
          "desc": "/ŋ/ is a voiced velar nasal. The tongue back presses against the velum; "
                  "the velum is lowered so air escapes through the nose (Section 1.14.2b)."},

    # ── Approximants ──────────────────────────────────────────────────
    "l": {"place": "Alveolar",      "manner": "Approximant",  "voicing": "Voiced",
          "example": "low /ləʊ/",
          "desc": "/l/ is a voiced alveolar lateral approximant. The tongue tip is raised "
                  "to the alveolar ridge but the sides of the tongue are down, permitting "
                  "air to escape laterally (Section 1.14.2e)."},
    "r": {"place": "Alveopalatal",  "manner": "Approximant",  "voicing": "Voiced",
          "example": "red /red/",
          "desc": "/r/ is a voiced alveopalatal (post-alveolar) approximant. Produced by "
                  "curling the tongue tip back behind the alveolar ridge – a retroflex "
                  "articulation (Section 1.14.2e)."},
    "j": {"place": "Palatal",       "manner": "Approximant",  "voicing": "Voiced",
          "example": "yes /jes/",
          "desc": "/j/ is a voiced palatal approximant (glide/semi-vowel). The tongue front "
                  "is raised towards the hard palate; it glides rapidly from the position "
                  "of /iː/ or /ɪ/ to the following vowel (Section 1.14.2e)."},
    "w": {"place": "Bilabial/Velar","manner": "Approximant",  "voicing": "Voiced",
          "example": "well /wel/",
          "desc": "/w/ is a voiced bilabial-velar approximant (glide/semi-vowel). The lips "
                  "are rounded (bilabial) and the tongue back is raised towards the velum "
                  "(velar). It glides rapidly from /uː/ or /ʊ/ to the following vowel "
                  "(Section 1.14.2e)."},
}

# 12 Pure vowels (Section 1.15)
PURE_VOWELS = {
    "iː": {"height": "High",    "part": "Front",   "length": "Long/Tense",   "rounding": "Unrounded",
            "example": "beat /biːt/"},
    "ɪ":   {"height": "High",    "part": "Front",   "length": "Short/Lax",    "rounding": "Unrounded",
            "example": "bit /bɪt/"},
    "e":   {"height": "Mid",     "part": "Front",   "length": "Short/Lax",    "rounding": "Unrounded",
            "example": "bet /bet/"},
    "æ":   {"height": "Low",     "part": "Front",   "length": "Short/Lax",    "rounding": "Unrounded",
            "example": "bat /bæt/"},
    "ɑː":  {"height": "Low",     "part": "Back",    "length": "Long/Tense",   "rounding": "Unrounded",
            "example": "bar /bɑː/"},
    "ɒ":   {"height": "Low",     "part": "Back",    "length": "Short/Lax",    "rounding": "Rounded",
            "example": "lot /lɒt/"},
    "ɔː":  {"height": "Mid",     "part": "Back",    "length": "Long/Tense",   "rounding": "Rounded",
            "example": "bought /bɔːt/"},
    "ʊ":   {"height": "High",    "part": "Back",    "length": "Short/Lax",    "rounding": "Rounded",
            "example": "book /bʊk/"},
    "uː":  {"height": "High",    "part": "Back",    "length": "Long/Tense",   "rounding": "Rounded",
            "example": "boot /buːt/"},
    "ʌ":   {"height": "Low-Mid", "part": "Central", "length": "Short/Lax",    "rounding": "Neutral",
            "example": "but /bʌt/"},
    "ɜː":  {"height": "Mid",     "part": "Central", "length": "Long/Tense",   "rounding": "Neutral",
            "example": "bird /bɜːd/"},
    "ə":   {"height": "Mid",     "part": "Central", "length": "Short/Lax",    "rounding": "Neutral",
            "example": "about /əˈbaʊt/"},
}

# 8 Diphthongs (Section 1.16)
DIPHTHONGS = {
    "ɪə": {"type": "Centring",  "glide": "→ ə",  "example": "beard /bɪəd/"},
    "eə": {"type": "Centring",  "glide": "→ ə",  "example": "air /eə/"},
    "ʊə": {"type": "Centring",  "glide": "→ ə",  "example": "tour /tʊə/"},
    "eɪ": {"type": "Closing",   "glide": "→ ɪ",  "example": "face /feɪs/"},
    "aɪ": {"type": "Closing",   "glide": "→ ɪ",  "example": "fly /flaɪ/"},
    "ɔɪ": {"type": "Closing",   "glide": "→ ɪ",  "example": "boy /bɔɪ/"},
    "əʊ": {"type": "Closing",   "glide": "→ ʊ",  "example": "go /ɡəʊ/"},
    "aʊ": {"type": "Closing",   "glide": "→ ʊ",  "example": "how /haʊ/"},
}

# ──────────────────────────────────────────────────────────────────────
# GAME ZONE MAPPING  (Level 1 – Voicing classification)
# Based on Table 3 and Section 1.14.3
# ──────────────────────────────────────────────────────────────────────

VOICING_ZONE = {}
for sym, info in CONSONANTS.items():
    if info["manner"] == "Nasal":
        VOICING_ZONE[sym] = "Nasal"
    elif info["voicing"] == "Voiceless":
        VOICING_ZONE[sym] = "Voiceless"
    else:
        VOICING_ZONE[sym] = "Voiced"

# ──────────────────────────────────────────────────────────────────────
# PYGAME CONSTANTS
# ──────────────────────────────────────────────────────────────────────

WIDTH, HEIGHT = 1280, 720
FPS = 60

# Palette — minimalist academic aesthetic
BG_COLOR       = (245, 243, 240)   # warm off-white
CARD_COLOR     = (255, 255, 255)
CARD_BORDER    = (60,  60,  60)
CARD_DRAG      = (230, 240, 255)
ZONE_COLORS    = {
    "Voiceless": (200, 220, 255),   # cool blue
    "Voiced":    (200, 255, 210),   # soft green
    "Nasal":     (255, 220, 200),   # warm peach
}
ZONE_BORDER    = {
    "Voiceless": (100, 140, 200),
    "Voiced":    (80,  170, 100),
    "Nasal":     (200, 130,  80),
}
CORRECT_FLASH  = (150, 220, 150)
WRONG_FLASH    = (240, 120, 120)
TEXT_COLOR      = (30,  30,  30)
SUBTITLE_COLOR = (100, 100, 100)
OVERLAY_BG     = (20,  20,  20, 210)
WHITE          = (255, 255, 255)

CARD_W, CARD_H = 110, 70
ZONE_W, ZONE_H = 340, 340
ZONE_Y         = 320
ZONE_GAP       = 40
ZONE_X_START   = (WIDTH - 3 * ZONE_W - 2 * ZONE_GAP) // 2

# ──────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────

def try_fonts(names, size, bold=False):
    """Try a list of font names; fall back to default."""
    for name in names:
        font = pygame.font.SysFont(name, size, bold=bold)
        if font:
            return font
    return pygame.font.SysFont(None, size, bold=bold)


def wrap_text(text, font, max_width):
    """Word-wrap text to fit within max_width pixels."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_rounded_rect(surface, rect, color, radius=12, border=0, border_color=None):
    """Draw a rounded rectangle."""
    r = pygame.Rect(rect)
    pygame.draw.rect(surface, color, r, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surface, border_color, r, width=border, border_radius=radius)


# ──────────────────────────────────────────────────────────────────────
# CARD CLASS
# ──────────────────────────────────────────────────────────────────────

class Card:
    def __init__(self, symbol, x, y):
        self.symbol = symbol
        self.rect = pygame.Rect(x, y, CARD_W, CARD_H)
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.home_x = x
        self.home_y = y
        self.placed = False      # successfully placed in correct zone
        self.flash_timer = 0
        self.flash_color = None

    def draw(self, surface, font_ipa, font_small):
        if self.placed:
            return

        color = CARD_DRAG if self.dragging else CARD_COLOR
        if self.flash_timer > 0:
            color = self.flash_color

        shadow_rect = self.rect.move(3, 3)
        draw_rounded_rect(surface, shadow_rect, (200, 200, 200), radius=10)
        draw_rounded_rect(surface, self.rect, color, radius=10, border=2, border_color=CARD_BORDER)

        # IPA symbol
        sym_surf = font_ipa.render(f"/{self.symbol}/", True, TEXT_COLOR)
        sym_rect = sym_surf.get_rect(center=(self.rect.centerx, self.rect.centery - 8))
        surface.blit(sym_surf, sym_rect)

        # Manner label
        info = CONSONANTS[self.symbol]
        lbl = font_small.render(info["manner"], True, SUBTITLE_COLOR)
        lbl_rect = lbl.get_rect(center=(self.rect.centerx, self.rect.centery + 18))
        surface.blit(lbl, lbl_rect)

    def update(self, dt):
        if self.flash_timer > 0:
            self.flash_timer -= dt
            if self.flash_timer <= 0:
                self.flash_timer = 0

    def snap_home(self):
        self.rect.x = self.home_x
        self.rect.y = self.home_y


# ──────────────────────────────────────────────────────────────────────
# MAIN GAME
# ──────────────────────────────────────────────────────────────────────

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Phonetic Card Battle — Level 1: Voicing")
    clock = pygame.time.Clock()

    # Fonts — prefer fonts with good IPA coverage
    ipa_candidates = [
        "DejaVu Sans", "DejaVuSans", "dejavu sans",
        "Noto Sans", "NotoSans", "noto sans",
        "Liberation Sans", "liberationsans",
        "FreeSans", "freesans",
        "Arial Unicode MS", "Arial",
        "Segoe UI", "Ubuntu",
    ]
    font_ipa     = try_fonts(ipa_candidates, 28, bold=True)
    font_title   = try_fonts(ipa_candidates, 36, bold=True)
    font_small   = try_fonts(ipa_candidates, 16)
    font_zone    = try_fonts(ipa_candidates, 22, bold=True)
    font_zone_sm = try_fonts(ipa_candidates, 15)
    font_info    = try_fonts(ipa_candidates, 20)
    font_info_sm = try_fonts(ipa_candidates, 17)
    font_score   = try_fonts(ipa_candidates, 20, bold=True)
    font_overlay_title = try_fonts(ipa_candidates, 30, bold=True)

    # Build card deck (all 24 consonants, shuffled)
    symbols = list(CONSONANTS.keys())
    random.shuffle(symbols)

    # Deal cards in rows along the top
    cards = []
    cards_per_row = 12
    x_margin = 40
    y_start = 70
    x_spacing = (WIDTH - 2 * x_margin) // cards_per_row
    for i, sym in enumerate(symbols):
        row = i // cards_per_row
        col = i % cards_per_row
        cx = x_margin + col * x_spacing + (x_spacing - CARD_W) // 2
        cy = y_start + row * (CARD_H + 12)
        cards.append(Card(sym, cx, cy))

    # Zone rects
    zones = {}
    zone_names = ["Voiceless", "Voiced", "Nasal"]
    for i, name in enumerate(zone_names):
        zx = ZONE_X_START + i * (ZONE_W + ZONE_GAP)
        zones[name] = pygame.Rect(zx, ZONE_Y, ZONE_W, ZONE_H)

    # Zone placed-card tracking
    zone_placed = {"Voiceless": [], "Voiced": [], "Nasal": []}

    # Game state
    score = 0
    total = len(symbols)
    dragging_card = None
    show_overlay = False
    overlay_text_lines = []
    overlay_symbol = ""
    overlay_correct_zone = ""
    game_complete = False

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # ── Overlay dismiss ───────────────────────────────────
            if show_overlay:
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                    show_overlay = False
                continue

            # ── Win-screen dismiss ────────────────────────────────
            if game_complete:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Restart
                        return main()
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        running = False
                continue

            # ── Mouse events ──────────────────────────────────────
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                # Pick up topmost non-placed card under cursor
                for card in reversed(cards):
                    if not card.placed and card.rect.collidepoint(mx, my):
                        card.dragging = True
                        card.offset_x = card.rect.x - mx
                        card.offset_y = card.rect.y - my
                        dragging_card = card
                        # Move to top of draw order
                        cards.remove(card)
                        cards.append(card)
                        break

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if dragging_card:
                    dragging_card.dragging = False
                    dropped_in_zone = None
                    for zname, zrect in zones.items():
                        if dragging_card.rect.colliderect(zrect):
                            dropped_in_zone = zname
                            break

                    if dropped_in_zone:
                        correct_zone = VOICING_ZONE[dragging_card.symbol]
                        if dropped_in_zone == correct_zone:
                            # Correct!
                            dragging_card.placed = True
                            dragging_card.flash_color = CORRECT_FLASH
                            dragging_card.flash_timer = 0.4
                            zone_placed[correct_zone].append(dragging_card.symbol)
                            score += 1
                            if score == total:
                                game_complete = True
                        else:
                            # Wrong — show corrective overlay
                            dragging_card.flash_color = WRONG_FLASH
                            dragging_card.flash_timer = 0.6
                            dragging_card.snap_home()

                            info = CONSONANTS[dragging_card.symbol]
                            show_overlay = True
                            overlay_symbol = dragging_card.symbol
                            overlay_correct_zone = correct_zone
                            overlay_text_lines = [
                                f"/{dragging_card.symbol}/ belongs to the {correct_zone.upper()} zone.",
                                "",
                                f"Place: {info['place']}   |   Manner: {info['manner']}   |   Voicing: {info['voicing']}",
                                f"Example: {info['example']}",
                                "",
                                info["desc"],
                                "",
                                "(Section 1.14 – Consonants, Table 3)",
                                "",
                                "Click or press any key to continue."
                            ]
                    else:
                        dragging_card.snap_home()

                    dragging_card = None

            elif event.type == pygame.MOUSEMOTION:
                if dragging_card:
                    mx, my = event.pos
                    dragging_card.rect.x = mx + dragging_card.offset_x
                    dragging_card.rect.y = my + dragging_card.offset_y

            # Keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # ── Update ────────────────────────────────────────────────
        for card in cards:
            card.update(dt)

        # ── Draw ──────────────────────────────────────────────────
        screen.fill(BG_COLOR)

        # Title bar
        title_surf = font_title.render("Phonetic Card Battle", True, TEXT_COLOR)
        screen.blit(title_surf, (20, 14))

        subtitle = font_small.render(
            "Level 1 — Drag each consonant card to the correct voicing zone (Table 3, Section 1.14)",
            True, SUBTITLE_COLOR
        )
        screen.blit(subtitle, (20, 52))

        # Score
        score_surf = font_score.render(f"Score: {score} / {total}", True, TEXT_COLOR)
        screen.blit(score_surf, (WIDTH - score_surf.get_width() - 24, 20))

        # Drop zones
        for zname, zrect in zones.items():
            # Background
            draw_rounded_rect(screen, zrect, ZONE_COLORS[zname], radius=14,
                              border=3, border_color=ZONE_BORDER[zname])

            # Zone title
            zt = font_zone.render(zname, True, ZONE_BORDER[zname])
            screen.blit(zt, (zrect.centerx - zt.get_width() // 2, zrect.y + 10))

            # Zone description
            if zname == "Voiceless":
                desc = "No vocal-cord vibration"
            elif zname == "Voiced":
                desc = "Vocal cords vibrate"
            else:
                desc = "Air escapes through the nose"
            zd = font_zone_sm.render(desc, True, SUBTITLE_COLOR)
            screen.blit(zd, (zrect.centerx - zd.get_width() // 2, zrect.y + 38))

            # Placed symbols
            placed = zone_placed[zname]
            if placed:
                cols = 5
                sx = zrect.x + 14
                sy = zrect.y + 62
                for idx, psym in enumerate(placed):
                    pr = idx // cols
                    pc = idx % cols
                    px = sx + pc * 62
                    py = sy + pr * 32
                    ps = font_info_sm.render(f"/{psym}/", True, TEXT_COLOR)
                    screen.blit(ps, (px, py))

        # Cards
        for card in cards:
            card.draw(screen, font_ipa, font_small)

        # ── Corrective overlay ────────────────────────────────────
        if show_overlay:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill(OVERLAY_BG)
            screen.blit(overlay, (0, 0))

            box_w, box_h = 750, 400
            box_x = (WIDTH - box_w) // 2
            box_y = (HEIGHT - box_h) // 2
            box_rect = pygame.Rect(box_x, box_y, box_w, box_h)
            draw_rounded_rect(screen, box_rect, (250, 245, 240), radius=16,
                              border=3, border_color=WRONG_FLASH)

            # Title
            ot = font_overlay_title.render("Incorrect!", True, (200, 60, 60))
            screen.blit(ot, (box_x + (box_w - ot.get_width()) // 2, box_y + 18))

            # Text
            ty = box_y + 65
            max_tw = box_w - 50
            for line in overlay_text_lines:
                if line == "":
                    ty += 10
                    continue
                wrapped = wrap_text(line, font_info_sm, max_tw)
                for wl in wrapped:
                    ls = font_info_sm.render(wl, True, TEXT_COLOR)
                    screen.blit(ls, (box_x + 25, ty))
                    ty += 24

        # ── Win screen ────────────────────────────────────────────
        if game_complete:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((20, 60, 20, 200))
            screen.blit(overlay, (0, 0))

            win_t = font_title.render("Level 1 Complete!", True, WHITE)
            screen.blit(win_t, ((WIDTH - win_t.get_width()) // 2, HEIGHT // 2 - 60))

            win_s = font_info.render(
                f"You correctly classified all {total} consonants!", True, WHITE
            )
            screen.blit(win_s, ((WIDTH - win_s.get_width()) // 2, HEIGHT // 2))

            win_h = font_info_sm.render(
                "Press R to replay  |  Press Q or Esc to quit", True, (200, 255, 200)
            )
            screen.blit(win_h, ((WIDTH - win_h.get_width()) // 2, HEIGHT // 2 + 45))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
