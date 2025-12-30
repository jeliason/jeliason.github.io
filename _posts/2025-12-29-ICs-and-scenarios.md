---
layout: post
title: "What Should My Initial Conditions Be?"
date: 2025-12-29
tags: [qsp]
---

Let's talk about initial conditions—time zero, or how to start the model, where to start the model at.

## The Spin-Up Approach

A commonly used method in QSP is what I call "spinning up." You basically start most things in a zero state—zero concentration or zero count. You start off with a pretty small tumor and then you just let everything evolve according to the equations until you hit a minimum tumor volume, which is a typical volume you would expect at diagnosis. And then that's sort of your actual initial conditions. From here, this is what we'd expect at diagnosis. From here on out, you set all of the species to the values that they had at this diagnosis time point, and that becomes your new time zero.

You're hoping that everything is sort of equilibrating or moving in the right direction no matter where you start it—whether you start everything at zero or something else, it's kind of moving to an attractor, so to speak. I mentioned that you sort of run until you get to this tumor volume or tumor diameter that you would expect. There may be other constraints for initial conditions besides this tumor volume element. This is commonly used—I'm not going to spend more time thinking about if there are other constraints for ICs for now.

## Not Really Equilibration

We spin up to this tumor volume, and this is definitely not necessarily a steady state. Sometimes we call it "equilibration," even though the species may not equilibrate at all. It may be growing quickly at that point. Of course, that's what is happening in real patients too. It's not like when we measure their tumors that everything is equilibrated in steady state. That's obviously not true—the tumor continues to grow, cells continue to infiltrate and polarize and do their thing. So we sometimes call it equilibration, but that's definitely a misnomer.

I'm thinking right now that we have these baseline functions running from a true zero until we hit this minimum tumor volume. So maybe we need sort of an outer boundary for this time—maybe we could set it to something like the 99th percentile of expected growth time, perhaps.

## Defining True Zero

Really thinking about what true zero is, how true zero is defined. Especially for PDAC, there are precursor states like IPMN. What does IPMN look like as far as the densities of different cell types, concentrations of different cytokines? Should we assume that we're starting at this true zero in an IPMN-like state? Does it matter that much?

We can move from a zero—say, maybe it's healthy pancreas or an IPMN precursor state—move from there until we get to our minimum tumor volume. Hopefully at this diagnostic stage we're not yet at late-stage PDAC. That's what we get at resection. Of course, you're moving through these different cancer stages as well.

## Stage-Dependent Parameters

An idea is: what if rates change over stage? Like these kinetic parameters that we have—do those change over stage? This was just a thought I had in my head. We do already have that actually, to some degree. We have these "effective" or "modulated" rates that are dependent on other species, right? We can have a cancer cell killing rate by T cells that's modulated by T-regs, modulated by CAFs, etc.

We'll need to make sure that any of these stage-dependent parameters are appropriately captured where they're modulated in this way. This way we can start at this time zero and appropriately capture all parameters. It's not like we need to set parameters per stage anymore. We can expect those parameters will be modulated accordingly as the tumor progresses through these stages.

## Modeling Resections

Yeah, we should probably model resections specifically. I don't know if we do that right now. That probably isn't hard—you just cut the tumor down significantly, and maybe some of the other species as well.

So yeah, I think that's probably enough for this particular part. Next time I'll talk a little bit more about defining scenarios and things like that. Let's stop there for now.
