# MCs Thesis: 'Political Polarization & Echo Chamber: an Approach for Identification and Analysis on Reddit'

## Abstract:

Heterogeneity in content and freedom of expression provided by Social Networking sites can
cause to their users Cognitive Dissonance. Such a discomfort leads users to selectively expose
themselves to information that supports their personal beliefs or values, i.e., confirmation
bias. This trend is further reinforced by the reccomendation algorithms of the Social Networks
which leads to phenomena such as Polarization and Echo Chambers. 
This thesis, focusing on a political context of the first two and a half years of Donald Trump presidency, aims to identify
Echo Chambers and measure Polarization on Reddit.
Initially, we define a methodology to measure the political polarization of a sumbission
(i.e., post on Reddit). Once a Ground Truth is created, we leverage two different algorithms/
approaches on this task and evaluate their results. The first consits in identifying via Latent
Dirichlet Allocation highly disinctive terms from both that chacterize the rethorical languages
of both parties and subsequently training a Support Vector Machine to classiffy submission accoridng
to such extracted features. The latter is a neural approach. It leverages Word Embeddings
and Long Short-Term Memory architecture in order to measure the polarization score
of a submission by quantifying its agreement with both ideologies.
Next, we verify the existence of polarized system, namely Echo Chamber, across three
different topics concenrning socio-political issues. For all of them, we define the user interaction
network, labeled by their polarization score. By applying algorithms of Community
Detection, we extract communities that we further analyze by evaluating their structural and
idelogical cohesion. The approaches deployed enable to identify potential politically polarized
Echo Chamber both with respect to the democratic and republican ideologies.

