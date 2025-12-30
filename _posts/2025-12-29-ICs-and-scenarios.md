---
layout: post
title: "Scenarios, Contexts, and Observables in QSP"
date: 2025-12-29
tags: [qsp]
---

Now let's talk about templated timing and treatment configurations. The reason we need those when we're recording our observables is that oftentimes we're not recording our observables in a natural state or wild-type state—a lot of times it's under some sort of intervention or essentially exogenous forcing. There's some sort of stuff happening to our patient or model, and we want to be able to capture that well when we're capturing our observables for calibrating our system.

At this stage, I'm thinking about this more abstractly without really thinking about how to write the derivation code, but essentially, during the annotation process, I want to record enough information so that derivation is simple.

## Defining Scenarios

We need to predefine the scenario parts ahead of time. A scenario essentially consists of timing and events that happen in that timing. You start at time zero, you move to first diagnosis, followed by biopsies or resection, neoadjuvant therapies, maybe additional biopsies and other therapies, and hopefully patient survival (and sometimes not, of course). This can all be captured as a scenario. A lot of these things are happening to the patients—it's not just the tumor growing in a vacuum, so to speak.

Some of this is dosing and dosing schedules of drugs, and that's already well captured in our QSP modeling. We can model how different chemos are administered, like nab-paclitaxel and gemcitabine. Scenarios essentially consist of these treatments or interventions, but not only treatments and interventions—also measurements. We want to be able to capture measurement events. You have all these different events happening during a scenario.

## Intervention Events

These interventions include resections, biopsies, chemo, immunotherapies. For each of these, we want to know: for resection, how much tumor is removed, what species are removed; same with biopsies. We already talked about how we already have a workflow for chemotherapy and immunotherapy drugs. We want to know at what time these things are administered, or if they're interventions, are they in certain cycles, repeat doses, amounts in the doses, etc. A lot of that stuff is already captured; some of it we don't have yet.

## Context Mismatches

We've talked about context as well. The idea behind a lot of this stuff is that the context for a PDAC model is a human—a human gets a diagnosis and goes under treatment, and maybe some other things as well. But some of our observables may come from things that don't quite match that context.

Contexts are basically things that we're not able to explicitly capture in our model. We're not explicitly capturing that we're modeling human versus mouse—we don't have a switch to toggle between the two. So if we get observables from a mouse but we want to use them to help calibrate our human model, we have to add what we're currently doing: adding predefined fudge factors. These are ways to expand uncertainty a lot of times, or maybe bias the observable in different directions.

When we have these fudge factors, it can be useful to think: are there things that we're currently fudging—species, indication, compartment volume, etc.—that maybe we should be explicitly capturing in our model so we don't have to add this extra uncertainty? We can just try and capture whatever it is we're not capturing explicitly mechanistically. That may add more parameters and more complexity, but it may be worth it for decreasing the variance or bias that we're having to fudge with.

## PDAC-Relevant Observables

Let's move on to some of the observables that are particularly relevant for PDAC:
- **Tumor volume over time** - a huge one
- **Clinical data** - survival data (overall versus progression-free)
- **Immune cell densities** - CD8+ T cell density, Treg density, TAM density, MDSC density, CAF density. Very common, all of these different counts, especially at baseline biopsies
- **Markers** - PD-1 expression, Ki-67 proliferation indices
- **Stromal content** - super important for PDAC. We have the dense matrix, very hard for T cells to infiltrate. We want to be able to capture that stuff.

Of course, we're thinking about the time zero problem again. What should we define as time zero? Maybe I'll just get into that in later blog posts.
