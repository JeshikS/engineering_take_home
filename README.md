# engineering_take_home
# Engineering Take-Home Assignment

## Overview

This project is an automated lead generation and outreach pipeline that:

1. Accepts a company domain as input.
2. Retrieves company information using Apollo.
3. Finds similar companies using a custom similarity scoring algorithm.
4. Discovers decision makers and work emails using Hunter.
5. Generates personalized outreach emails.
6. Sends emails using Brevo.
7. Supports a safe test mode to prevent accidental outreach during development.

---

## Architecture

```text
Input Domain
      │
      ▼
Apollo Company Lookup
      │
      ▼
Similar Company Finder
      │
      ▼
Hunter Contact Discovery
      │
      ▼
Decision Maker Filter
      │
      ▼
Email Template Generator
      │
      ▼
Brevo Email Sender
```

---

## Features

### Company Discovery

Uses Apollo to retrieve:

* Company name
* Industry information
* Keywords
* Employee count
* Website
* LinkedIn profile

### Similar Company Discovery

A custom similarity scoring algorithm ranks companies based on:

* Industry overlap
* Keyword overlap
* Employee count similarity

### Contact Discovery

Uses Hunter Domain Search API to discover:

* First name
* Last name
* Job title
* Work email
* Email confidence score

### Decision Maker Filtering

Filters contacts to prioritize:

* Chief Executive Officer (CEO)
* Chief Technology Officer (CTO)
* Chief Financial Officer (CFO)
* Chief Operating Officer (COO)
* Chief Marketing Officer (CMO)
* Vice Presidents (VPs)
* Directors
* Heads of Departments
* Founders and Co-Founders

### Email Outreach

Generates personalized emails and sends them using Brevo.

### Test Mode

All emails can be redirected to a personal email address for testing purposes.

---

## Project Structure

```text
engineering_take_home/
│
├── main.py
│
├── pipeline/
│   ├── lead_pipeline.py
│   └── similar_company_finder.py
│
├── services/
│   ├── apollo.py
│   ├── hunter.py
│   └── brevo.py
│
├── utils/
│   ├── contact_filter.py
│   ├── email_template.py
│   ├── file_utils.py
│   └── logger.py
│
├── output/
│
├── requirements.txt
├── .env
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd engineering_take_home
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
APOLLO_API_KEY=

HUNTER_API_KEY=

BREVO_API_KEY=
BREVO_SENDER_NAME=
BREVO_SENDER_EMAIL=

TEST_EMAIL=
```

---

## Usage

### Normal Mode

Emails are sent to discovered contacts.

```bash
python main.py stripe.com
```

### Test Mode

Emails are redirected to the configured test email.

```bash
python main.py stripe.com --test
```

---

## Example Workflow

Input:

```text
stripe.com
```

Pipeline:

```text
Stripe
 ↓
Find Similar Companies
 ↓
PayPal
PhonePe
Mastercard
...
 ↓
Find Decision Makers
 ↓
Generate Personalized Emails
 ↓
Send via Brevo
```

---

## Output

Generated lead data is stored as JSON files.

Example:

```json
{
  "source_company": {
    "name": "Stripe",
    "domain": "stripe.com"
  },
  "similar_company_leads": [
    {
      "company": {
        "name": "PayPal"
      },
      "contacts": [
        {
          "first_name": "John",
          "last_name": "Doe",
          "position": "Director",
          "email": "john@paypal.com"
        }
      ]
    }
  ]
}
```

---

## Design Decisions

### Why Apollo?

Apollo provides enriched company metadata including:

* Industries
* Keywords
* Employee counts
* Company profiles

This information is used to identify similar companies.

### Why Hunter?

Hunter provides reliable domain-based contact discovery and work email identification.

### Why Brevo?

Brevo offers a simple and developer-friendly email API for automated outreach.

### Similarity Scoring

Companies are ranked using:

1. Industry overlap
2. Keyword overlap
3. Employee count similarity

This approach is domain-agnostic and avoids hardcoded industry-specific rules.

---

## Error Handling

The application includes:

* API error handling
* Logging
* Missing data protection
* Test mode safeguards
* User confirmation before email sending

---

## Future Improvements

* Pagination support for larger company datasets
* Retry mechanisms for API failures
* Contact scoring and ranking
* Advanced similarity algorithms
* Unit and integration tests

---

## Author

Jeshik S
