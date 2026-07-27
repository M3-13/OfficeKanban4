# Design — Project Identity

> This document is project-long-lived. Tokens are not changed without
> the Architect's approval. Developers MUST use these tokens
> instead of improvising their own colors/spacings.

## Style Direction

Helles, minimalistisches Board mit kühlem Blau als Akzent. Ruhig, fokussiert, aufgeräumt – wie ein gut beleuchteter Schreibtisch. Angelehnt an Linear/Notion: reduzierte Farbpalette, dezente Schatten, klare Typografie, Farbakzente nur zur Orientierung.

## Colors

- `--color-bg`: **#FAFBFC**
- `--color-fg`: **#1A2332**
- `--color-accent`: **#3B6FF5**
- `--color-accent_hover`: **#2B5AD5**
- `--color-accent_active`: **#1E4ABF**
- `--color-border`: **#E1E5EB**
- `--color-muted`: **#6B7785**
- `--color-surface`: **#FFFFFF**
- `--color-surface_hover`: **#F4F6F9**
- `--color-surface_active`: **#EDF0F5**
- `--color-danger`: **#D94040**
- `--color-danger_hover`: **#C53030**
- `--color-success`: **#2E7D43**
- `--color-column_bg`: **#F0F3F7**
- `--color-card_shadow`: **0 1px 3px rgba(0,0,0,0.08)**

## Typography

- `font_family`: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif
- `heading_weight`: 600
- `body_weight`: 400
- `size_scale`: 12px/14px/16px/18px/22px/28px

## Spacing Scale

- `--space-0`: 4px
- `--space-1`: 8px
- `--space-2`: 12px
- `--space-3`: 16px
- `--space-4`: 20px
- `--space-5`: 24px
- `--space-6`: 32px
- `--space-7`: 48px

## Border-Radii

- `--radius-sm`: 4px
- `--radius-md`: 8px
- `--radius-lg`: 12px
- `--radius-pill`: 999px

## Components

### Button / Primary

bg=accent(#3B6FF5), fg=#FFFFFF, padding 8px 16px, radius=md(8px), font-weight=600, font-size=14px, min-height=44px (Touch), border=none. Hover: bg=accent_hover(#2B5AD5). Active: bg=accent_active(#1E4ABF), scale(0.97). Disabled: opacity=0.45, cursor=not-allowed, kein Hover-Effekt. Focus-visible: outline 2px solid accent, outline-offset 2px.

### Button / Secondary

bg=transparent, fg=accent(#3B6FF5), padding 8px 16px, radius=md(8px), font-weight=600, font-size=14px, min-height=44px, border=1px solid border(#E1E5EB). Hover: bg=surface_hover(#F4F6F9). Active: bg=surface_active(#EDF0F5). Disabled: opacity=0.45. Focus-visible: outline 2px solid accent, outline-offset 2px.

### Button / Danger

bg=danger(#D94040), fg=#FFFFFF, padding 8px 16px, radius=md(8px), font-weight=600, font-size=14px, min-height=44px, border=none. Hover: bg=danger_hover(#C53030). Active: scale(0.97). Disabled: opacity=0.45. Focus-visible: outline 2px solid danger.

### Button / Icon

bg=transparent, fg=muted(#6B7785), padding 6px, radius=sm(4px), min-dimensions=32x32px (Touch min 44px: zusätzlich 6px transparent padding), border=none, display=inline-flex, align=center, justify=center. Hover: bg=surface_hover(#F4F6F9), fg=fg(#1A2332). Active: bg=surface_active(#EDF0F5). Focus-visible: outline 2px solid accent.

### Card

bg=surface(#FFFFFF), padding 12px 16px, radius=md(8px), border=1px solid border(#E1E5EB), box-shadow=card_shadow, min-height=44px, cursor=grab, font-size=14px, line-height=1.5. Hover: border-color=muted(#6B7785), box-shadow='0 2px 6px rgba(0,0,0,0.12)'. Dragging: opacity=0.6, cursor=grabbing, box-shadow='0 4px 12px rgba(0,0,0,0.18)'. Card-Titel: font-weight=600, margin-bottom=4px. Card-Beschreibung: color=muted, font-size=12px.

### Column

bg=column_bg(#F0F3F7), padding 12px, radius=lg(12px), min-width=280px, max-width=340px, flex-shrink=0, display=flex, flex-direction=column, gap=8px. Column-Header: padding 4px 8px, font-weight=600, font-size=14px, color=fg(#1A2332), display=flex, align=center, justify=space-between, min-height=40px. Column-Card-List: flex=1, overflow-y=auto, display=flex, flex-direction=column, gap=8px, min-height=60px (Drop-Zone sichtbar). Drop-Zone-Highlight: bg leicht aufgehellt, border gestrichelt accent beim Drüberziehen.

### Board Header / Top Bar

bg=surface(#FFFFFF), padding 16px 24px, border-bottom=1px solid border(#E1E5EB), display=flex, align=center, justify=space-between, min-height=56px, position=sticky, top=0, z-index=10. Board-Titel: font-size=22px, font-weight=600, color=fg(#1A2332), editierbar mit Klick (wird zu Input). User-Badge rechts: Benutzername + Logout-Icon, font-size=14px, color=muted.

### Text Input

bg=surface(#FFFFFF), fg=fg(#1A2332), padding 8px 12px, radius=md(8px), border=1px solid border(#E1E5EB), font-size=14px, font-family=inherit, min-height=44px, width=100%, outline=none, transition=border-color 0.15s. Placeholder: color=muted(#6B7785), font-style=italic. Focus: border-color=accent(#3B6FF5), box-shadow='0 0 0 3px rgba(59,111,245,0.15)'. Error: border-color=danger(#D94040). Disabled: bg=column_bg, opacity=0.6.

### Modal / Dialog

Overlay: bg=rgba(0,0,0,0.4), position=fixed, inset=0, z-index=100, display=flex, align=center, justify=center. Dialog-Fenster: bg=surface(#FFFFFF), padding 24px, radius=lg(12px), max-width=480px, width=90vw, box-shadow='0 8px 32px rgba(0,0,0,0.18)'. Dialog-Titel: font-size=18px, font-weight=600, margin-bottom=16px. Dialog-Actions: display=flex, justify=flex-end, gap=8px, margin-top=24px.

### Login / Register Page

Zentrierte Card auf bg(#FAFBFC), max-width=400px, padding 32px, margin=auto, margin-top=15vh. Logo/Brand: 'OfficeKanban' Schriftzug, font-size=28px, font-weight=600, color=accent, text-align=center, margin-bottom=32px. Input-Felder: siehe Text-Input-Komponente, margin-bottom=16px. Submit-Button: volle Breite, siehe Button/Primary. Switch-Link ('Registrieren'/'Einloggen'): text-align=center, font-size=14px, color=accent, margin-top=16px, cursor=pointer.

### Board List (Dashboard)

Grid: display=grid, grid-template-columns=repeat(auto-fill, minmax(260px, 1fr)), gap=16px, padding 24px. Board-Card: bg=surface(#FFFFFF), padding 20px, radius=md(8px), border=1px solid border, cursor=pointer, min-height=100px, transition=box-shadow 0.15s. Hover: box-shadow='0 2px 8px rgba(0,0,0,0.1)'. Board-Titel: font-size=16px, font-weight=600. Board-Meta: font-size=12px, color=muted, margin-top=8px. 'Neues Board'-Karte: gestrichelter Rand, fg=muted, display=flex, align=center, justify=center, font-size=14px, hover wird zu durchgezogenem Rand + accent.

## Layout Principles

- Container max-width: 100% (Board scrollt horizontal), Content padding: 24px
- Breakpoints: <768px (Tablet/klein) Spalten untereinander statt nebeneinander, Kartenbreite flexibel; >=768px horizontales Scrollen der Spalten
- Kanban-Bereich: display=flex, gap=16px, padding 24px, overflow-x=auto, align-items=flex-start, min-height=calc(100vh - 56px - 48px) (abzgl. Topbar + Padding)
- Responsive Abstände: Content-Padding 24px auf Desktop, 16px auf Tablet (<768px)
- Z-index Staffel: Topbar=10, Dropdown/Overlay=50, Modal=100, Toast=200
- Touch-freundlich: alle interaktiven Elemente mindestens 44x44px Hit-Target
- Kartenbreite innerhalb Spalte: 100% der Spaltenbreite, kein horizontales Überlaufen
- Farbcodierung: Accent nur für primäre Aktionen und Fokus; Danger nur für destruktive Aktionen; Success für Status-Done-Indikatoren
- Animation: sanfte Übergänge (0.15s–0.2s ease) für Hover, Focus, Drag; kein übertriebenes Motion-Design
- Leerraum: großzügige Abstände zwischen Spalten (16px) und Karten (8px) – Luft zum Atmen, reduziert kognitive Last
