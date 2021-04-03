from yahoo_fantasy_stats import YahooFantasyStats
import re
import os

# Compare matchup_stats to top_stats
def compare_stat(stat_name, top_stats, matchup_stats, team_id):
    updated_top_stats = top_stats

    # If matchup stats value is greather than current top stat value, replace the top stat value with the matchup stats value
    if matchup_stats.get(team_id).get("stats").get(stat_name) > top_stats.get(stat_name).get("value"):
        top_stat_value = matchup_stats.get(team_id).get("stats").get(stat_name)
        updated_top_stats[stat_name] = {"team_id": team_id, "value": top_stat_value}
        return updated_top_stats

    else:
        # top_stats will already have the highest value up to the current iteration - return it back so that top stats isn't set to None
        return updated_top_stats

# Read MVP standings from previous week's report and add to the values for current week. 
# Read team ID instead of name in case taem name changed in current week.
def update_mvp_standings(top_stats):
    last_wk_mvp = {}
    last_wk_report_path= (f'{os.getcwd()}\\all_reports\yfb_week_{int(matchup_week)-1}_report.txt')

    try:
        with open (last_wk_report_path, "r") as f: 
            lines = f.readlines()
    
        for line in reversed(lines):
            if '-----------------------' in line:
                break
            match = re.search(r'(.+) \(ID #(\d+)\) - (\d+)', line)

            if match:
                team_name = match.group(1)
                team_id = match.group(2)
                prev_mvp_count= match.group(3)

            last_wk_mvp[team_id] = int(prev_mvp_count)

        for key, value in top_stats.items():
            # If team mvp standing doesn't exist, give it one point. Else, add 1 to current total.    
            if last_wk_mvp.get(value.get('team_id')) == None:
                last_wk_mvp[value.get('team_id')] = 1
            else:
                last_wk_mvp[value.get('team_id')] += 1
        
        last_wk_mvp = dict(sorted(last_wk_mvp.items(), key=lambda x: x[1], reverse=True))
            
        return last_wk_mvp
        
    except FileNotFoundError:
        for key, value in top_stats.items():
            # If team mvp standing doesn't exist, give it one point. Else, add 1 to current total.   
            if last_wk_mvp.get(value.get('team_id')) == None:
                last_wk_mvp[value.get('team_id')] = 1
            else:
                last_wk_mvp[value.get('team_id')] += 1

        last_wk_mvp = dict(sorted(last_wk_mvp.items(), key=lambda x: x[1], reverse=True))

        return last_wk_mvp

if __name__ == "__main__":
    lg_name= "Mississauga Mandems"
    cwd = os.getcwd()
    reports_dir = cwd + '\\all_reports'
    my_class= YahooFantasyStats(lg_name)
    matchup_week= my_class.matchup_week()
    matchup_stats= my_class.matchup_stats()

    # TODO: Read cats from fantasy API
    top_stats = {"FG%": {"team_id":"", "value": 0}, "FT%": {"team_id":"", "value": 0}, "3PTM": {"team_id":"", "value": 0}, "PTS": {"team_id":"", "value": 0}, "REB": {"team_id":"", "value": 0}, "AST": {"team_id":"", "value": 0}, "STL": {"team_id":"", "value": 0}, "BLK": {"team_id":"", "value": 0}, "A/T": {"team_id":"", "value": 0}}
    mvp = {}

    # Iterate through each team's stats in matchup_stats. In each iteration, compare the team's stat values to the current top stat values in top_stats dictionary.
    for team_id, value in matchup_stats.items():
        top_stats = compare_stat("FG%", top_stats, matchup_stats, team_id)
        top_stats = compare_stat("FT%", top_stats, matchup_stats, team_id)
        top_stats = compare_stat("3PTM", top_stats, matchup_stats, team_id)
        top_stats = compare_stat("PTS", top_stats, matchup_stats, team_id)
        top_stats = compare_stat("REB", top_stats, matchup_stats, team_id)
        top_stats = compare_stat("AST", top_stats, matchup_stats, team_id)
        top_stats = compare_stat("STL", top_stats, matchup_stats, team_id)
        top_stats = compare_stat("BLK", top_stats, matchup_stats, team_id)
        top_stats = compare_stat("A/T", top_stats, matchup_stats, team_id)

    # Get MVP standings from previous report and then update it with the current MVP standings
    # TODO: use 'team_id' instead of 'name'
    mvp = update_mvp_standings(top_stats)

    #mvp= dict(sorted(mvp.items(), key=lambda x: x[1], reverse=True))

    report_contents= (
        f'{lg_name}'
        f'\n\nMatchup Week: {matchup_week}'
        f'\nDate Range - {my_class.prev_date_range()[0]} to {my_class.prev_date_range()[1]}'
        f'\n'
        f'\n----------------------------------'
        f'\nTOP STATS OF THE WEEK'
        f'\n----------------------------------'
        # Read team_id from each stat in top_stats and use it to get corresponding team_name from matchup_stats
        f'\nFG% - {matchup_stats.get(top_stats.get("FG%").get("team_id")).get("name")} [{top_stats.get("FG%").get("value")}]'
        f'\nFT% - {matchup_stats.get(top_stats.get("FT%").get("team_id")).get("name")} [{top_stats.get("FT%").get("value")}]'
        f'\n3PTM - {matchup_stats.get(top_stats.get("3PTM").get("team_id")).get("name")} [{top_stats.get("3PTM").get("value")}]'
        f'\nPTS - {matchup_stats.get(top_stats.get("PTS").get("team_id")).get("name")} [{top_stats.get("PTS").get("value")}]'
        f'\nREB - {matchup_stats.get(top_stats.get("REB").get("team_id")).get("name")} [{top_stats.get("REB").get("value")}]'
        f'\nAST - {matchup_stats.get(top_stats.get("AST").get("team_id")).get("name")} [{top_stats.get("AST").get("value")}]'
        f'\nSTL - {matchup_stats.get(top_stats.get("STL").get("team_id")).get("name")} [{top_stats.get("STL").get("value")}]'
        f'\nBLK - {matchup_stats.get(top_stats.get("BLK").get("team_id")).get("name")} [{top_stats.get("BLK").get("value")}]'
        f'\nA/T - {matchup_stats.get(top_stats.get("A/T").get("team_id")).get("name")} [{top_stats.get("A/T").get("value")}]'
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
        # Write current MVP standings  
        for team_id, count in mvp.items():
            f.write(f'\n{matchup_stats.get(team_id).get("name")} (ID #{team_id}) - {count}')    
