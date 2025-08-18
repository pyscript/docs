# Change Management and Deprecation Cycles

> ποταμοῖσι τοῖσιν αὐτοῖσιν ἐμβαίνουσιν ἕτερα καὶ ἕτερα ὕδατα ἐπιρρεῖ
> (Upon those who step into the same stream ever different waters flow)
>
> ~ Heraclitus

!!! info

    **TL;DR: Change happens.**

    Sometimes such change is a breaking change. Sometimes such change means
    retiring capabilities.

    **This document explains how we're going to manage change carefully,
    collaboratively and compassionately.**

All code changes.

To ensure PyScript changes are smooth, dependable and well advertised within
our community of users, this document outlines our approach in two areas:

1. Changes and additions to our codebase.
2. Deprecation of existing features as they are replaced or become redundant.

Ultimately, and out of necessity as a web-based project, our aim is for a
small, neat, and comprehensible code base, created through engagement with our
community.

Each release of PyScript is given a [calver](https://calver.org/) release
number so folks using PyScript can immediately see how up-to-date their
referenced PyScript is. For example, release number `2024-10-2` is the second
release made in October, 2024.

Furthermore, **calver allows users to pin the version of PyScript used in their
project to a specific version**. Since a release never changes once released,
users can be confident PyScript won't shift from under them.

**We recommend developers using PyScript keep the version of PyScript they are
using up to date**. To ensure this process is smooth, this document was
created to describe what you can expect from us.

## Change

The source of change in PyScript comes from three places:

1. The community - who need change in order to work more effectively.
2. The core developers - who know the code, and want it to be well maintained.
3. The tech world - who update web standards, grow WASM and bring new features.

Taking each in turn, here's how such changes ought to take place (although we
want to acknowledge this may not always be possible due to context).

### The Community

The community of coders who create with PyScript are our primary concern. We
are a diverse community who include folks with many different, and sometimes
conflicting, technical needs. So PyScript best reflects these needs, we invite
our community to engage with us as we shape PyScript's future.

* Informal technical discussion happens over on our
  [discord server](https://discord.gg/HxvBtukrg2).
* We have
  [weekly technical community calls](https://discord.gg/CxkMkSa3Zk?event=1303877626154323968)
  on our discord server, and you can find recordings of these calls over on
  [our YouTube channel](https://www.youtube.com/@PyScriptTV).
* If you have a proposal for a change,
  [start a discussion over on GitHub](https://github.com/pyscript/pyscript/discussions)
  or [submit an issue/bug report](https://github.com/pyscript/pyscript/issues).
* If, after discussion and consensus has been agreed with the core developers,
  you find yourself creating code, please submit a pull request by following
  the information in our [developer guide](../developers).
* Finally, we expect everyone to act in the spirit of our
  [code of conduct](../conduct/).

Sometimes there will be conflicting needs or opinions. We welcome constructive
criticism, compassionate argument and pragmatic analysis. However, our core aim
is to find a consensus, and this will inevitably require compromise,
humbleness, and patience. Often such consensus will not please anyone since
nobody gets exactly what they want. But in such a situation, by ensuring our
debate and community engagement is done in public, we will (at least) have a
record of how we arrived at such a consensus.

### The Developers

The core developers of PyScript often need to refactor or change code to ensure
PyScript remains a high quality open source project. To this end, our changes
will be:

* Proposed via a discussion on GitHub, or debated in the community call,
  or described on discord (or a mixture of all three). Our intention is to do
  all our work in the open and with the full engagement of the community.
* Delivered via a pull request, reviewed in public. The community is invited to
  be a part of this review process (subscribe to these updates
  via your GitHub account).
* Described in our docs and release notes.

We, as core maintainers, welcome constructive feedback about our processes.

### External Tech

The universe is always changing and PyScript needs to change with it. These
changes happen in three ways:

* **Dependencies**. The Python interpreters, upon which we depend, are active
  open source projects who also make new releases. The core maintainers of
  PyScript have excellent relationships with these upstream projects and we
  will endeavour to ensure the latest changes appear in PyScript as soon as
  possible,
* **Security**. Inevitably some code we depend upon, or perhaps even
  in PyScript itself, will encounter a security related problem. **PyScript
  takes such problems very seriously** and will take all the necessary steps to
  ensure security related changes are timely, well documented and taken with
  the greatest of care and attention.
* **Standards**. PyScript's parents are Python and the web. PyScript is itself
  facilitated by web-assembly (WASM). All of these technical worlds rely on
  standards to ensure compatibility. Such standards are evolving and changing
  all the time and we (PyScript core developers) are actively involved in such
  developments and will endeavour to ensure PyScript, when appropriate, is
  updated to the latest versions of these standards.

## Deprecation

Sometimes we need to make breaking changes:

* A new feature supercedes an old one.
* An initial implementation of an API requires improvement.
* A feature is no longer used and requires removal to save space / complexity.

Breaking changes can cause disruption. Therefore we will be very careful when
making such changes. Of primary importance are communication and
predictability.

### Communication

Any breaking changes will be arrived at via the processes described in the
[Change](#change) section.

Since these will be done in public and with community engagement we hope the
initial decision for a breaking change will come as no surprise. Furthermore,
as the change is implemented there will be further opportunities for the change
to be broadcast: via updates in our community call, via our upcoming PyScript
newsletter, and in the formal technical discussions that take place on GitHub.

### Predictability

The release of a breaking change follows this process:

* After the initial communication of the change, the release of PyScript that
  immediately follows the decision will ensure the affected API reports the
  upcoming changes via a warning in the browser console.
* The documentation will also be updated to reflect the upcoming changes to the
  API: the old API will be clearly flagged as about to change.
* The release notes immediately following the implementation of the
  breaking change will include a clear indication that the breaking change has
  landed.
* The documentation, immediately following the implementation of the breaking
  change, will include a warning to indicate how the new update is different
  from the old, and will remove the references to the old API.
* In the following releases the warning about the arrival of the new breaking
  change will be removed.

## Feedback

This document is a work in progress. Please feel free to offer feedback via
[the GitHub project for our documentation](https://github.com/pyscript/docs).

Thank you!
