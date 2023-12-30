# pd.analyzer scripts
======

A section for standalone scripts and intended to be run on-demand. 

### scripts/pdictionary.py

In the event of new pose dataset, this script has to be rerun to process and update the reference dictionary which is used for pose recognition service, dictionary module, etc.

All pose data from external resources (such as books) for the pole dictionary are stored in:

```
├── data
│   ├── external
│   │   ├── advanced # Pose PNG Images here
│   │   ├── beginner
│   │   ├── intermediate
│   │   └── pdictionary.csv
```

Running this script on command shell will process all pose images per category and concatenate them in `pdictionary.csv`, which will be used in the dictionary module.

```
python3 scripts/pdictionary.py
```

--------------------------------------------

## resources
1. https://www.goodreads.com/book/show/43151907-pole-dance-fitness
2. https://eu.polejunkie.com/products/spin-city-the-ultimate-pole-bible-6th-edition