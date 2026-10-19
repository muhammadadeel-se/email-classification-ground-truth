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
            "Hi team, I am planning a road trip with my family from {date_start} to {date_end}. Do you have any mid-size SUVs available at the downtown branch?",
        ),
        (
            "Car rental quote question",
            "Hello, looking to check if I can secure a vehicle for next weekend. My dates are roughly {date_start} through {date_end}. Let me know what compact options are left.",
        ),
        (
            "Fleet availability inquiry",
            "Are there any 7-seater vans open for the upcoming holiday week? We need something spacious for luggage.",
        ),
        (
            "Holding a booking without immediate payment",
            "Is it possible to pencil in a reservation for {date_start} while I finalize my flight details, or do I need to pay upfront?",
        ),
    ],
    "Cancellation Request": [
        (
            "Need to pull out of my upcoming booking",
            "Hey support, my travel plans changed due to an emergency and I won't be needing the car booked for {date_start}. Please process whatever cancellation steps are necessary.",
        ),
        (
            "Stopping my reservation",
            "I unfortunately have to call off my trip. Please terminate my reservation reference #{ticket_num}. Let me know if there's any penalty fee.",
        ),
        (
            "Reversing my rental arrangement",
            "Due to flight cancellations, I am dropping my booking for next week. I do not want to keep the car reservation active anymore.",
        ),
        (
            "Unsure cancellation policy check",
            "I don't want to cancel just yet, but I need to know your exact policy if I do pull out 48 hours prior.",
        ),
    ],
    "Payment Issue": [
        (
            "Card declined on checkout",
            "Every time I try to complete my deposit payment using my Visa ending in {cc_last}, the transaction fails with an error code. I know funds are available.",
        ),
        (
            "Double billed for my rental",
            "Looking at my bank statement this morning, I noticed two identical charges from your company for the same booking ID. Can someone look into this billing error?",
        ),
        (
            "Card update and charge question",
            "The charge on my statement from Tuesday doesn't match my tier. Also, my card expired so I need to update my billing details before final settlement.",
        ),
        (
            "Receipt request and payment failure",
            "My payment didn't process correctly on the mobile app earlier. Can you send a fresh payment link or manual invoice?",
        ),
    ],
    "Vehicle Damage Report": [
        (
            "Scratch on bumper upon pickup",
            "Hi, I just picked up vehicle plate #{plate} and noticed a 3-inch scratch on the rear bumper that wasn't marked on the check-out sheet.",
        ),
        (
            "Minor dent during my trip",
            "While parked outside a coffee shop yesterday, another car bumped into the passenger side door, leaving a minor dent. Let me know how to file an incident report.",
        ),
        (
            "Windshield chip from highway debris",
            "Driving down the highway earlier today, a loose stone flew off a truck and chipped the front windshield right in the driver's line of sight.",
        ),
        (
            "Post-return damage dispute",
            "I returned the vehicle yesterday morning. Just received an email about a wheel rim scrape, but that scuff was already present when I took delivery.",
        ),
    ],
    "General Feedback": [
        (
            "Amazing experience with staff",
            "Just wanted to leave a quick note commending Sarah at the front desk. She was exceptionally helpful when our travel plans got chaotic. Great service overall!",
        ),
        (
            "App interface suggestion",
            "Your mobile app is mostly straightforward, but it would be super helpful if you added a dark mode toggle and saved payment methods securely.",
        ),
        (
            "Overall thoughts on vehicle condition",
            "The car ran smoothly during our trip, though the interior smelled faintly of smoke when we first got in. Might want to check detailing before the next renter.",
        ),
        (
            "Great service, minor delay",
            "Pickup took a bit longer than expected due to system updates at the counter, but once assisted, everything went smoothly. Thanks!",
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
      template_subject, template_body = random.choice(category_templates)

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

      # Add occasional lowercase noise
      if random.random() < 0.15:
        body = body.lower()

      data.append({
          "email_id": f"EML-{email_id_counter}",
          "subject": subject,
          "body": body,
          "category": category,
      })
      email_id_counter += 1

  df = pd.DataFrame(data)
  df = df.sample(frac=1, random_state=42).reset_index(drop=True)
  return df


if __name__ == "__main__":
  df_dataset = generate_dataset(200)

  # 1. Verify shape as requested by mentor
  print("Dataset Shape (should be 200, 4):", df_dataset.shape)

  # 2. Verify all five categories are represented
  print("\nCategory Value Counts:")
  print(df_dataset["category"].value_counts())

  # 3. Write directly to emails.csv in root directory
  output_filename = "emails.csv"
  df_dataset.to_csv(output_filename, index=False)
  print(f"\nSuccessfully generated and saved to '{output_filename}'!")