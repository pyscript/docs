# 6. Conclusion and next steps

The headline is encouraging and directive in equal measure. PyScript's core
proposition, friction-free Python in the browser, is genuinely loved and is
working ([Theme A](./friction_free.md)). The recent engineering and documentation work is landing.
The clearest risks are not that people dislike PyScript, but that
PyScript.com's reliability is actively disrupting the teaching of our closest
institutional partners, that we win people on the easy case and lose them at
the JavaScript and browser boundary ([Theme B](./js_boundary.md)), and that too few people know
PyScript exists at all ([Theme F](./visibility.md)).

## Next steps

The following next steps map onto the themes. They are proposed in the
interests of discussion, not as explicit commitments: each requires
refinement based on evidence and feedback.

### 1. Target the boundary drop-off

**([Theme B](./js_boundary.md))**

Commission a migration-style
tutorial series for Python programmers, showing the wrong way then the right
way across the FFI, workers and debugging. Tighten runtime-ready semantics
and framework-integration and header documentation. This is the single
highest-leverage retention move.

### 2. Invest in demos and remixable examples

**(Themes [A](./friction_free.md), [C](./packages_stability_errors.md), [D](./onboarding_path.md))**

Treat idiomatic, tear-apart-and-recombine examples as a primary onboarding
surface. This directly addresses the blank page problem and gives learners
and educators something to start from.

### 3. Finish the compatibility and error-message work, and add a stability story

**([Theme C](./packages_stability_errors.md))**

Surface package compatibility earlier and more loudly, add a
plain-language explanatory layer to common errors, and investigate a pinned,
long-term-support environment for educational and self-hosted use.

### 4. Make PyScript an excellent citizen of the LLM ecosystem 

**([Theme E](./ai_default.md))**

Treat how our docs, API and examples are consumed by LLMs as a first-class
problem; fix version-awareness in generated code; and keep a fully supported
AI-free path. Hold no single house line on AI in our external-facing
communication.

### 5. Get Invent to an early release and validate it against real users

**(Themes [A](./friction_free.md), [D](./onboarding_path.md), [E](./ai_default.md))**

Hammad described Invent unprompted - an encouraging signal. Aim
for an alpha in Q2 2026 and put it in front of Hammad, Mark and others for
iterative feedback, designing to Mark's migratability test.

### 6. Fix PyScript.com reliability, and ship the self-hostable tool

**(Themes [A](./friction_free.md), [B](./js_boundary.md), [D](./onboarding_path.md), [F](./visibility.md))**

Two parallel tracks, and a decision. Immediately, track down and
repair the underlying PyScript.com reliability problem, since it is
disrupting a named institutional partner's teaching now. In parallel, take
TuftsHub to a named, pip-installable PyPI release providing channels, the
API proxy and authorisation for local-first and self-hosted use, developed
in the open under the Tufts organisation. And decide, deliberately, whether
PyScript.com is to be properly resourced or retired ([Theme A](./friction_free.md)); **the current
unowned middle state is the worst option**. Note the strategic signal
Nicholas flagged: this is effectively a white-label "PyScript.com
enterprise" pattern worth Anaconda's attention.

### 7. Build sustained visibility and repair trust

**([Theme F](./visibility.md))**

Stand up a
content strategy weighted to video and LLM channels; pursue the CodePen
partnership; make feedback routes visible from inside the product (an
in-product banner, per Anna); re-engage deliberately with contributors like
Claudiu; and treat the Tufts arc as the template for requirement-to-solution
work done in the open and based upon evidence.

One forward-looking note. The commercial software world is increasingly framed
around what Gartner calls "AI-native" development (explored more fully in
[appendix 2](./appendix2.md)). Their specific predictions are speculation, and we treat them as
such. But the language is the language our commercial users already think in,
and engaging with it - meeting practitioners inside the AI-native tools they
now use - matters regardless of whether the forecasts prove accurate. This is
where the open-source practitioner focus of this report and Anaconda's
commercial interests most clearly converge.

## Conclusion

A closing observation. Almost every interviewee, unprompted, offered to keep
helping: to file issues, to share breaking examples, to trial Invent, to join a
community call. Chris and Ethan went further, co-developing a tool with us in
the open.

The raw material for a vibrant, empowering PyScript is already here in the
people who use it.

Our job is to listen, and make it obviously worth their while.