# 2. Key findings

## Affirmations

The strongest and most consistent theme is that PyScript's frictionless
experience is its defining strength: it just works. People who did
not enjoy setting up Python environments, or who could not, found that PyScript
removed that barrier entirely. Anna, a learner, valued that "there is no setup
you have to do, you just hit create website, and then you can type right in and
immediately see on the other side what is happening." Kattni, who teaches,
compared it directly to the moment that first drew her to CircuitPython:
"PyScript is closer to the LED blinking in the sense that you do the thing and
it's all right there." Hammad, who home educates, went as far as to say we had,
perhaps unintentionally, "built the simplest system of just getting started."

A second positive: the browser gives Python superpowers for free. Łukasz used
PyScript to convert audio formats entirely in the browser for a friend on a
locked-down machine, noting that "all of this binary operations can be just
successfully done inside a browser." Sai found the browser's sandbox solved a
real security problem: an AI agent generating Python that runs client-side is
contained by the browser (in Nicholas's phrase, "the blast radius is only going
to be your Chrome"). As Sai put it, because it runs in the browser he does not
have to stand up "an AWS Lambda with some hacked-up Python," nor obfuscate API
keys, since the browser carries authentication for him.

Third, the recent engineering work is landing. Interviewees repeatedly praised
the rewrite, the improved worker support, cross-browser progress, the rewritten
documentation with intentional examples, and the TuftsHub self-hosting release.
Hammad singled out the TuftsHub release not just for what it did but for how it
was delivered: a YouTube video plus a GitHub repo that simply worked. Mark, a
veteran engineer, was unreserved: "I'm able to do real stuff with it."

## Challenges

The clearest challenge is the JavaScript and browser boundary. This is where
experienced users get stuck, and it is the point at which we appear to be
losing people. Łukasz described the accumulated, hard-won knowledge of "the two
worlds that you're living in all the time," and was blunt that the rough edges
have not gone away: he has simply learned to "avoid the rough edges, not
because they're no longer there, just because you know to avoid them."
Crucially, he reported a pattern he hears from other Python programmers: "it
works for something simple, it didn't work for something else, I didn't know
what to do." We are converting Python developers on the easy case and losing
people at the next step as they attempt to dig deeper into the browser's
JavaScript APIs or try to use popular Python packages that simply cannot work
inside a browser.

Packaging and stability came up repeatedly. Kattni hit the wall of C-dependent
packages and, tellingly, the failure was silent: "none of the error messages
implied this library is not supported." Hammad wants version stability above
novelty, arguing "the most valuable thing is your own time when you've set it
up," and is wary of Pyodide's release cadence (Pyodide is the CPython
distribution, compiled for the browser, that PyScript uses).

Error messages and the blank page problem affect newcomers specifically. The
live session with Anna was the clearest illustration we have: she reads only
the top line of an error and ignores the stack trace, "because there's a lot,
and I know that I don't need to read every single line." Kattni named the blank
page problem directly: "you go to PyScript[.com], and it's this sandbox, it's
open... and I'm like, what do I do?"

Discoverability and marketing were raised, unprompted, by most of the nine
interviewees. Kattni called it "a perennial problem" for open source. Nitau, an
engineer, found it "a little bit mind-boggling" that PyScript is not more
widely known given what it does. Claudiu had previously produced a full
marketing proposal that went nowhere; despite his explicitly asking an Anaconda
architect for guidance, none came - a frustrating experience we should own
and address (see Theme F).

Finally, feedback channels are effectively invisible to users. When
PyScript.com crashed, Anna "basically walked away," told no one, filed no
report, and was unaware of any way to give feedback. This is not an isolated
attitude; Hammad described himself as a silent reader who assumed the problem
"might be my own" until we reached out.

PyScript.com's reliability, which surfaced most sharply in the Tufts case
study, is another major challenge. Chris was blunt that the service "does with
fair regularity" become "ungodly slow," and that when it does mid-lesson "the
class kind of falls apart." He gave concrete casualties: a middle-school
workshop, college classes and company presentations. Because PyScript.com is
unmaintained, our current fix path is to escalate through colleagues and
infrastructure, which "takes 15 minutes to half an hour" - useless in a live
classroom. Anna's and Hammad's crash experiences echo this.

## Opportunities

Three opportunities stand out.

First, a simple, opinionated higher-level UI layer. Hammad described, entirely
unprompted, something extremely close to Invent: "import UI, UI.run," bundled
so that "from pyscript import invent" just works. This is an encouraging
external signal for the Invent direction and work we had to stop.

Second, AI as the new default route into and through PyScript. It is now the
way people discover PyScript (Nitau found it via an LLM), the way they learn
it, the way they build with it (Claudiu, Momin, Sai), and increasingly the way
our documentation reaches humans at all. This changes what "writing
documentation" means and validates our approach to rewriting our documentation
in Q4 2025.

Third, partnerships and content. Mark's CodePen suggestion, Łukasz's and
Claudiu's calls for video content, and the repeated marketing theme all point
at the same gap: PyScript is largely invisible in the channels where developers
now learn and share trends and innovations.