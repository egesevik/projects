import pandas as pd
import itertools

def generate_email_addresses(names_csv, domains_file, output_csv):
    # Read the names CSV
    names_df = pd.read_csv(names_csv)

    # Ensure the CSV contains the required columns
    if not {'Name', 'Surname'}.issubset(names_df.columns):
        raise ValueError("The input CSV must contain 'Name' and 'Surname' columns.")

    # Read the domains from the text file
    with open(domains_file, 'r') as file:
        domains = [line.strip() for line in file.readlines()]

    # Normalize and sanitize the names and surnames
    def sanitize(text):
        return text.strip().lower()

    names_df['Name'] = names_df['Name'].apply(sanitize)
    names_df['Surname'] = names_df['Surname'].apply(sanitize)

    # Generate email address combinations
    email_combinations = []
    for _, row in names_df.iterrows():
        name, surname = row['Name'], row['Surname']

        # Generate combinations for each domain
        for domain in domains:
            email_combinations.extend([
                f"{name}{surname}@{domain}",
                f"{name}.{surname}@{domain}",
                f"{surname}{name}@{domain}",
                f"{surname}.{name}@{domain}",
                f"{name}@{domain}",
                f"{surname}@{domain}"
            ])

    # Create a DataFrame for the results
    emails_df = pd.DataFrame({'Email': email_combinations})

    # Save to a CSV file
    emails_df.to_csv(output_csv, index=False)
    print(f"Email combinations saved to {output_csv}")

# Example usage
names_csv_path = "names.csv"  # Replace with the path to the names CSV file
domains_file_path = "domains.txt"  # Replace with the path to the domains file
output_csv_path = "emails_generated.csv"  # Replace with the desired output file path

generate_email_addresses(names_csv_path, domains_file_path, output_csv_path)
