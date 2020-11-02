# DIGBUG – Pre/Post-processing Operator Selection for Accurate Bug Localization

This repository shares code used for the DIGBUG project.
http://code-search.uni.lu/facoy

## What it is?
DIGBUG is a bug localization approach that investigates the attributes of each bug report and analyzes effects of pre/post-processing operators to improve IRBL (Informtion Retrieval based Bug Localization) performance.

## How it works?
DIGBUG works based on the investigation of attributes of each bug report (each of them has its own attributes (e.g., reporter type, presence of code entity, etc.)). It classifies bug reports into different buckets (splitted by attributs) and applies every possible combination of pre/post-processing operators to pick the best one for each.

## Maintance
@FalconLK Kisub Kim
@Deadlyelder Sankalp
@darksw Dongsun Kim


## Citation
```
@inproceedings{kim2020digbug,
  title={DIGBUG – Pre/Post-processing Operator Selection for Accurate Bug Localization},
  author={Kim, Kisub and Ghatpande, Sankalp, and Liu, Kui and Anil, Koyuncu and Kim, Dongsun and Bissyande, Tegawende F and Klein, Jacques and Le Traon, Yves},
  booktitle={under review},
  year={2020}
}```
