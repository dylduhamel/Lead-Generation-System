# Acuritas Property Leads Generation Tool

## Overview

This is a proprietary tool developed for Acuritas Consulting by Dylan Duhamel. The tool is designed to automate the process of finding and processing property leads by scraping multiple public web sources using Selenium. It gathers information, enriches the data by skiptracing, and then saves all pertinent details to a database for further use by the Acuritas team.

**NOTE: This tool is only intended for use by Acuritas employees. Unauthorized use is strictly prohibited.**

## Features

- Automates the process of property lead generation.
- Scrapes multiple web sources for property information.
- Enhances the data by skiptracing to fill in missing details.
- Removes duplicate entries to maintain a clean database.
- Exports enriched data to a JSON file.
- Sends notifications via the Twilio API for SMS/Email messaging.
- Tracks and displays the execution time of the main function for performance monitoring.

## Installation

To get started with this tool, you need to install the required Python packages. Navigate to the project directory in your terminal and run the following command:

```sh
pip3 install -r requirements.txt
```

This command reads the `requirements.txt` file and installs all the dependencies listed in it.

## Usage

After installing the necessary packages, you can run the program using your preferred Python IDE or from the terminal by navigating to the project directory and running `python main.py`.

## Contributions

This project is proprietary and developed specifically for Acuritas. Therefore, we are not accepting any external contributions at this time. 

## Support

For any issues, questions, or comments, please contact the Acuritas team [team@acuritasconsulting.com].

## License

This tool is proprietary software owned by Acuritas. Unauthorized use, modification, or distribution of this software is strictly prohibited.
