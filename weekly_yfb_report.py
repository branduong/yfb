from yahoo_fantasy_stats import YahooFantasyStats
import re
import os

def compare_stat(stat_name, top_stats, matchup_stats, team_num):
    updated_top_stats = top_stats

    if matchup_stats.get(team_num).get("stats").get(stat_name) > top_stats.get(stat_name).get("value"):
        team_name = matchup_stats.get(team_num).get("name")
        top_stat_value = matchup_stats.get(team_num).get("stats").get(stat_name)
        updated_top_stats[stat_name] = {"name": team_name, "value": top_stat_value}
        return updated_top_stats

    else:
        # top_stats will already have the highest value up to the current iteration - return it back so that top stats isn't set to None
        return updated_top_stats

def update_mvp_standings():
    last_wk_mvp = {}

    try:
        with open (f"yfb_week_{int(matchup_week)-1}_report.txt", "r") as f: 
            lines = f.readlines()
    
        for line in reversed(lines):
            if '-----------------------' in line:
                break
            line = line.strip('\n').split(' - ')
            last_wk_mvp[line[0]] = int(line[1])
            
        return last_wk_mvp
    
    except FileNotFoundError:
        return last_wk_mvp

if __name__ == "__main__":
    lg_name= "Mississauga Mandems"
    cwd = os.getcwd()
    reports_dir = cwd + '\\all_reports'
    my_class= YahooFantasyStats(lg_name)
    matchup_week= my_class.matchup_week()
    matchup_stats= my_class.matchup_stats()
    # TODO: Read cats from fantasy API
    top_stats = {"FG%": {"name":"", "value": 0}, "FT%": {"name":"", "value": 0}, "3PTM": {"name":"", "value": 0}, "PTS": {"name":"", "value": 0}, "REB": {"name":"", "value": 0}, "AST": {"name":"", "value": 0}, "STL": {"name":"", "value": 0}, "BLK": {"name":"", "value": 0}, "A/T": {"name":"", "value": 0}}
    mvp = {}

    for team_num, value in matchup_stats.items():
        top_stats = compare_stat("FG%", top_stats, matchup_stats, team_num)
        top_stats = compare_stat("FT%", top_stats, matchup_stats, team_num)
        top_stats = compare_stat("3PTM", top_stats, matchup_stats, team_num)
        top_stats = compare_stat("PTS", top_stats, matchup_stats, team_num)
        top_stats = compare_stat("REB", top_stats, matchup_stats, team_num)
        top_stats = compare_stat("AST", top_stats, matchup_stats, team_num)
        top_stats = compare_stat("STL", top_stats, matchup_stats, team_num)
        top_stats = compare_stat("BLK", top_stats, matchup_stats, team_num)
        top_stats = compare_stat("A/T", top_stats, matchup_stats, team_num)
    
    # Get MVP standings from previous report and then update it with the current MVP standings
    mvp = update_mvp_standings()
    for key, value in top_stats.items():
        # If team mvp standing doesn't exist, give it one point. Else, add 1 to current total.    
        if mvp.get(value.get('name')) == None:
            mvp[value.get('name')] = 1
        else:
            mvp[value.get('name')] += 1

    mvp= dict(sorted(mvp.items(), key=lambda x: x[1], reverse=True))
    report_contents= (
        f'{lg_name}'
        f'\n\nMatchup Week: {matchup_week}'
        f'\nDate Range - {my_class.prev_date_range()[0]} to {my_class.prev_date_range()[1]}'
        f'\n'
        f'\n----------------------------------'
        f'\nTOP STATS OF THE WEEK'
        f'\n----------------------------------'
        f'\nFG% - {top_stats.get("FG%").get("name")} [{top_stats.get("FG%").get("value")}]'
        f'\nFT% - {top_stats.get("FT%").get("name")} [{top_stats.get("FT%").get("value")}]'
        f'\n3PTM - {top_stats.get("3PTM").get("name")} [{top_stats.get("3PTM").get("value")}]'
        f'\nPTS - {top_stats.get("PTS").get("name")} [{top_stats.get("PTS").get("value")}]'
        f'\nREB - {top_stats.get("REB").get("name")} [{top_stats.get("REB").get("value")}]'
        f'\nAST - {top_stats.get("AST").get("name")} [{top_stats.get("AST").get("value")}]'
        f'\nSTL - {top_stats.get("STL").get("name")} [{top_stats.get("STL").get("value")}]'
        f'\nBLK - {top_stats.get("BLK").get("name")} [{top_stats.get("BLK").get("value")}]'
        f'\nA/T - {top_stats.get("A/T").get("name")} [{top_stats.get("A/T").get("value")}]'
        f'\n'
        f'\n-----------------------'
        f'\nMVP STANDINGS'
        f'\n-----------------------'
    )

    print (f"\nWeek {matchup_week} top stat report generated in {reports_dir}")

    if not os.path.isdir(reports_dir):
        os.mkdir(reports_dir)
    with open(f"{reports_dir}\\yfb_week_{matchup_week}_report.txt", "w") as f:
        f.write(report_contents)    
        for team_name, count in mvp.items():
            f.write(f'\n{team_name} - {count}')    
