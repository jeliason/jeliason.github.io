---
layout: post
title: "Dealing with Context Mismatches in QSP Parameterization"
date: 2025-12-23
tags: [qsp]
---

I'm thinking about parameters. The example I'm using is the rate of M2 to M1 polarization (macrophage polarization). This is often estimated by combining various different quantities across several different contexts. I'm thinking contexts have various axes like species, compartment or organ, treatment scenario, etc.

Sometimes there are differences in the mechanistic alignment—by mechanistic alignment I mean things like: is this an effective kill rate or a pure kill rate? Is this killing rate being modulated? Or is this kill rate only applicable in a specific scenario? You have to be careful about things like that.

The observables also have context. They're defined similarly along all of these same axes. They could be combined to estimate a parameter of interest (POI). However, if the contexts are mismatched, then you'll need to add bias/uncertainty to the estimate according to some predefined rules. There are probably many recipes for combining observables into a POI; however, there's probably one that minimizes the bias/variance given a set of observables. So now we have a somewhat different problem.

## Context Mapping

Is there such a thing as a reasonable rubric for mapping between contexts? There is certainly something like allometric scaling. We're thinking about contexts where an observable is measured in, you know, resectable PDAC in humans—that'd be the ideal—but say it was actually measured in mice. Can we scale from mice to humans? If we have tumor volumes and stuff like that, we can scale compartment volumes allometrically. But other parameters, like kinetic rate parameters, it's probably not as straightforward to scale those. So yeah, that's something to think about.

## Mechanistic Interpretation

Another thing to think about, harkening back to that mechanistic alignment problem: Can we formally define a parameter's mechanistic interpretation so that we can formally verify that a set of observables and mappings (with these recipes that we have) verifiably maps to the parameter of interest with the correctly aligned mechanistic interpretation?

This is a little bit confusing, but when we're trying to map to a parameter of interest and we have a set of observables that we're using to construct that parameter of interest, we want to make sure that the observables, when combined together with the mappings, verifiably map to the parameter of interest with the correct mechanistic interpretation. This is kind of a hard problem—you have to understand exactly how this parameter is being used within the model. You need to take the observables and force your mappings to constrain to that exact interpretation. This is somewhat beyond just unit checking.

We can enumerate a list of types of constants, like a first-order rate, Hill coefficient, EC50, etc., or other kinds of rate parameters. And then I got to thinking: is a set of ODEs formal enough? If we have the model structure written down, that's essentially as formal as we could get. And so a parameter defined within that ODE structure—given that, we should be able to get at least some sort of truncated-order approximation of the parameter's interpretation within the model.

By truncated order I mean: we have some neighborhood around the parameter, of reactions and species, that maybe affect how that parameter can be interpreted. But as we get farther and farther away from that—you can imagine all these reactions happening in sort of a network—as you get farther and farther away from that reaction, the parameter may be less and less constrained by those other things. So we can truncate the neighborhood around the parameter, around that reaction in which the parameter takes part, in order to identify this truncated-order approximation of the mechanistic interpretation.

I'm thinking of things like chemical reaction networks (CRN), for example. We can interpret the parameters in their CRN neighborhood. We truncate out at some order. And so then, after that, maybe it is possible to formally assemble observables into a parameter of interest with a verifiable mechanistic interpretation that is implied according to that CRN neighborhood approximation. That means that somehow observables need to be stated in terms of the CRN neighborhood too. Maybe they are outputs of a given neighborhood, for example.

The problem is that there can be a decent amount of confounding, at least among more tightly coupled neighborhoods. The truncation problem is sort of rearing its head here. There may be decent "cleavage points," though—clustering, as it were—that allows us to not rely on the whole model, the whole chemical reaction network, but just the neighborhoods. So maybe we need to find clusters in order to be able to properly define these mechanistic interpretations.

## Global Inference Approach

So we have all of these observables. Ideally, we would have a machine that can simply perform inference on the global model given these observables. There may be various amounts of context mapping, though. Also, it may in fact be advantageous to actually make some cuts in the CRN at those cleavage points, possibly.

Let's switch focus to inference. Everything should pass through the calibration targets. Let's just run inference directly through calibration targets. We still have to think about (a) transferring context and (b) appropriately capturing the mapping from model species to observable. Should we still go via Monte Carlo samples? I think so, and we can always fit, for example, a Gaussian or other model to give us parameterized measurements in different contexts.

Ultimately, I think identifying this formal structure from parameters and their interpretations is maybe too difficult. Really, with all these observables, what we should do is just run inference and let the model figure out how best to use the information that is being given in this global sense, rather than trying to force everything together in this sort of structured, forced-logic way.
