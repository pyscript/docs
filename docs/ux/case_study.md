# Case study: the Tufts tooling arc (PyScript.com reliability and TuftsHub)

This case study sits slightly apart from the six themes because it is a single,
continuous story told across two calls, and because its subject, Chris and
Ethan at Tufts, is an institutional relationship rather than an individual
archetype. It is included in full because it does three things at once: it
states the PyScript.com reliability problem first-hand, it enumerates exactly
what a replacement must provide, and it demonstrates the engagement loop this
report advocates.

## The problem

Chris and Ethan both praised PyScript.com's ease of
developing, sharing and cloning, and the instant browser-based start it gives
students. The failure is reliability. In Chris's words the service "does with
fair regularity" become "ungodly slow", and when it does so mid-lesson "the
class kind of falls apart", with a middle-school workshop, college classes and
company presentations all named as failures. Because PyScript.com is
unmaintained, the fix path runs through colleagues and infrastructure and
takes fifteen minutes to half an hour, which is no use in front of a class.
This is the first-hand version of the crashes Anna and Hammad reported
second-hand.

## What a replacement must provide

The professors were willing to move
hosting to GitHub Pages, which they value for teaching industry-standard Git
workflows, but only three PyScript.com capabilities stand in the way: channels
(sharing information between pages over WebSockets), an API proxy (so a secret
key is never exposed), and authorisation (so a project is restricted to
approved people, since an open project is, as Ethan noted, "attached to my
credit card"). A useful clarification emerged on channels: they already run on
the same publish/subscribe logic as the industry-standard MQTT message bus,
with PyScript.com acting as the broker, and Chris confirmed they have
connected Raspberry Pis and ESP32s to the PyScript WebSocket. The desired
solution was a one-click, pip-installable tool that "just sits there happily
humming away in the corner like a fridge", local-first and offline-capable
(Ethan's "aeroplane version"), syncing to a GitHub folder, and self-hostable
on Tufts, Amazon or any other infrastructure. Nicholas noted this effectively
amounts to a white-label "PyScript.com enterprise" instance, a useful data
point and potential opportunity for Anaconda.

## The response and its review

Nicholas built TuftsHub (thub) against these
requirements, and the second call reviewed it. Chris demonstrated it serving an
app locally straight from the source he was editing, with user management built
in. Feedback and new requests followed: a one-action pull of an existing
PyScript.com project (reading the `pyscript.toml` and assembling a complete
offline copy), support for running several projects at once, and a
single-window view combining files, code and live preview to escape the sprawl
of many editor and browser windows. Nicholas was careful throughout not to
reinvent PyScript.com's in-browser IDE, preferring to open the design question
to colleagues Martin and Josh and the wider community, and floated his earlier
PySnippets work as a possible starting point.

## Why it matters

Beyond the concrete requirements, the arc is the report's
clearest example of engagement done effectively: requirements gathered on the
record so the movement from problem to solution is visible, a proof of concept
built quickly, a review to refine it, and then a deliberate opening-up, keeping
the repository under the Tufts GitHub organisation, seeking a better name than
thub, releasing on PyPI, and shifting future requests from private Slack to
public GitHub issues. It is both a source of requirements (Themes
[A](./friction_free.md), [B](./js_boundary.md), [D](./onboarding_path.md)) and
a template for how this kind of work should run ([Theme F](./visibility.md)).