# Cross-chapter knowledge map
`concept-links.json` is the source of truth for the 84 hand-curated concept cross-links shown in the 28 standalone HTML chapters. Each of the 28 chapter records has exactly three destinations, an existing article section anchor, a reader-facing question, and a causal explanation.

Why the graph is static:
- Navigation works without network access and without JavaScript.
- Every article remains self-contained. Links are optional extensions, not prerequisites or substitutes for explanation.
- The graph uses stable `NN.html#section-id` URLs so readers can arrive at the explanation rather than the top of a large page.
- Change destinations only after checking they are materially related; no automated synonym-link spam.
- `scripts/validate_site.py` and `tests/test_site.py` check graph cardinality, target pages and anchor IDs, and whether each article renders its three edges.

The curated learning map is `knowledge-map.html`, featuring five routes and nine cross-topic causal links. Update both the graph and the static map if major topic groups or key links change.
