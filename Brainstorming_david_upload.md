# Blaupause: Iterative Segmentierungspipeline für Uveitis-OCT/OCTA

## Zielse:

Ziel des Projekts ist der Aufbau robuster, reproduzierbarer *semantischer Segmentierungen für strukturelle und krankheitsrelevante Bildmanifestationen bei Uveitis* auf OCT/OCTA-Daten.  

einzelne Modelle, die mehrere Sturkuren segmentieren stellen, insbesondere in den frühen Phasen des Projektes die Gefahr dar, sich in komplizierte Traininsmethoden zu verstricken - daher:

DEs wird bewusst **nicht** der Ansatz verfolgt, ein einzelnes Modell zu trainieren, das alle relevanten Strukturen gleichzeitig segmentiert. Stattdessen wird eine **modulare Pipeline aus mehreren spezialisierten Modellen** entwickelt, die jeweils klar definierte anatomische oder pathologische Zielstrukturen adressieren.


Vorteile:
- unterschiedliche Strukturen weisen stark unterschiedliche Bildcharakteristika auf,
- Annotationen werden klarer und konsistenter,
- Fehlerquellen lassen sich besser analysieren,
- Modelle bleiben austauschbar, erweiterbar, EVALUATION MÖGLICH
- Brainstorm charakter ebenso in der Annotation der Ground truth (intra- inter- observer var. überprüfbar / technisch sauberer)

---

## Einstiegsstrukturen

Als Einstieg werden zwei Strukturen gewählt, die sich besonders gut für eine iterative Pipeline-Entwicklung eignen:

### 1. Retinal Pigment Epithelium (RPE)

Die RPE-Grenze ist in OCT-Bildern in der Regel gut sichtbar und vergleichsweise eindeutig definierbar.  
Sie eignet sich daher gut für:
- initiale Modellvalidierung,
- Interobserver-Vergleiche,
- Definition stabiler Referenzlinien für spätere geometrische Marker (z. B. Thickness-Maße).

### 2. Vitreal Area / Vitreous Space

Die Vitreous-Region ist im Kontext von Uveitis klinisch relevant  ebenso stellt sie die Abgrenzung der Retina zum VIT dar, weist jedoch wesentlich andere Signalcharakteristika auf als retinale Grenzflächen.  
Sie erlaubt:
- die Ableitung krankheitsrelevanter Bildmarker (z. B. Vitreous haze)
- frühe Auseinandersetzung mit Feature-Engineering jenseits reiner Segmentierung,
- Prüfung der Pipeline-Flexibilität bei sehr unterschiedlichen Zielstrukturen (im vergleich zu RPE -> Evaluationsdimension)

---

## Mehrwert der kombinierten Segmentierung

Durch die getrennte Segmentierung von RPE und Vitreous lassen sich bereits in einer frühen Projektphase mehrere zentrale Bausteine ableiten:

- Definition einer konsistenten **Retina-Region of Interest (ROI)**  
- Berechnung erster **Thickness-basierter Marker**  
- Quantitative Analyse des **Vitreous Signals** als Proxy für Inflammation  
- Grundlage für späteres standardisiertes **Cropping der Retina**, für nachgelagerte Layer-Segmentierungen dient  

Damit entsteht früh ein funktionaler Analyse-Workflow, der nicht auf perfekte Multi-Layer-Segmentierungen angewiesen ist.

---

## Modellansatz

Für jede Zielstruktur wird ein eigenes **nnU-Net-Modell** trainiert:

- **Modell A:** RPE-Segmentierung  
- **Modell B:** Vitreal Area-Segmentierung  

Die resultierenden Segmentierungen werden anschließend regelbasiert zusammengeführt, um geometrische Konsistenz sicherzustellen und robuste ROIs für die Markerberechnung zu erzeugen.

---

## Workflow pro Modell

### Datengrundlage
- Kombination aus öffentlichen und internen OCT/OCTA-Datensätzen
- Harmonisierung von Formaten, Auflösung und Metadaten
- Strikte Aufteilung in Trainings-, Validierungs- und Testdatensätze  

### Annotation
- ca. 100 Bilder pro Modell für Training/Validierung
- Annotation durch 2–3 Personen
-  Interobserver-Anteil zur Abschätzung der menschlichen Variabilität

### Training
- nnU-Net-Training mit task-spezifischer Konfiguration
- Dokumentation von:
  - Rechenaufwand (GPU/CPU, Zeit, Speicher) -> welches cluster können wir überhaupt nutzen 
  - Preprocessing-Schritten

### Evaluation
- klassische Segmentierungsmetriken (Dice, IoU)
- oberflächenbasierte Metriken (z. B. Hausdorff95)
- (Subgruppenanalysen (Gerät, Bildqualität, Krankheitsausprägung)) -> wahrscheinlich erst später 

### Zusammenführung der Segmentierungen
- regelbasierte Konsistenzprüfungen (z. B. anatomische Reihenfolge)
- Postprocessing nur dort, wo biologisch sinnvoll -> Absprache mit David 
- Qualitätskontrollen und Plausibilitätschecks

### Biomarker-Ableitung
- Retina-ROI-Extraktion
- Thickness-bezogene Features
- Vitreous-Intensity- und Texturmerkmale
- (Stabilität gegenüber Bildqualität und Scanvarianten)

---

## Erkenntnis:

Der Fokus liegt nicht ausschließlich auf maximaler Segmentierungsperformance, sondern auf:

- Vergleich von Modellleistung vs. Interobserver-Grenze
- Generalisierbarkeit zwischen Datensätzen
- Annotation- vs. Compute-Aufwand
- Stabilität und Interpretierbarkeit der abgeleiteten Bildmarker

Für mich wichtig zu verstehen **welche Segmentierungsqualität für klinisch sinnvolle Marker tatsächlich erforderlich ist**

---


Wenn sich der Ansatz bewährt, kann die Pipeline schrittweise erweitert werden:

- Layer-Segmentierung auf standardisierten Retina-ROIs
- zusätzliche uveitisrelevante Manifestationen als eigene Modelle
- Integration weiterer Modalitäten (z. B. OCTA)


