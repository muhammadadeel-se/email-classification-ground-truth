# Synthetic Email Ground Truth Dataset

## Overview
This repository contains a reproducible Python script (`generate_dataset.py`) that generates a ground-truth dataset of 200 realistic synthetic customer service emails (`emails.csv`). The dataset is engineered to prevent models from relying on superficial keyword shortcuts (such as matching words like "cancel" or "payment"), ensuring classifiers rely on true semantic context and nuance.

## Dataset Schema
The output CSV (`emails.csv`) contains the following columns:
* **email_id**: Unique identifier for each record (e.g., `EML-1001`).
* **subject**: Subject line of the email.
* **body**: Simulated email body incorporating realistic variables (dates, ticket numbers, card suffixes, license plates, and names).
* **category**: The ground-truth classification label.

## Categories & Labeling Guidelines
The dataset represents five core categories:
1. **Reservation Inquiry**: Questions regarding vehicle availability, rental dates, quotes, or holding bookings.
2. **Cancellation Request**: Communications requesting to terminate, call off, or cancel an active reservation, including policy inquiries.
3. **Payment Issue**: Transaction failures, declined credit cards, double billing, card updates, or receipt requests.
4. **Vehicle Damage Report**: Incidents involving scratches, dents, windshield chips, or pre-existing damage disputes.
5. **General Feedback**: App suggestions, compliments, or general comments regarding service and vehicle conditions.

## Methodology & Realism
* **Faker Integration**: Utilized the `Faker` library combined with randomized templates to dynamically generate realistic contextual details.
* **Realism & Noise**: Incorporated varied tones, mixed salutations, overlapping terminology (e.g., cancellation terms appearing in billing inquiries), and occasional lowercase formatting noise to mimic authentic human communication.
* **Balanced Distribution**: Exactly 200 rows divided equally across all five categories (40 rows per category) and shuffled for training and evaluation readiness.

## How to Run
1. Install required dependencies:
   ```bash
   pip install pandas faker