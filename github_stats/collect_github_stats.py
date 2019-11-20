import requests
import json
import sys
import pandas as pd
import argparse
import random


def parse_args():
    parser = argparse.ArgumentParser(description="Github PR comments parser")
    parser.add_argument('--num_results',
                        '-n',
                        dest='n_results',
                        default=50,
                        type=int,
                        help="The number of random repositories to scrape.")

    parser.add_argument('--popular-repos',
                        '-r',
                        dest='popular_path',
                        default='repos.txt',
                        help='The path of the file containing information about popular repositories.')

    parser.add_argument('--other-repos',
                        dest='other_path',
                        help='Path to a text file containing the numeric IDs of other repos.')

    parser.add_argument('--others_out',
                        dest='others_out',
                        default='others_out.txt',
                        help='Path to the output file for numeric IDs of other repos.')

    parser.add_argument('--out',
                        '-o',
                        dest='out',
                        default='out.csv',
                        help='Path to the output csv files.  Will be affixed with _pop and _other.')

    return parser.parse_args()


def collect_stats(session, input, params):
    data = []
    for repo in input:
        url = f'https://api.github.com/repos/{repo}'
        print(url)
        text = json.loads(session.get(url).text)
        try:
            data.append(get_params(text,params))
        except ValueError:
            pass

    metadata_df = pd.DataFrame(columns=params, data=data)
    return(metadata_df)

def get_params(text, params):
    try:
        if text['message'] == 'Not Found':
            print("Bad repo!")
            raise ValueError
    except KeyError:
        pass
    data = []
    for i in params:
        try:
            data.append(text[i])
        except KeyError:
            data.append(None)
    return data


def collect_random_stats(session, n_samples, params):
    data = []
    n_success = 0
    while n_success < n_samples:
        repo_id = random.randint(0, 12000000)
        url = f'https://api.github.com/repositories/{repo_id}'
        print(url)
        text = json.loads(session.get(url).text)
        try:
            data.append(get_params(text,params))
            n_success += 1
        except:
            pass

    metadata_df = pd.DataFrame(columns=params, data=data)
    return(metadata_df)

def main(n_results, popular_path, other_path, others_out, out):
    # Show github repository (user view)
    username = 'AustinSanders'
    token = '51e1a4cbe9213d1277c262cb48c7ee8a8938b463'
    session = requests.Session()
    session.auth = (username, token)

    with open('params.txt', 'r') as f:
        # Take one off the end because the my IDE forces a newline at the end of files.
        #  Without removing this, it creates a blank parameter.
        params = f.read().split('\n')[:-1]


    with open(popular_path, 'r') as f:
        popular = f.read().split('\n')
    # Collect statistics for the popular repositories

    #popular_stats = collect_stats(session, popular, params)
    #popular_stats.to_csv(out.replace('.csv','_popular.csv'))

    # Collect statistics for 'other' repositories
    other_stats = collect_random_stats(session, n_results, params)
    other_stats.to_csv(out.replace('.csv','_other.csv'))


if __name__ == "__main__":
    args = parse_args()
    sys.exit(main(**vars(args)))
