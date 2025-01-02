import pandas as pd
import unicodedata
import re

def sanitize_text(text):
    # Ensure the input is a string
    if not isinstance(text, str):
        return text

    # Normalize the text to decompose special characters
    text = unicodedata.normalize('NFD', text)
    
    # Remove diacritics by filtering combining characters
    text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Mn')

    # Replace specific characters with their English equivalents
    replacements = {
        'ß': 'ss',   # German sharp S
        'ı': 'i',    # Turkish dotless i
        'ö': 'o',    # German, Turkish, etc.
        'ü': 'u',    # German, Turkish, etc.
        'ä': 'a',    # German
        'å': 'a',    # Scandinavian
        'æ': 'ae',   # Scandinavian
        'ø': 'o',    # Scandinavian
        'ç': 'c',    # Turkish, French
        'ğ': 'g',    # Turkish
        'ş': 's',    # Turkish
        'ñ': 'n',    # Spanish
        'é': 'e',    # French, Spanish, etc.
        'è': 'e',    # French
        'ê': 'e',    # French
        'ë': 'e',    # French
        'à': 'a',    # French, Italian
        'á': 'a',    # Spanish, Portuguese
        'â': 'a',    # French
        'í': 'i',    # Spanish, Portuguese
        'î': 'i',    # French
        'ï': 'i',    # French
        'ó': 'o',    # Spanish, Portuguese
        'ô': 'o',    # French
        'ò': 'o',    # Italian
        'ú': 'u',    # Spanish, Portuguese
        'û': 'u',    # French
        'ý': 'y',    # Czech, Slovak, etc.
        'ž': 'z',    # Czech, Slovak, etc.
        'č': 'c',    # Czech, Slovak, etc.
        'ř': 'r',    # Czech
        'ů': 'u',    # Czech
        'ł': 'l',    # Polish
        'ż': 'z',    # Polish
        'ź': 'z',    # Polish
        'ę': 'e',    # Polish
        'ą': 'a',    # Polish
        'õ': 'o',    # Estonian
        'ì': 'i',    # Italian
        'ò': 'o',    # Italian
        'î': 'i',    # French
        'ů': 'u',    # Czech
        'č': 'c',    # Czech
    }

    for key, value in replacements.items():
        text = text.replace(key, value)

    # Convert to lowercase
    text = text.lower()

    # Remove any remaining non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', '', text)

    return text

def sanitize_csv(input_csv, output_csv):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv)

    # Apply the sanitize_text function to all string columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(sanitize_text)

    # Save the sanitized DataFrame to a new CSV file
    df.to_csv(output_csv, index=False)
    print(f"Sanitized CSV saved to {output_csv}")

# Example usage
input_csv_path = "C:\\Users\\Ege S\\Downloads\\test_input.csv"  # Replace with your input CSV file path
output_csv_path = "output_sanitized.csv"  # Replace with your desired output file path

sanitize_csv(input_csv_path, output_csv_path)
