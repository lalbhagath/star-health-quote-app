# star-health-quote-app

Automated Star Health Insurance Premium Calculator - Fetches quotes for 4 scenario combinations with automatic DOB-based age calculation.

## Overview

This automation tool simplifies Star Health insurance premium comparison by automatically fetching quotes for four standard scenarios:
- **5L/1yr**: 5 Lakh coverage for 1 year
- **5L/3yr**: 5 Lakh coverage for 3 years
- **10L/1yr**: 10 Lakh coverage for 1 year
- **10L/3yr**: 10 Lakh coverage for 3 years

The calculator automatically computes your age from your date of birth and retrieves premium quotes from the Star Health Quick Quote portal.

## Features

✅ **Automatic Age Calculation** - Calculates age from DOB (YYYY-MM-DD format)  
✅ **Multi-Scenario Quotes** - Fetches all 4 scenarios in a single execution  
✅ **Web Automation** - Uses Selenium for reliable interaction with Star Health portal  
✅ **JSON Output** - Saves results in structured JSON format  

✅ **Multiple Family Members Support** - Supports up to 4 family members with individual DOB tracking
✅ **Automatic Age Calculation** - Calculates age for each family member automatically
✅ **Family Insurance Quotes** - Gets quotes for complete family units (not just individuals)

## ⭐ NEW FEATURE: Multiple Family Members Support!

Now you can get quotes for your **entire family** (up to 4 members) with a single command!

### How It Works:

1. **Define Your Family** - List all family members with their DOB
2. **Automatic Age Calculation** - Script calculates age for each person
3. **Single Quote Execution** - Gets all 4 scenario quotes for your family
4. **Complete Family Data** - Results include all member details and quotes

### Family Member Types:

- `adult` - Working age adults
- `parent` - Senior parents/grandparents
- `child` - Children (if applicable)

### Example - Get Quotes for Your Family:

```python
from star_health_calculator import StarHealthFamilyCalculator

calculator = StarHealthFamilyCalculator()

# Define your family (up to 4 members)
family = [
    {
        'name': 'Father',
        'dob': '1960-05-15',
        'type': 'adult'
    },
    {
        'name': 'Mother',
        'dob': '1962-08-20',
        'type': 'adult'
    },
    {
        'name': 'Son',
        'dob': '1995-03-10',
        'type': 'adult'
    },
    {
        'name': 'Daughter',
        'dob': '1998-12-25',
        'type': 'adult'
    }
]

# Get all quotes for your family
results = calculator.get_all_quotes_for_family(family)

# Display results
print(f"Family: {results['family']}")
print(f"Member Count: {results['member_count']}")
print("\nIndividual Ages:")
for member in results['members']:
    age = calculator.calculate_age(member['dob'])
    print(f"  - {member['name']}: {age} years old")

print("\nQuotes:")
for scenario, premium in results['quotes'].items():
    print(f"  {scenario}: {premium}")

# Save to file
calculator.save_results('family_quotes.json')
calculator.close()
```

### Output Example:

```json
{
  "family": "Father + Mother + Son + Daughter",
  "members": [
    {"name": "Father", "dob": "1960-05-15", "type": "adult"},
    {"name": "Mother", "dob": "1962-08-20", "type": "adult"},
    {"name": "Son", "dob": "1995-03-10", "type": "adult"},
    {"name": "Daughter", "dob": "1998-12-25", "type": "adult"}
  ],
  "member_count": 4,
  "quotes": {
    "5L/1yr": "₹12,500",
    "5L/3yr": "₹31,200",
    "10L/1yr": "₹18,900",
    "10L/3yr": "₹48,100"
  }
}
```
✅ **Configurable** - All scenarios and settings in config.json  
✅ **Error Handling** - Comprehensive error management and logging  

## Prerequisites

- **Python** 3.7 or higher
- **Chrome/Chromium Browser** (for Selenium WebDriver)
- **ChromeDriver** (matches your Chrome version)
- **pip** package manager

## Installation

### Step 1: Clone the repository
```bash
git clone https://github.com/lalbhagath/star-health-quote-app.git
cd star-health-quote-app
```

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set up ChromeDriver
Download ChromeDriver from: https://chromedriver.chromium.org/  
Ensure the version matches your Chrome browser version.

## Configuration

Edit `config.json` to customize:
- **sum_insured**: Coverage amounts (in INR)
- **tenure_years**: Duration (1 or 3 years)
- **browser_wait_timeout**: Maximum time to wait for page elements
- **headless_mode**: Run browser in background (true/false)

## Usage

### Basic Usage

```python
from star_health_calculator import StarHealthCalculator

# Initialize calculator
calculator = StarHealthCalculator()

# Replace with your DOB (YYYY-MM-DD format)
dob = "1990-05-15"

# Get all 4 scenario quotes
results = calculator.get_all_quotes(dob)

# Display results
print(f"Age: {results['age']}")
for scenario, premium in results['quotes'].items():
    print(f"{scenario}: {premium}")

# Save to JSON file
calculator.save_results()

# Close browser
calculator.close()
```

### Command Line Usage

```bash
python star_health_calculator.py
```

Update the DOB in the main block before running.

## Output

The calculator generates `quotes.json` with the following structure:

```json
{
  "dob": "1990-05-15",
  "age": 34,
  "quotes": {
    "5L/1yr": "₹5,500",
    "5L/3yr": "₹14,200",
    "10L/1yr": "₹8,900",
    "10L/3yr": "₹23,100"
  }
}
```

## Scenarios Explained

| Label | Coverage | Tenure | Use Case |
|-------|----------|--------|----------|
| **5L/1yr** | 5 Lakh (₹500,000) | 1 Year | Basic annual protection |
| **5L/3yr** | 5 Lakh (₹500,000) | 3 Years | Long-term basic coverage |
| **10L/1yr** | 10 Lakh (₹1,000,000) | 1 Year | Premium annual protection |
| **10L/3yr** | 10 Lakh (₹1,000,000) | 3 Years | Comprehensive 3-year plan |

## File Structure

```
star-health-quote-app/
├── star_health_calculator.py   # Main automation script
├── config.json                 # Scenario configurations
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── quotes.json                 # Output file (generated)
└── .gitignore                  # Git ignore rules
```

## Troubleshooting

### Issue: "ChromeDriver not found"
**Solution**: Ensure ChromeDriver is in your PATH or update the driver path in the script.

### Issue: "Element not found" error
**Solution**: Star Health portal layout may have changed. Update CSS selectors in the script.

### Issue: Timeout errors
**Solution**: Increase `browser_wait_timeout` in config.json or your system internet speed.

### Issue: Age calculation errors
**Solution**: Ensure DOB format is YYYY-MM-DD (e.g., 1990-05-15)

## API Reference

### StarHealthCalculator

#### `__init__()`
Initializes the calculator and sets up Selenium WebDriver.

#### `calculate_age(dob_str)`
- **Parameters**: dob_str (str) - Date of birth in YYYY-MM-DD format
- **Returns**: int - Age in years

#### `fetch_quote(age, sum_insured, tenure)`
- **Parameters**:
  - age (int): Person's age
  - sum_insured (int): Coverage amount in INR
  - tenure (int): Duration in years
- **Returns**: str - Premium amount

#### `get_all_quotes(dob)`
- **Parameters**: dob (str) - Date of birth in YYYY-MM-DD format
- **Returns**: dict - Results with age and all 4 scenario quotes

#### `save_results(filename)`
- **Parameters**: filename (str) - Output JSON filename (default: quotes.json)
- **Returns**: None

#### `close()`
Closes the browser and cleans up resources.

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - See LICENSE file for details

## Disclaimer

This tool is for educational and personal use. Star Health Insurance terms and conditions apply. Always verify quotes directly with Star Health for accuracy.

## Support

For issues or questions, please open an issue on GitHub: https://github.com/lalbhagath/star-health-quote-app/issues
