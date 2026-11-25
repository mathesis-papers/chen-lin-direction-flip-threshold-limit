# Convergence of Chen and Lin's direction-flip threshold

Haobo Ma (ChronoAI Pte Ltd, Singapore) and Wenlin Zhang (National University of Singapore; ChronoAI Pte Ltd, Singapore).

The note answers Question 6.1 of Chen and Lin, arXiv:2609.14655v1, Section 6. It proves convergence for the original strict threshold, gives its finite-counterexample infimum formula and an explicit witness-dependent cutoff, and establishes the bound `1/1665 <= L <= 9/19`. The exact value asked for in Problem 6.2 remains undetermined.

## Build

Use Tectonic 0.17.0:

```sh
tectonic note.tex
```

Alternatively use a standard LaTeX distribution:

```sh
pdflatex note.tex
pdflatex note.tex
```

The bibliography is included in `note.tex`; no BibTeX step or external figures are needed.

## Mathematical coverage

The all-length proof is contained in `note.tex`. Its reflected-matrix and padding argument treats all positive lengths, arbitrary finite nonempty tournaments, and noninjective homomorphisms. The strict threshold is preserved, including saturation at the length.

The pinned [Lean file](https://github.com/the-omega-institute/trureturing/blob/81968a52b83b3d79d4db8e60c34e05d953675dc0/D5/S3/Combinatorics/ExtremalDensity/ChenLinFlipLimit.lean) contains `source_fullConvergence` for precisely that convergence proposition, `sourceF_eq_f` for the sign/list threshold correspondence, and `mass_transfer_eq_density` for the counting normalization. The explicit logarithmic cutoff and numerical upper bound have the written arguments in the note.

Run the finite checks with Python 3, using its standard library:

```sh
python3 verify.py > checker-output.json
```

They check reflection, matrix products, the Cauchy lower bound, the extension identity, and the reflected-word flip count for all labelled tournaments of orders 1–4 and all words of lengths 0–6; the flip-count checks use nonempty words and repetition counts 1–4. For orders 1–3 and lengths 0–4, direct enumeration of all vertex maps checks the count normalization. Two integer algorithms count the displayed length-10 word in the transitive tournament on 128 vertices. These finite checks support the displayed identities and witness, not an exhaustive classification of TAS paths.

## Permutation-count consequence

The periodic-prefix counts in OEIS A058258 give 4,967,931,050,777 permutations with signature `(++--)^4+++`. Its nineteen edges and eight flips yield `L <= 9/19`. The checker reproduces the tabulated counts by a last-rank recurrence and independently checks the modified signature by inclusion--exclusion over descents. It also checks a strict injective-map lower bound in the transitive tournament on 4,096 vertices. The note credits Banks, Harcharras, Neuwirth and Ricard for the matrix amplification inequality, Luck for the earlier periodic-pattern half bound, and Stein for the older ten-edge permutation count.

## License

CC BY 4.0 (`cc-by-4.0`). Copyright Haobo Ma and Wenlin Zhang.
