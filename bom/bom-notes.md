# BOM notes

- Every line is priced in indicative USD for one reference site (three tilt stakes 10 m apart, one crack gauge, 60 m of bus cable, one mast), with a supplier or supplier type. Prices are not quotes.
- Line numbers match the numbered callouts in `media/exploded.png`. Lines 9 and 10 have no callout.
- Line 6 (FieldNode core, $126) is the lab's shared node, costed in the FieldNode project under SLW-DDR-001 D1 (adopted for TRL 3 work, open for Amish's review). It is listed for completeness and is not counted against the SlopeWatch budget.
- SlopeWatch-specific total $261.00 against the $250 `budget_usd` (4.4 % over, R11 not met); $237.00 where an existing pole replaces the mast (line 8). With the FieldNode core the site total is $387.00. `docs/04-calcs/sizing.py` sums the file and checks it against `project.yaml`.
- TRL 3 changes: line 4 adds a reader board and box (+$6), because the gauge is about 60 m of cable from the node; line 10 adds foam plugs for the capsule (+$1); line 2 specifies the SCL3300-D01 in mode 1 and a 0.4 m capsule depth; line 8 adds the earth rod to the description at no change in price.
- A LoRaWAN gateway is not included. Sites without coverage need one (TwinKit, about $290 in parts per its TRL 3 BOM).
