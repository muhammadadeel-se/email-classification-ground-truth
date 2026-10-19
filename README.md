# Synthetic Email Ground Truth Dataset

## Overview
This repository contains a Python script and a generated 200-row synthetic dataset designed to train and evaluate email classification models. To prevent models from relying on superficial keyword shortcuts (e.g., matching the word "cancel"), the dataset incorporates semantic nuance, mixed tones, overlapping terminology, and realistic human noise (such as lowercase text and variable formatting).

## Dataset Schema
The output CSV (`data/emails_ground_truth.csv`) contains the following columns:
* **email_id**: Unique identifier for each email record (e.g., `EML-1001`).
* **subject**: Subject line of the email.
* **body**: Simulated message body containing contextual nuance and variables.
* **category**: The ground truth label assigned to the email.

## Categories & Labeling Guidelines
The dataset represents five core business categories:
1. **Reservation Inquiry**: Questions regarding vehicle availability, date changes, holding bookings, or rental quotes.
2. **Cancellation Request**: Communications requesting to terminate, pull out of, or cancel an active reservation.
3. **Payment Issue**: Transaction failures, declined credit cards, double billing, or receipt requests.
4. **Vehicle Damage Report**: Incidents involving scratches, dents, windshield chips, or pre-existing damage disputes.
5. **General Feedback**: Compliments, app feature suggestions, or general comments regarding customer service or vehicle condition.

## How to Run the Script
1. Install the required dependencies:
   ```bash
   pip install pandas faker