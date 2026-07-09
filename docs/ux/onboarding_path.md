# Theme D: Onboarding - the blank page and the graduation path

## What it is

Two ends of the same concern. At the entry end, the blank page
problem: a beginner faced with an empty sandbox and no idea what to do in
PyScript.com. At the far end, the graduation problem: an advanced user needing
to know that PyScript.com will let them grow rather than trapping them.

## What it means for PyScript

Enabling a practitioner's growth is a design
responsibility, not something we can leave to chance. Kattni, an educator,
named the blank page problem plainly and gave us the remedy: she does "a lot
better when I have something to tear apart and put back together than I do when
I have to write something from scratch," and asked repeatedly for more demos
and idiomatic examples. This maps neatly onto the friction-free strength of
[Theme A](./friction_free.md): the environment is welcoming, but a welcoming environment still needs
something in it.

At the other end, Mark, a formidably experienced engineer, framed the
graduation problem in terms of his "architecture is destiny" principle. His
advice on Invent applies to PyScript as a whole: design so that the skills a
user learns are migratable, and "if you're thinking about solving a problem in
a way that is not migratable, then you're bolting people into that
cul-de-sac." Where a cul-de-sac is unavoidable, make it "obvious to you" (the
user) that the dead end is coming, so they can move on deliberately rather than
hitting a wall. Hammad made the same point constructively from the
learner's side: users "can graduate to deeper tooling like UV in their own
time," provided we do not force it on them early.

A framing Nicholas offered during the Hammad interview belongs here: limiting
a learner's surface area so they grow stepwise (Vygotsky's zone of proximal
development) applies to all practitioners, not only beginners.

The Tufts case study gives the graduation path a concrete outcome. What Chris
asked for is a tool he can "pip install... and hit run and now suddenly
everything just works", something that "just sits there happily humming away in
the corner like a fridge." That is the graduation path for real: start on
PyScript.com's friction-free loop, then move to a local-first, offline-capable,
self-hostable tool that carries the same capabilities into a GitHub-based
workflow the students are learning anyway. The retrospective also surfaced the
risk at the far end that Mark warned about. Chris, having lived with TuftsHub,
found himself wanting a single window holding files, code and live preview, and
Nicholas was wary of "re-implementing PyScript.com," preferring to take the
question to the wider community rather than quietly rebuild an IDE. The
tension between meeting a real workflow pain and not trapping the tool in a
reinvention is exactly the migratability question highlighted in this theme.

## Future steps

Invest in demos and idiomatic, remixable examples as a
primary onboarding tool, not an afterthought; Kattni, Mark and Anna all pointed
here. Make the intended progression explicit: from PyScript.com, to
self-hosting, to full tooling, so that graduation feels like a signposted path
rather than a cliff. Carry the migratability test into Invent's design.

## Standing across archetypes

The blank page end is a learner and educator
theme. The graduation end is an engineer theme. Both are really the same
request for a coherent and clearly articulated pathway from first contact to
mastery.

## Challenges

PyScript.com is unmaintained and slowly bitrotting, so no
coherent graduation pathway can currently be built upon it. Work on Invent, the
most direct attempt to address the learning journey, was stopped in 2024. A
limited re-engagement was planned into Q1 2026, and, independently, this
research found an unprompted practitioner description of exactly what Invent
set out to provide (see [Section 2](./key_findings.md), Opportunities, and
[next step #5](./conclusion.md#5-get-invent-to-an-early-release-and-validate-it-against-real-users)). Properly
restarting that work is a resourcing and prioritisation decision that sits
above the PyScript team.