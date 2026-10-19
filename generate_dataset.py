import os
import random
import pandas as pd
from faker import Faker

# Initialize Faker with a fixed seed for reproducibility
fake = Faker()
Faker.seed(42)
random.seed(42)

# Define the 5 exact categories required
CATEGORIES = [
    "Reservation Inquiry",
    "Cancellation Request",
    "Payment Issue",
    "Vehicle Damage Report",
    "General Feedback",
]

# Rich, nuanced templates designed to prevent simple keyword shortcuts
TEMPLATES = {
    "Reservation Inquiry": [
        (
            "Booking availability for next month",
            "Hi team, I am planning a road trip with my family from {date_start} to {date_end}. Do you have any mid-size SUVs available at the downtown branch? Also wondering if additional drivers can be added without extra fees.",
        ),
        (
            "Car rental quote question",
            "Hello, looking to check if I can secure a vehicle for next weekend. My dates are a bit fluid, but roughly {date_start} through {date_end}. Let me know what compact options are left.",
        ),
        (
            "Fleet availability inquiry",
            "Quick question regarding vehicle availability. Are there any 7-seater vans open for the upcoming holiday week? We need something spacious for luggage.",
        ),
        (
            "Holding a booking without immediate payment",
            "Is it possible to pencil in a reservation for {date_start} while I finalize my flight details, or do I need to pay upfront to hold the vehicle?",
        ),
    ],
    "Cancellation Request": [
        (
            "Need to pull out of my upcoming booking",
            "Hey support, my travel plans changed drastically due to a family emergency and I won't be needing the car booked for {date_start}. Please process whatever cancellation steps are necessary on your end.",
        ),
        (
            "Stopping my reservation",
            "I unfortunately have to call off my trip. Please terminate my reservation reference #{ticket_num}. Let me know if there's any penalty fee applied to my account.",
        ),
        (
            "Reversing my rental arrangement",
            "Due to flight cancellations out of my control, I am dropping my booking for next week. I do not want to keep the car reservation active anymore.",
        ),
        (
            (
                "Don't want to lose my spot, but might need to back out"
            ),  # Edge case: contains "cancel" or similar intent check
            "I am writing because my schedule is up in the air. I don't want to cancel my subscription or booking just yet, but I need to know your exact policy if I do pull out 48 hours prior.",
        ),
    ],
    "Payment Issue": [
        (
            "Card declined on checkout",
            "Every time I try to complete my deposit payment using my Visa ending in {cc_last}, the transaction fails with an error code. I know funds are available, so I'm not sure why my payment isn't going through.",
        ),
        (
            "Double billed for my rental",
            "Looking at my bank statement this morning, I noticed two identical charges from your company for the same booking ID. Can someone look into this billing error and issue a correction?",
        ),
        (
            "Invoice and card update",
            "The charge on my statement from Tuesday doesn't match the tier I signed up for during the promo. Also, my card expired so I need to update my billing details before the final settlement.",
        ),
        (
            "Receipt request and payment failure",
            "My payment didn't process correctly on the mobile app earlier. Can you send a fresh payment link or manual invoice so I can clear my balance?",
        ),
    ],
    "Vehicle Damage Report": [
        (
            "Scratch on bumper upon pickup",
            "Hi, I just picked up the keys for vehicle plate #{plate} and noticed a noticeable 3-inch scratch on the rear bumper that wasn't marked on the check-out sheet. Attaching photos just in case.",
        ),
        (
            "Minor dent during my trip",
            "Regrettably, while parked outside a coffee shop yesterday, another car bumped into the passenger side door, leaving a minor dent. Let me know how to file an incident report.",
        ),
        (
            "Windshield chip from highway debris",
            "Driving down the highway earlier today, a loose stone flew off a truck and chipped the front windshield right in the driver's line of sight. Reporting this immediately as requested.",
        ),
        (
            "Post-return damage dispute",
            "I returned the vehicle yesterday morning. Just received an email about a wheel rim scrape, but that scuff was already present when I took delivery of the car last week.",
        ),
    ],
    "General Feedback": [
        (
            "Amazing experience with staff",
            "Just wanted to leave a quick note commending Sarah at the front desk. She was exceptionally helpful when our travel plans got chaotic. Great customer service overall!",
        ),
        (
            "App interface suggestion",
            "Your mobile app is mostly straightforward, but it would be super helpful if you added a dark mode toggle and saved payment methods securely for faster checkouts.",
        ),
        (
            "Overall thoughts on vehicle condition",
            "The car ran smoothly during our trip, though the interior smelled faintly of smoke when we first got in. Might want to check the detailing before the next renter.",
        ),
        (
            "Great service, minor delay",
            "Pickup took a bit longer than expected due to system updates at the counter, but once assisted, everything went smoothly. Thanks for the smooth ride!",
        ),
    ],
}


def generate_dataset(total_rows=200):
  rows_per_category = total_rows // len(CATEGORIES)
  data = []
  email_id_counter = 1001

  for category in CATEGORIES:
    category_templates = TEMPLATES[category]

    for _ in range(rows_per_category):
      # Pick a template variation
      template_subject, template_body = random.choice(category_templates)

      # Inject dynamic random data using Faker & random values to create realistic noise
      subject = (
          f"{template_subject} - {fake.word().capitalize()}"
          if random.random() > 0.5
          else template_subject
      )
      body = (
          template_body.format(
              date_start=fake.date_between(
                  start_date="+1d", end_date="+15d"
              ).strftime("%B %d"),
              date_end=fake.date_between(
                  start_date="+16d", end_date="+30d"
              ).strftime("%B %d"),
              ticket_num=fake.random_number(digits=6, fix_len=True),
              cc_last=fake.random_number(digits=4, fix_len=True),
              plate=fake.bothify(text="???-###", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
          )
          + f" Regards, {fake.first_name()}."
      )

      # Add occasional human typing noise (typos or lowercase sentences)
      if random.random() < 0.15:
        body = body.lower()  # lowercase noise

      data.append({
          "email_id": f"EML-{email_id_counter}",
          "subject": subject,
          "body": body,
          "category": category,
      })
      email_id_counter += 1

  df = pd.DataFrame(data)
  # Shuffle dataset so categories are mixed
  df = df.sample(frac=1, random_state=42).reset_index(drop=True)
  return df


if __name__ == "__main__":
  output_dir = "data"
  os.makedirs(output_dir, exist_ok=True)
  output_path = os.path.join(output_dir, "emails_ground_truth.csv")

  df_dataset = generate_dataset(200)
  df_dataset.to_csv(output_path, index=False)
  print(
      f"Successfully generated {len(df_dataset)} rows across"
      f" {df_dataset['category'].nunique()} categories at '{output_path}'."
  )