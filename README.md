findproxy.py -themofo 
Proxy Scanner for use with proyxychains.
Overview

This project provides a simple vibe coded Python script (findproxy.py) to fetch free proxies using the proxyscrape library. The proxies are saved in the correct format for proxychains.

Prerequisites





Python 3.6 or higher



pip package manager



A working internet connection to fetch proxies

Installation





Clone or download this repository to your local machine.



Create and activate a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows



Install the required dependencies:

pip install -r requirements.txt

Usage





Ensure the dependencies are installed.



Run the script to fetch proxies:

python findproxy.py



The script will retrieve a list of proxies (e.g., HTTP, HTTPS) and can be modified to filter proxies by country, anonymity, or type.




Example

To fetch HTTP proxies from the USA and print them:

from proxyscrape import create_collector

collector = create_collector('my-collector', 'http')
proxy = collector.get_proxy({'code': 'us'})
print(proxy)

Notes





Free proxies from proxyscrape may be unreliable or slow. Consider premium proxies for critical tasks.



Always obtain permission before scanning networks to comply with legal and ethical guidelines.




Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes. -purptea

License

This project is licensed under the MIT License.
