# DIGBUG – Pre/Post-processing Operator Selection for Accurate Bug Localization

This repository shares code used for the DIGBUG project.

## What it is?
DIGBUG is a bug localization approach that investigates the attributes of each bug report and analyzes effects of pre/post-processing operators to improve IRBL (Informtion Retrieval based Bug Localization) performance.

## How it works?
DIGBUG works based on the investigation of attributes of each bug report (each of them has its own attributes (e.g., reporter type, presence of code entity, etc.)). It classifies bug reports into different buckets (splitted by attributs) and applies every possible combination of pre/post-processing operators to pick the best one for each.

## Evaluation
We evaluated DIGBUG by leveraging the data from D&C [1] to train a model that classifies bug reports into multiple buckets and utilized the data from Bench4BL [2] to test the approach.

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
}
```


[1] A. Koyuncu, T. F. Bissyandé, D. Kim, K. Liu, J. Klein, M. Monperrus, Y. L. Traon, D&c: A divide-and-conquer approach to IR-based bug localization, arXiv:1902.02703 [cs] (2019).

[2] J. Lee, D. Kim, T. F. Bissyandé, W. Jung, Y. Le Traon, Bench4bl: Reproducibility study on the performance of IR-based bug localization, in: Proceedings of the 27th ACM SIGSOFT International Symposium on Software Testing and Analysis, ISSTA 2018, ACM, 2018, pp. 61–72.
