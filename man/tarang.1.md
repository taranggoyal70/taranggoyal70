```text
TARANG(1)                  User Commands                  TARANG(1)
```

## NAME

**tarang** — AI product engineer; turns ambiguous problems into systems people can test

## SYNOPSIS

**tarang** [**--build**] [**--prove**] [**--talk-to-users**] [_problem_]...

## DESCRIPTION

**tarang** is a product process resident on atlas. It works across model behavior,
frontend, backend, integrations, deployment, and evaluation. It prefers a complete
loop with evidence over a polished demo with an invisible failure mode.

Invoked without arguments, **tarang** defaults to `--build-end-to-end`.

## OPTIONS

**--build**
: Converts a rough problem into a working product path.

**--prove**
: Measures before making a claim and leaves the limits visible.

**--talk-to-users**
: Replaces assumptions with uncomfortable notes from real people.

**--hackathon**
: Competitive mode. Eight wins across thirteen entries.

**--sleep**
: Recognized for POSIX compliance. Still optional.

## EXIT STATUS

**0**  shipped and checked
**1**  learned something useful
**>1** evidence missing; do not claim success

## BUGS

Starts another product when the current one exposes a more interesting systems problem.
Several maintainers consider this the feature.

## SEE ALSO

**locus**(1), **tickmark**(1), **hackathons.log**(5), **.plan**(7), and the
[README](../README.md) this page escaped from.

```text
ATLASD OS 8.0                  2026-10-23                TARANG(1)
```
