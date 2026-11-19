---
name: Bio-Synthetic Kinetic Telemetry
colors:
  surface: '#0f150f'
  surface-dim: '#0f150f'
  surface-bright: '#353b34'
  surface-container-lowest: '#0a0f0a'
  surface-container-low: '#181d17'
  surface-container: '#1c211b'
  surface-container-high: '#262b25'
  surface-container-highest: '#313630'
  on-surface: '#dfe4db'
  on-surface-variant: '#c2cab0'
  inverse-surface: '#dfe4db'
  inverse-on-surface: '#2c322c'
  outline: '#8c947c'
  outline-variant: '#424936'
  surface-tint: '#98da27'
  primary: '#ccff80'
  on-primary: '#213600'
  primary-container: '#a3e635'
  on-primary-container: '#416400'
  inverse-primary: '#446900'
  secondary: '#4edea3'
  on-secondary: '#003824'
  secondary-container: '#00a572'
  on-secondary-container: '#00311f'
  tertiary: '#bdffc2'
  on-tertiary: '#003915'
  tertiary-container: '#59ee81'
  on-tertiary-container: '#00692d'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#b2f746'
  primary-fixed-dim: '#98da27'
  on-primary-fixed: '#121f00'
  on-primary-fixed-variant: '#334f00'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#6bff8f'
  tertiary-fixed-dim: '#4ae176'
  on-tertiary-fixed: '#002109'
  on-tertiary-fixed-variant: '#005321'
  background: '#0f150f'
  on-background: '#dfe4db'
  surface-variant: '#313630'
typography:
  display-lg:
    fontFamily: Space Grotesk
    fontSize: 56px
    fontWeight: '700'
    lineHeight: 64px
    letterSpacing: -0.04em
  display-lg-mobile:
    fontFamily: Space Grotesk
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.03em
  headline-lg:
    fontFamily: Space Grotesk
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Space Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Space Grotesk
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Geist
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-lg:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '600'
    lineHeight: 18px
    letterSpacing: 0.08em
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.12em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 9px
    fontWeight: '700'
    lineHeight: 12px
    letterSpacing: 0.16em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-tablet: 1.25rem
  gutter-desktop: 1.5rem
  margin: 1rem
  margin-tablet: 1.5rem
  margin-desktop: 2.5rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style
The design system establishes a high-performance bio-digital automotive telemetry aesthetic. It merges brutalist technical precision with an organic cyberpunk undercurrent—evoking synthetic vitality, mechanical diagnostics, and hyper-calibrated vehicular intelligence.

The visual language draws heavily from high-contrast sci-fi heads-up displays (HUD), dark glassmorphic terminal architecture, and vector oscilloscopes. Interfaces are dense, intentional, and diagnostic. Elements communicate system readiness, live kinetic data, and raw bio-synthetic throughput without superfluous decorative fluff.

## Colors
The palette operates on absolute light-dark dichotomy: deep pitch-black foundations overlaid with obsidian and chlorite glass surfaces, electrified by acute radioactive lime highlights.

- **Primary (`#a3e635`)**: High-luminance acid lime. Reserved for active states, hyper-critical telemetry warnings, real-time kinetic needles, and luminescent focal points.
- **Secondary (`#10b981`)**: Bio-luminescent emerald green. Acts as the functional grounding hue for nominal system metrics, secondary data streams, and steady status indicators.
- **Tertiary (`#22c55e`)**: Vibrant synthetic green. Bridges intermediate diagnostic states, progress tracks, and secondary chart vectors.
- **Neutral (`#080d08`)**: Deep abyss matrix. Provides non-emissive surface isolation, preventing ambient eye fatigue while accentuating phosphorescent visual readouts.

Complementary surface tokens use `#050805` for root viewports, `#0d1810` for primary glass layer backings, and `#132417` for elevated interactive telemetry cells.

## Typography
The typographic hierarchy implements three distinct typefaces to separate computational data, structural labeling, and editorial telemetry readouts:

1. **Space Grotesk (Headlines & Display)**: Provides cold, geometric authority with slight optical anomalies fitting bio-mechanical interfaces.
2. **Geist (Body)**: Delivers surgical, modern neutral legibility for textual diagnostic logs and long-form data parameters.
3. **JetBrains Mono (Labels & Values)**: Strict monospaced clarity for sensor outputs, coordinate axes, speed readouts, and uppercase status flags. Always render labels with extended tracking (`letterSpacing`) to simulate digital terminal readouts.

## Layout & Spacing
The layout adheres to a rigid 12-column dense fluid grid structured around HUD cockpit layouts and mission-critical telemetry viewports.

- **Mobile (< 768px)**: 4-column flow. Primary vital clusters (e.g., speed, battery core, torque vector) stack linearly. Gutter is `1rem`, outer screen margins are `1rem`.
- **Tablet (768px - 1024px)**: 8-column layout. Gauges and system diagnostics run side-by-side with split-screen telemetry cards.
- **Desktop / In-Dash Display (> 1024px)**: Full 12-column telemetry dashboard. Left-to-right prioritization places critical kinetic gauges in the visual center, telemetry logs on the right flank, and navigation/environmental bio-sensors on the left.
- **Spacing Rhythm**: Internal component padding follows a strict 4px/8px baseline rhythm (`space-xs` through `space-xl`). Micro elements maintain compact spacing to sustain visual density.

## Elevation & Depth
Depth is created through dark obsidian glass surfaces and targeted neon luminescent blooming rather than drop shadows.

- **Level 0 (Canvas Base)**: Pitch black (`#050805`), completely matte, non-reflective.
- **Level 1 (Telemetry Panels & Pods)**: Translucent obsidian green (`#0d1810` at 80% opacity), with `backdrop-filter: blur(12px)` and a fine 1px structural outline of `#10b981` at 20% opacity.
- **Level 2 (Active Cards & Overlays)**: Elevated matrix containers (`#132417` at 90% opacity) encased in a 1px border of `#a3e635` at 40% opacity, paired with an ambient phosphorescent glow: `box-shadow: 0 0 16px -2px rgba(163, 230, 53, 0.15)`.
- **Level 3 (Alerts & Critical Modals)**: Glass tinted with `#10b981` at 15% mix, surrounded by an energized neon contour (`0 0 24px 2px rgba(163, 230, 53, 0.4)` and `border: 1px solid #a3e635`).

## Shapes
Corner geometry favors technical, calibrated hardness. Roundedness level `1` (0.25rem / 4px base) prevents organic softness from diluting the surgical automotive persona. 

- **Standard Containers**: 4px radius edges. Optionally, primary telemetry pods utilize chamfered or angled 45-degree technical corners (`clip-path: polygon(...)`) to simulate military HUD components.
- **Buttons & Control Tabs**: Precision cut 4px corners, maintaining an engineered feel.
- **Interactive Badges**: 2px corner micro-radii with 1px hairline borders.

## Components

### Buttons & Trigger Nodes
- **Primary Kinetic Action**: Background in `#a3e635`, text in `#050805` (Space Grotesk, Bold, Uppercase). When hovered or engaged, emit an outer lime bloom (`box-shadow: 0 0 16px rgba(163, 230, 53, 0.6)`) and scale up brightness.
- **Secondary Telemetry Action**: Glass fill (`#0d1810` / 80%), border 1px solid `#10b981`, typography in `#10b981` (JetBrains Mono). Hover triggers a subtle phosphor glow and `#a3e635` border shift.

### Telemetry Cards & Metric Pods
- Surface constructed with `#0d1810` glass, 1px border `#132417`. 
- Top-left corner houses a diagnostic index label (`label-sm`, e.g., `SYS.01 // TORQUE`), while numeric outputs dominate the interior in `display-lg` lime typography.
- Background displays an ultra-subtle grid or vector scanline texture (`rgba(34, 197, 94, 0.03)`).

### Input Fields & Command Prompts
- Background: Pitch black `#050805`.
- Border: 1px solid `#132417`. On focus, transitions cleanly to 1px `#a3e635` with `box-shadow: inset 0 0 6px rgba(163, 230, 53, 0.2)`.
- Text: Geist 14px in `#10b981` with blinking lime terminal caret.

### Checkboxes, Toggles & Switches
- **Toggle Tracks**: Pill track tinted `#0d1810` with 1px border `#10b981`. Active indicator slides right and turns `#a3e635` with a localized 8px blur ring.
- **Checkboxes**: Hard 2px rounded squares. Checked state shows an energetic bio-electric crosshair instead of an organic checkmark.

### Telemetry Gauges & Waveforms (Custom System Component)
- Multi-segment radial arc or horizontal bar split into discrete LED-like ticks.
- Inactive ticks render in muted forest slate (`#132417`); active ticks pulse progressively from `#10b981` up through `#a3e635` at dynamic thresholds.