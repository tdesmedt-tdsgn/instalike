# Instagram Auto Like and Share

This script automatically likes and shares the posts and stories of multiple Instagram users.

## Prerequisites

- Python 3.x
- [instagram_private_api](https://pypi.org/project/instagram-private-api/)
- [Apache Airflow](https://airflow.apache.org/) (optional)

## Installation

1. Clone this repository: git clone https://github.com/YOUR_USERNAME/instagram-auto-like-share.git
2. Install the required Python packages: pip install -r requirements.txt
3. Copy the `.env.example` file to `.env` and fill in your Instagram username and password: cp .env.example .env

## Usage

1. Run the script: python auto_like_share.py
2. The script will like and share the posts and stories of the Instagram users listed in the `target_users` variable.

## Running with Airflow

1. Install Apache Airflow: pip install apache-airflow
2. Initialize the Airflow database: airflow initdb
3. Copy the `dags/instagram_auto_like_share.py.example` file to `dags/instagram_auto_like_share.py`: cp dags/instagram_auto_like_share.py.example dags/instagram_auto_like_share.py
4. Edit the `dags/instagram_auto_like_share.py` file and set the `target_users` list to the Instagram users you want to like and share.
5. Start the Airflow web server: airflow webserver -p 8080
6. Start the Airflow scheduler in a new terminal window: airflow scheduler
7. Open the Airflow web interface at `http://localhost:8080`.
8. Turn on the `instagram_auto_like_share` DAG and let it run according to the schedule you set.

## Contributing

Contributions are welcome! If you have any feature requests, suggestions, or bug reports, please open a GitHub issue or pull request.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.





