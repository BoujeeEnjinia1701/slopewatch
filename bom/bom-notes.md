# BOM notes

- Every line is priced in indicative USD for one reference site (three tilt stakes 10 m apart, one crack gauge, 60 m of bus cable, node on an existing pole; line 8 mast priced as a site option), with a supplier or supplier type. Prices are not quotes.
- Line numbers match the numbered callouts in `media/exploded.png`. Lines 9 and 10 have no callout.
- Line 6 (FieldNode core, $126) is the lab's shared node, costed in the FieldNode project under SLW-DDR-001 D1 (decided by Amish, 2026-09-25, SLW-DDR-002). It is listed for completeness and is not counted against the SlopeWatch budget.
- Reference site (SLW-DDR-002): the node and alert unit go on an existing pole, so line 8 (mast and footing, $24) is a site option outside the reference-site cost. SlopeWatch-specific total for the reference site $245.00 against the $250 `budget_usd` (R11 met on paper, $5 within); $269.00 at a site that needs the mast. With the FieldNode core the reference site comes to $371.00. `docs/04-calcs/sizing.py` sums the file and checks it against `project.yaml`.
- DDR-002 change: line 7 now includes a 26.9 mm post and a 7 m lead in conduit, so the keyed silence switch stands about 5 m from the siren (+$8, from $25 to $33).
- TRL 3 changes: line 4 adds a reader board and box (+$6), because the gauge is about 60 m of cable from the node; line 10 adds foam plugs for the capsule (+$1); line 2 specifies the SCL3300-D01 in mode 1 and a 0.4 m capsule depth; line 8 adds the earth rod to the description at no change in price.
- A LoRaWAN gateway is not included. Sites without coverage need one (TwinKit, about $290 in parts per its TRL 3 BOM).
