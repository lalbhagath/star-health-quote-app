import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

class StarHealthCalculator:
    """
    Automates Star Health Insurance Premium Calculation
    Fetches quotes for 4 scenarios:
    - 5L/1yr (5 Lakh, 1 Year)
    - 5L/3yr (5 Lakh, 3 Years)
    - 10L/1yr (10 Lakh, 1 Year)
    - 10L/3yr (10 Lakh, 3 Years)
    """
    
    def __init__(self):
        self.quotes = {}
        self.driver = None
        # Star Health Quick Quote URL
        self.quote_url = "https://atom.starhealth.in/quickquote"
        
    def calculate_age(self, dob_str):
        """
        Calculate age from Date of Birth (YYYY-MM-DD format)
        """
        dob = datetime.strptime(dob_str, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    
    def fetch_quote(self, age, sum_insured, tenure):
        """
        Fetch quote from Star Health for given parameters
        
        Args:
            age: Age of the person
            sum_insured: Coverage amount (e.g., 500000 for 5L)
            tenure: Duration in years (1 or 3)
        
        Returns:
            Premium amount
        """
        try:
            if self.driver is None:
                self.driver = webdriver.Chrome()
            
            self.driver.get(self.quote_url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input"))
            )
            
            # Fill age
            age_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
            for inp in age_inputs:
                if 'age' in inp.get_attribute('placeholder').lower() or 'age' in inp.get_attribute('name').lower():
                    inp.clear()
                    inp.send_keys(str(age))
                    break
            
            # Select sum insured
            sum_insured_options = self.driver.find_elements(By.CSS_SELECTOR, "select option")
            for option in sum_insured_options:
                if str(sum_insured) in option.text or '5,00,000' in option.text if sum_insured == 500000 else False:
                    option.click()
                    break
            
            # Select tenure
            tenure_options = self.driver.find_elements(By.CSS_SELECTOR, "select option")
            for option in tenure_options:
                if str(tenure) in option.text:
                    option.click()
                    break
            
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
    
    def get_all_quotes(self, dob):
        """
        Get all 4 scenario quotes for a given DOB
        
        Args:
            dob: Date of Birth in YYYY-MM-DD format
        
        Returns:
            Dictionary with all quotes
        """
        age = self.calculate_age(dob)
        
        scenarios = [
            {'sum_insured': 500000, 'tenure': 1, 'label': '5L/1yr'},
            {'sum_insured': 500000, 'tenure': 3, 'label': '5L/3yr'},
            {'sum_insured': 1000000, 'tenure': 1, 'label': '10L/1yr'},
            {'sum_insured': 1000000, 'tenure': 3, 'label': '10L/3yr'},
        ]
        
        results = {
            'dob': dob,
            'age': age,
            'quotes': {}
        }
        
        for scenario in scenarios:
            print(f"Fetching quote for {scenario['label']}...")
            premium = self.fetch_quote(age, scenario['sum_insured'], scenario['tenure'])
            results['quotes'][scenario['label']] = premium
            time.sleep(2)  # Add delay between requests
        
        self.quotes = results
        return results
    
    def save_results(self, filename='quotes.json'):
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
    # Example usage
    calculator = StarHealthCalculator()
    
    # Replace with actual DOB in YYYY-MM-DD format
    dob = "1990-05-15"  # Example: 1990-05-15
    
    try:
        results = calculator.get_all_quotes(dob)
        print("\n=== Star Health Insurance Quotes ===")
        print(f"DOB: {results['dob']}")
        print(f"Age: {results['age']}")
        print("\nQuotes:")
        for scenario, premium in results['quotes'].items():
            print(f"  {scenario}: {premium}")
        
        calculator.save_results()
    
    finally:
        calculator.close()
