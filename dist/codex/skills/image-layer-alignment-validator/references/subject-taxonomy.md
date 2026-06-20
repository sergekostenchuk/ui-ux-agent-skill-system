# Subject Taxonomy

Use this reference when the main object is not obvious.

## Primary Subject

The primary subject is the object whose apparent identity and position must remain stable across the base and reveal layer. It is usually one of:

- the centered person, face, body, product, vehicle, device, garment, or hero object;
- the object that the cursor reveal is intended to transform;
- the object with the largest semantic importance, even if it is not the largest pixel region.

When several objects are present, choose the one that would make the effect feel broken if it shifted.

## Secondary Objects

Secondary objects can differ more freely:

- background gradients, walls, landscapes, reflections, lights, and shadows;
- accessories, helmets, tools, labels, small props, particles, and decorative layers;
- color treatments, texture overlays, atmospheric effects, and generated details.

Secondary objects still matter if they touch or occlude the primary subject. A changed helmet, hand, or face accessory may be secondary semantically but primary for perceived alignment.

## Ambiguity Rules

- If the reveal effect transforms a person into a character, treat the torso/head pose as the primary subject and the costume as secondary.
- If the reveal effect transforms a product finish, treat the product silhouette as primary and finish details as secondary.
- If a generated reveal adds a large new object that competes with the original subject, mention it as a secondary-object conflict.
- If no stable primary subject exists, return `different subject` or `inconclusive` instead of forcing a numeric alignment verdict.

## Manual Override

The script detects salient foreground boxes. It does not understand intent. Override the detected box when:

- the biggest detected component is background or a decorative object;
- the subject is split into multiple components;
- transparency or lighting causes a bad mask;
- the user identifies a specific object as the main subject.
