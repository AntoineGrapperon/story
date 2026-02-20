# Story Concepts Diagrams

This document illustrates core story concepts using Mermaid.js diagrams.

## 1. Narrative Arc (Activity Diagram)

This diagram visualizes the typical progression of a story, often referred to as Freytag's Pyramid.

```mermaid
graph TD
    A[Exposition] --> B{Inciting Incident};
    B -- Conflict Introduced --> C[Rising Action];
    C -- Increasing Tension --> D{Climax};
    D -- Turning Point --> E[Falling Action];
    E -- Resolution Approaches --> F[Resolution/Denouement];
```

## 2. Story Elements (Class Diagram)

This diagram shows the relationships between fundamental components of a story.

```mermaid
classDiagram
    Story "1" *-- "1" Plot : has
    Story "1" *-- "1..*" Character : features
    Story "1" *-- "1" Setting : occurs_in
    Story "1" *-- "1..*" Theme : explores
    Story "1" *-- "1..*" Conflict : driven_by

    Plot "1" *-- "5" PlotPoint : contains
    PlotPoint : Exposition
    PlotPoint : RisingAction
    PlotPoint : Climax
    PlotPoint : FallingAction
    PlotPoint : Resolution

    Character <|-- Protagonist
    Character <|-- Antagonist
    Character : +name
    Character : +motivations
    Character : +traits

    Protagonist "1" --> "1" Antagonist : opposes
    Protagonist "1" --> "1..*" Goal : seeks

    Conflict "1" *-- "2" Character : involves
    Conflict "1" *-- "1" Setting : may_involve
    Conflict "1" *-- "1" Theme : related_to

    Theme : +concept

    Setting : +time
    Setting : +place
    Setting : +atmosphere
```

## 3. Character Emotional Journey (State Machine Diagram)

This diagram illustrates a possible emotional progression for a character throughout a story.

```mermaid
stateDiagram-v2
    [*] --> Naive
    Naive --> Curious: experiences new things
    Curious --> Hopeful: discovers possibility
    Hopeful --> Determined: sets a goal
    Determined --> Struggling: faces obstacles
    Struggling --> Resigned: failure / loss
    Struggling --> Victorious: overcomes obstacles
    Resigned --> Reflective: processes event
    Victorious --> Content: achieves goal
    Reflective --> Transformed: new understanding
    Content --> Transformed: growth

    state Transformed {
        direction LR
        Transformed_Start: New Perspective
        Transformed_Start --> Wise: gains wisdom
        Transformed_Start --> Jaded: becomes cynical
    }
```