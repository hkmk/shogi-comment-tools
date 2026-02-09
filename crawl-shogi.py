# -*- coding: utf-8 -*-

'''
名人戦棋譜速報の棋譜を取得する．
'''

import requests
import time
import re
import tqdm
import os
import browser_cookie3

def get_with_sleep(url, cookies=None, sleep_time=2):

    response = requests.get(
        url,
        cookies=cookies,
    )

    time.sleep(sleep_time)
    return response

def get_game_list(cookies):

    games = []

    rank_list = ['M7', 'A1', 'B1', 'B2', 'C1', 'C2']
    calendar_url = 'http://member.meijinsen.jp/pay/game_list/meijinsen/{year}/{rank}/calendar.html'

    def get_games(text):

        games = re.findall(r"open_kif\('[^\)]*/[0-9]+.html'\)", text)
        games = [f'{gid[10:-7]}.txt' for gid in games]
        return games
    
    for rank in rank_list:

        response = get_with_sleep(calendar_url.format(year='latest', rank=rank), cookies)
        if response.status_code != 200:
            print('{}: {}'.format(latest_A1_calendar_url, response.status_code))
            break

        games.extend(get_games(response.text))
        calendars = re.findall(fr'../../[0-9]+/{rank}/calendar.html"', response.text)
        calendars = [int(calendar.split('/')[-3]) for calendar in calendars]

        for year in calendars:
            response = get_with_sleep(calendar_url.format(year=year, rank=rank), cookies)
            if response.status_code != 200:
                print('{}: {}'.format(calendar_url.format(year=year, rank=rank), response.status_code))
                break
            
            games.extend(get_games(response.text))
            break
        break

    return games

def get_game_record(cookies, game_record_url):

    response = get_with_sleep(game_record_url, cookies)
    if response.status_code != 200:
        print('{}: {}'.format(game_record_url, response.status_code))
        return None

    return response.text

def get_cookies(browser):

    if browser == 'chrome':
        return browser_cookie3.chrome()
    if browser == 'firefox':
        return browser_cookie3.firefox()
    if browser == 'safari':
        return browser_cookie3.safari()

    raise NotImplementedError()

if __name__=='__main__':

    import argparse

    parser = argparse.ArgumentParser('SGF game record crawler from meijinsen.com')
    parser.add_argument('--browser', choices=['chrome', 'firefox', 'safari'], default='chrome')
    parser.add_argument('--output_dir', default='./kifu')

    args = parser.parse_args()

    cookies = get_cookies(args.browser)

    game_list = get_game_list(cookies)
    print(f'Number of game records: {len(game_list)}')

    for game in tqdm.tqdm(game_list, ncols=0):

        game_record_url = f'http://member.meijinsen.jp{game}'
        ary = game.split('/')
        game = f'{ary[-5]}/{ary[-2]}/{ary[-1]}'
        save_path = f'{args.output_dir}/{game}'
        response = get_game_record(cookies, game_record_url)

        if response is None:
            continue

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(response)
