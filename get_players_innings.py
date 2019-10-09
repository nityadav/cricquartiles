from bs4 import BeautifulSoup
import urllib.request
import json

invalid_scores = ['DNB', 'TDNB', 'sub', 'absent']


def get_player_innings(player_url):
    with urllib.request.urlopen(player_url) as f:
        html_content = f.read()
        html_soup = BeautifulSoup(html_content, 'html.parser')
        inning_rows = html_soup.find_all('tr', attrs={'class':'data1'})
        return inning_rows[1:] # first item is overall


def get_player_batting_scores(player_url):
    def _validate(score: str):
        return not (score.strip() in invalid_scores)

    innings = get_player_innings(player_url)
    inning_scores = [i.find_all('td')[0].get_text() for i in innings]
    scores = [s for s in inning_scores if _validate(s)]
    return scores


def get_player_url(player_id: str):
    return 'http://stats.espncricinfo.com/ci/engine/player/{}.html' \
           '?class=1;template=results;type=batting;view=innings'.format(player_id)


if __name__ == '__main__':
    with open('player_ids.json') as ids_f, open('test_innings.json','w') as innings_f:
        player_info = json.load(ids_f)
        for p in player_info:
            p.update({'test_innings': get_player_batting_scores(get_player_url(p['id']))})
        json.dump(player_info, innings_f)
