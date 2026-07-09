# Theme E: AI is now the default route in, through and around PyScript

## What it is

Large language models as the medium of discovery, learning,
construction and documentation for PyScript. This is not a single feature
request; it is a shift in the environment, community and industry in which we
operate.

## What it means for PyScript

AI now sits on almost every path a user takes.
Discovery: Nitau, an engineer, found PyScript because "the LLM told me that
PyScript runs Python in the browser using WebAssembly." Building: Claudiu, a
hobbyist, has moved from writing code to directing it, teaching Claude to use
his PyScript helper functions and stepping back until "I'm never reading the
code, because the code is being produced much faster than I can read it."
Momin, an engineer, has built an entire platform around a copy-paste-from-LLM
workflow for non-technical students. Sai, an informatician, runs an AI agent
that generates Python executed in PyScript, and finds it competitive with a
"billion-dollar company's" full coding-agent setup, partly because "PyScript on
the browser is way faster, I can see what's happening."

There is a clear and important spread of attitudes, which we should represent
faithfully rather than lose under the generic "AI" term. At one end, Claudiu is
comfortable not reading the code. In the middle, Nitau uses "basic prompting"
as "a conscious choice," remaining "the gatekeeper" who reviews everything
before it enters his codebase, and Łukasz treats it as "a productivity
booster, but sometimes it's more like a slot machine." At the other end,
Kattni does not use AI at all, on ethical grounds (training data, climate, and
what she called an "evangelical" culture), and also because her self-assessed
Python knowledge means she "wouldn't be able to tell whether what I was just
given is good or bad." Anna, a learner, deliberately avoids AI for schoolwork
on principle while using it for lab work to move faster.

Two practical sub-findings deserve emphasis. First, model quality against
PyScript changed materially and recently: Łukasz reported that before December
2025, using AI with PyScript was "pretty dangerous," and that with Opus 4.5 it
became "tractable," speculating it may have been trained on the PyScript docs.
Momin noted LLMs "cannot detect the current version of PyScript" and sometimes
add random imports that break the code. Second, and strategically most
important: our documentation increasingly reaches humans only after passing
through an LLM. Nitau observed that he fed the docs' Markdown files to an AI
and "it did a perfect job." Nicholas's own reflection, echoed to several
interviewees, is that the people who read our documentation "are not people,
they're LLMs."

This extends beyond documentation. As AI-native tooling (coding agents such as
Claude Code and GitHub Copilot) becomes the default way practitioners build,
the question is no longer only whether a human can read our docs, but whether
an AI agent can correctly represent our APIs and services when a practitioner
prompts it. How well we express our work to these tools increasingly
determines the quality of response a practitioner receives about PyScript, and
about Anaconda's products more widely. Nicholas has
[written in depth about the challenges this poses](https://ntoll.org/article/predico/).

## Future steps

Treat "how our resources are consumed by LLMs" as a
first-class engineering, education and documentation problem (work Nicholas
has already begun). Ensure the docs, API surface and examples are structured
so an LLM produces correct, version-aware PyScript; the version-detection
failure Momin reported is a concrete target. Keep a genuinely AI-free path
fully supported and first-class, both because some valued community members
(Kattni) require it and because learners (Anna) deliberately choose it. Avoid
taking a single position on AI; the community spans the full range and trust
depends on us respecting and embracing that. Treat how our APIs and services
are represented inside AI-native coding tools as an extension of the
documentation problem: what a coding agent generates about PyScript is now
part of our public interface.

## Standing across archetypes

Universal, but polarised. Engineers and
hobbyists are furthest into AI-assisted building; educators are the most
cautious; learners are thoughtfully selective.

## Challenges

A definitional confusion has dogged discussion of AI and
PyScript inside Anaconda. "AI in the browser" can mean two quite different
things.

1. The first is running LLMs *inside* the browser runtime itself, using
   experimental web APIs. 
2. The second is what every AI-using practitioner in these interviews actually
   does: use LLMs as ordinary and complementary tools (cloud services or
   agents) that generate or assist with Python, which then runs in PyScript.

Internal advocacy at Anaconda has focused on the first sense of "AI in the
browser" (running models inside the browser); all the practitioner evidence in
this report concerns the second (LLMs as external tools generating PyScript
code or consuming PyScript-based resources). Acting on this theme therefore
requires realigning internal direction with the evidence, rather than
advocating for something with no demonstrated use case, market signal or
community demand. That realignment is beyond the PyScript team's sole
authority. Furthermore, were in-browser models ever wanted, JavaScript would be
the better-performing tool for the job.