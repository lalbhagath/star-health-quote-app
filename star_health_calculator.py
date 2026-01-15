import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

class StarHealthFamilyCalculator:
    """
    ENHANCED: Automates Star Health Insurance Premium Calculation
    NOW SUPPORTS UP TO 4 FAMILY MEMBERS!
    
    Fetches quotes for 4 scenarios with multiple family members:
    - 5L/1yr (5 Lakh, 1 Year)
    - 5L/3yr (5 Lakh, 3 Years)
    - 10L/1yr (10 Lakh, 1 Year)
    - 10L/3yr (10 Lakh, 3 Years)
    """
    
    def __init__(self):
        self.quotes = {}
        self.driver = None
        self.quote_url = "https://atom.starhealth.in/quickquote"
        
    def calculate_age(self, dob_str):
        """
        Calculate age from Date of Birth (YYYY-MM-DD format)
        """
        dob = datetime.strptime(dob_str, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    
    def fetch_quote_for_family(self, family_members, sum_insured, tenure):
        """
        Fetch quote from Star Health for multiple family members
        
        Args:
            family_members: List of dicts with member info
                Example: [
                    {'name': 'Father', 'dob': '1960-01-15', 'type': 'adult'},
                    {'name': 'Mother', 'dob': '1962-05-20', 'type': 'adult'},
                    {'name': 'Son', 'dob': '1995-03-10', 'type': 'adult'},
                    {'name': 'Daughter', 'dob': '1998-07-25', 'type': 'adult'}
                ]
            sum_insured: Coverage amount (e.g., 500000 for 5L)
            tenure: Duration in years (1 or 3)
        
        Returns:
            Premium amount
        """
        try:
            if self.driver is None:
                self.driver = webdriver.Chrome()
            
            self.driver.get(self.quote_url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input"))
            )
            
            # Calculate ages for all family members
            members_info = []
            for member in family_members:
                age = self.calculate_age(member['dob'])
                members_info.append({'name': member['name'], 'age': age, 'type': member['type']})
            
            # Get highest adult age
            highest_adult_age = max([m['age'] for m in members_info if m['type'] in ['adult', 'parent']])
            
            # Fill Age of Highest Adult
            age_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
            for inp in age_inputs:
                try:
                    if 'age' in inp.get_attribute('placeholder').lower():
                        inp.clear()
                        inp.send_keys(str(highest_adult_age))
                        break
                except:
                    pass
            
            # Select sum insured
            sum_insured_dropdowns = self.driver.find_elements(By.CSS_SELECTOR, "select")
            for dropdown in sum_insured_dropdowns:
                try:
                    options = dropdown.find_elements(By.TAG_NAME, "option")
                    for option in options:
                        if '5,00,000' in option.text if sum_insured == 500000 else '10,00,000' in option.text:
                            option.click()
                            break
                except:
                    pass
            
            # Select tenure
            tenure_dropdowns = self.driver.find_elements(By.CSS_SELECTOR, "select")
            for dropdown in tenure_dropdowns:
                try:
                    options = dropdown.find_elements(By.TAG_NAME, "option")
                    for option in options:
                        if str(tenure) in option.text:
                            option.click()
                            break
                except:
                    pass
            
            # Click get quote button
            buttons = self.driver.find_elements(By.CSS_SELECTOR, "button")
            for button in buttons:
                if 'quote' in button.text.lower() or 'get' in button.text.lower():
                    button.click()
                    break
            
            # Wait and extract premium
            time.sleep(3)
            premium_text = self.driver.find_element(By.CSS_SELECTOR, ".premium-amount").text
            
            return premium_text
        
        except Exception as e:
            print(f"Error fetching quote: {str(e)}")
            return None
    
    def get_all_quotes_for_family(self, family_members):
        """
        Get all 4 scenario quotes for a family with multiple members
        
        Args:
            family_members: List of family member dicts with dob info
        
        Returns:
            Dictionary with all quotes for the family
        """
        scenarios = [
            {'sum_insured': 500000, 'tenure': 1, 'label': '5L/1yr'},
            {'sum_insured': 500000, 'tenure': 3, 'label': '5L/3yr'},
            {'sum_insured': 1000000, 'tenure': 1, 'label': '10L/1yr'},
            {'sum_insured': 1000000, 'tenure': 3, 'label': '10L/3yr'},
        ]
        
        family_name = " + ".join([m['name'] for m in family_members])
        
        results = {
            'family': family_name,
            'members': family_members,
            'member_count': len(family_members),
            'quotes': {}
        }
        
        for scenario in scenarios:
            print(f"Fetching {scenario['label']} for {family_name}...")
            premium = self.fetch_quote_for_family(family_members, scenario['sum_insured'], scenario['tenure'])
            results['quotes'][scenario['label']] = premium
            time.sleep(2)
        
        self.quotes = results
        return results
    
    def save_results(self, filename='family_quotes.json'):
        """
        Save results to JSON file
        """
        with open(filename, 'w') as f:
            json.dump(self.quotes, f, indent=2)
        print(f"Results saved to {filename}")
    
    def close(self):
        """
        Close the browser
        """
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    calculator = StarHealthFamilyCalculator()
    
    # EXAMPLE: Define your family members (up to 4)
    # Change these to match your actual family!
    family = [
        {
            'name': 'Father',
            'dob': '1960-05-15',
            'type': 'adult'  # Can be: adult, parent, child
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
    
    try:
        results = calculator.get_all_quotes_for_family(family)
        
        print("\n" + "="*60)
        print("STAR HEALTH FAMILY INSURANCE QUOTES")
        print("="*60)
        print(f"\nFamily: {results['family']}")
        print(f"Members: {results['member_count']}")
        print(f"\nIndividual Ages:")
        for member in results['members']:
            age = calculator.calculate_age(member['dob'])
            print(f"  - {member['name']}: {age} years old")
        
        print(f"\nQuotes:")
        for scenario, premium in results['quotes'].items():
            print(f"  {scenario}: {premium}")
        
        calculator.save_results()
    
    finally:
        calculator.close()
