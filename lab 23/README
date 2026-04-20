# FedSpeak 2.0 — NLP Pipeline for Central Bank Communications

## Objective

Built and repaired a production-style NLP pipeline for Federal Reserve minutes, combining domain-specific sentiment analysis, TF-IDF feature engineering, and sentence-transformer embeddings to study policy communication and predict monetary tightening regimes.

## Key Tasks

- Diagnosed and fixed three core NLP pipeline failures:
  - naive whitespace tokenization
  - incorrect sentiment dictionary selection
  - poorly specified TF-IDF parameters
- Corrected preprocessing with lowercasing, regex cleanup, `nltk.word_tokenize`, stop-word removal, and lemmatization
- Replaced the Harvard General Inquirer with the Loughran–McDonald financial dictionary
- Rebuilt TF-IDF features using stronger document-frequency filtering and bigrams
- Encoded FOMC minutes using the `all-MiniLM-L6-v2` sentence-transformer model
- Compared TF-IDF and embedding-based clustering
- Evaluated predictive performance of both representations in a time-ordered classification setting
- Packaged the final workflow into a reusable `fomc_sentiment.py` module

## Key Findings

- The repaired preprocessing pipeline removed punctuation-attached artifacts and improved text quality.
- Domain-specific sentiment scoring substantially reduced false positives relative to the generic dictionary benchmark.
- Sentence-transformer embeddings captured semantic structure effectively, but TF-IDF performed better on the final prediction task.
- **TF-IDF achieved the higher AUC (0.811), compared with embeddings (0.721).**
- The result suggests that Fed tightening regimes are closely associated with distinctive policy vocabulary, which sparse lexical features capture especially well.

## Repo Structure

- `notebooks/lab-ch23-diagnostic.ipynb` : main lab notebook
- `src/fomc_sentiment.py` : reusable FOMC text analysis module
- `README.md` : project summary

## Methods Used

- NLP pipeline debugging
- Financial text preprocessing
- Loughran–McDonald sentiment analysis
- TF-IDF vectorization
- Sentence-transformer embeddings
- K-means clustering
- TimeSeriesSplit evaluation
- Logistic regression classification
- AUC-based model comparison
