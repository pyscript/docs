# Theme C: Packages, stability and error messages

## What it is

Three linked practical blockers: which packages work
(especially C-dependent ones), how stable the platform stays over time, and
whether error messages explain themselves.

## What it means for PyScript

These are the day-to-day friction points that
turn an ambitious first project into a curtailed one. Kattni, an educator,
came in with an ambitious idea, hit a C-dependent package, and had to retreat
to "something much more within my wheelhouse." The deeper problem was silence:
"none of the error messages implied this library is not supported. It was
failing in weird ways." We have already responded to exactly this with
[packages.pyscript.net](https://packages.pyscript.net/) and with improved,
documented error messages. Worth noting: this was a direct result of earlier
feedback from Kattni to Dan Yeaw (our previous PyScript engineering manager).

On stability, Hammad, an educator, made the strongest case for valuing
continuity over novelty. Drawing a finance analogy about teams staying on old
Excel versions, he argued "the most valuable thing is your own time when you've
set it up," and was wary of Pyodide's deprecations and release cadence. He
admired the Xeus Python model of a self-contained conda environment where "the
package [is there] and it works."

On error messages, the newcomer experience is stark. Anna, a learner, reads
only the line "that looks important", ignoring everything else. She routinely
pastes errors she cannot parse into an LLM "to figure out what it's trying to
say." Her suggestion was simple: she would read an error "if there was an
explanation of what it's trying to tell me."

## Future steps

Continue the compatibility-checking and error-message work
already begun. Consider surfacing package compatibility earlier and more
loudly, so an unsupported package fails with an explanation rather than in
"weird ways." Encourage and surface the stability and long-term-support story
for self-hosted and educational contexts, where the pinned, known-good
environment is worth more than the latest versions. On error messages,
prioritise a plain-language explanatory layer on the most common errors, since
this helps beginners directly and also improves what LLMs echo back
([Theme E](./ai_default.md)).

## Standing across archetypes

Educators and learners feel this most deeply.
Engineers tend to route around it; Sai and Łukasz, for example, compile their
own wheels when needed.

## Challenges

Package availability is largely upstream: PyScript depends on
Pyodide for its packaging story, so compatibility and version churn are only
partially within our control. Error reporting is deeply embedded in how
PyScript works, making clearer errors a significant engineering effort rather
than a quick fix.