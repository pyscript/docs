# Theme B: The JavaScript and browser boundary is where we lose people

## What it is

The Python/JavaScript interface, the FFI, complex worker
semantics, debugging across the two runtimes, and the browser's security model.
The place where a Python programmer's reasonable expectations become lost in
the unfamiliar and mysterious platform that is the browser. They are used to
being knowledgeable and productive but suddenly find themselves in confusing,
unfamiliar territory. The result is a feeling of disempowerment and loss of
agency.

## What it means for PyScript

This is the most important retention finding in
the whole set. We convert well on the easy case and lose people at the next
step, and the drop-off is concentrated at this point. Łukasz, an expert
engineer, articulated the pattern he hears repeatedly from other Python
developers: they try PyScript, "it works for something simple, it didn't work
for something else, I didn't know what to do." He is candid that his own
fluency is survivorship: he has learned to "avoid the rough edges, not because
they're no longer there, just because you know to avoid them." He described the
specific pain of debugging across two runtimes: the JavaScript debugger does
not step into PyScript code, and PyScript debugging techniques do not step into
JavaScript.

The boundary shows up differently for different users. Hammad, an educator,
does not want to see it at all: "I know in your docs, it's like `import ffi`.
To me, I'm sitting there being like... there's more of a layer [that] can go on
top." Nitau, an engineer, hit a concrete limitation trying to extend web
classes (a custom `div` subclass) and found the translation into JavaScript
got in the way. Sai, an informatician, spends most of his time fighting the
framework-integration case (PyScript inside React or Next.js) and worker
headers, and reported non-deterministic runtime readiness: "when the agent
starts and spits out the Python code, sometimes it's flaky, sometimes the
runtime is not ready." Mark, a veteran engineer, wanted a straightforward path
to integrate arbitrary WASM modules such as ammo.js and found none.

The Tufts case study names an additional problem in a particularly concrete
and actionable way. Reduced to essentials, what PyScript.com provides that
plain GitHub Pages hosting cannot is three capabilities: channels (sharing
information between pages over WebSockets), an API proxy (so a secret key such
as one for ChatGPT is never exposed), and authorisation (so a hosted project is
restricted to approved people or domains). Ethan was precise about why the
proxy and authorisation matter together: an open project means "anyone can be
using my chatbot, and then that's, of course, attached to my credit card."
These are not abstractions about "the JS boundary"; they are tangible
capabilities that, once a project needs more than to run by itself, push a user
off GitHub Pages and back towards a service. They are also the natural shape of
a self-hostable tool (see [Theme D](./onboarding_path.md) and the [case study](./case_study.md)).

## Future steps

This deserves dedicated attention. Concretely: (1) a
migration-style tutorial series aimed at Python programmers crossing the
boundary, showing the wrong way and then the right way, which Łukasz explicitly
asked for; (2) clearer, awaitable runtime-ready semantics and documented
patterns for framework integration and worker headers, drawing on Sai's
deployment experience; (3) better cross-runtime debugging guidance; (4) a
documented recipe for integrating third-party WASM modules, per Mark. Several
of these are documentation and example problems as much as engineering ones,
which makes them quickly tractable.

## Standing across archetypes

This is the engineers' and informaticians'
theme above all. Educators want the boundary hidden entirely; engineers want it
made navigable.

## Challenges

The browser platform itself is the constraint. Workers,
response headers, security policies and the FFI are inherent complexities of
the web, not defects we can engineer away. Our room for action is limited to
education, documentation, abstraction through frameworks (Invent) and API
smoothing (the built-in `pyscript` namespace): we can make the boundary
navigable, but we cannot remove it.