from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import datetime

class YahooFantasyStats:

    now = datetime.datetime.now()
    prev_year= now.year - 1

    def __init__(self, lg_name):
        self.lg_name = lg_name
        self.lg = None
        self.prev_week= None
        self.all_matchup_stats = {}

        sc = OAuth2(None, None, from_file='brandon_permissions.json')
        gm = yfa.Game(sc, 'nba')
        all_curr_lgs= gm.league_ids(year= self.prev_year)
        #print (f"\nYahoo Fantasy Basketball League IDs ({self.prev_year} - {self.now.year}): {all_curr_lgs}")
        
        lg_dict = {}
        lg_name_check = 0

        for lg_id in all_curr_lgs:
            lg = gm.to_league(lg_id)
            _lg_name = lg.matchups().get("fantasy_content").get("league")[0].get("name")
            # Check lg_name class argument to see if it is an existing league in the Yahoo Game object
            if lg_name.upper() == _lg_name.upper():
                lg_name_check = 1
                self.lg_name = _lg_name
            lg_dict[_lg_name] = lg_id
            #print(f"{lg_id}: {_lg_name}")

        if lg_name_check != 1:
            raise NameError(f"{self.lg_name} is not a valid league name.")

        _lg_id= lg_dict[self.lg_name]
        #print(f"_lg_id: {_lg_id}")
        self.lg = gm.to_league(_lg_id)
        curr_week= self.lg.current_week()
        
        # TODO: add argument for week #
        #self.prev_week= 1
        self.prev_week= curr_week - 1

        self.scoreboard= self.lg.matchups(self.prev_week).get("fantasy_content").get("league")[1].get("scoreboard")
        self.all_matchups= self.scoreboard.get("0").get("matchups")

    def matchup_week(self):
        return self.scoreboard.get("week")

    def prev_date_range(self):
        return self.lg.week_date_range(self.prev_week)

    # All matchup stats stored in a dictionary with the following format:
    # {team_num: {"name":example_name, "stats":{"FGM/A":"179/406", "FG": 0.441, ... }}}
    def matchup_stats(self):
        matchup_num= 0

        #TODO: Make dynamic by setting range to # team in league
        for team_num in range (0, 12, 2):  
            t0_name =  self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("0").get("team")[0][2].get("name")

            t0_fgm_a = self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("0").get("team")[1].get("team_stats").get("stats")[0].get("stat").get("value")
            t0_fg_pct = float(self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("0").get("team")[1].get("team_stats").get("stats")[1].get("stat").get("value"))
            t0_ftm_a = self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("0").get("team")[1].get("team_stats").get("stats")[2].get("stat").get("value")
            t0_ft_pct = float(self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("0").get("team")[1].get("team_stats").get("stats")[3].get("stat").get("value"))
            t0_3ptm = int(self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("0").get("team")[1].get("team_stats").get("stats")[4].get("stat").get("value"))
            t0_pts = int(self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("0").get("team")[1].get("team_stats").get("stats")[5].get("stat").get("value"))
            t0_reb = int(self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("0").get("team")[1].get("team_stats").get("stats")[6].get("stat").get("value"))
            t0_ast = int(self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("0").get("team")[1].get("team_stats").get("stats")[7].get("stat").get("value"))
            t0_stl = int(self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("0").get("team")[1].get("team_stats").get("stats")[8].get("stat").get("value"))
            t0_blk = int(self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("0").get("team")[1].get("team_stats").get("stats")[9].get("stat").get("value"))
            t0_ast_to = float(self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("0").get("team")[1].get("team_stats").get("stats")[10].get("stat").get("value"))

            t1_name = self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("1").get("team")[0][2].get("name")

            t1_fgm_a = self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("1").get("team")[1].get("team_stats").get("stats")[0].get("stat").get("value")
            t1_fg_pct = float(self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("1").get("team")[1].get("team_stats").get("stats")[1].get("stat").get("value"))
            t1_ftm_a = self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("1").get("team")[1].get("team_stats").get("stats")[2].get("stat").get("value")
            t1_ft_pct = float(self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("1").get("team")[1].get("team_stats").get("stats")[3].get("stat").get("value"))
            t1_3ptm = int(self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("1").get("team")[1].get("team_stats").get("stats")[4].get("stat").get("value"))
            t1_pts = int(self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("1").get("team")[1].get("team_stats").get("stats")[5].get("stat").get("value"))
            t1_reb = int(self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("1").get("team")[1].get("team_stats").get("stats")[6].get("stat").get("value"))
            t1_ast = int(self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("1").get("team")[1].get("team_stats").get("stats")[7].get("stat").get("value"))
            t1_stl = int(self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("1").get("team")[1].get("team_stats").get("stats")[8].get("stat").get("value"))
            t1_blk = int(self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("1").get("team")[1].get("team_stats").get("stats")[9].get("stat").get("value"))
            t1_ast_to = float(self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("1").get("team")[1].get("team_stats").get("stats")[10].get("stat").get("value"))

            #self.all_matchup_stats[team_num] = {"name": self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("0").get("team")[0][2].get("name"), "stats": self.all_matchups.get("0").get("matchup").get("0").get("teams").get("0").get("team")[1].get("team_stats").get("stats")}
            #self.all_matchup_stats[team_num + 1] = {"name": self.all_matchups.get(str(matchup_num)).get("matchup").get("0").get("teams").get("1").get("team")[0][2].get("name"), "stats": self.all_matchups.get("0").get("matchup").get("0").get("teams").get("1").get("team")[1].get("team_stats").get("stats")}
            self.all_matchup_stats[team_num] = {"name": t0_name, "stats": {"FGM/A":t0_fgm_a, "FG%":t0_fg_pct, "FTM/A":t0_ftm_a, "FT%":t0_ft_pct, "3PTM":t0_3ptm, "PTS":t0_pts, "REB":t0_reb, "AST":t0_ast, "STL":t0_stl, "BLK":t0_blk, "A/T":t0_ast_to}}
            self.all_matchup_stats[team_num + 1] = {"name": t1_name, "stats": {"FGM/A":t1_fgm_a, "FG%":t1_fg_pct, "FTM/A":t1_ftm_a, "FT%":t1_ft_pct, "3PTM":t1_3ptm, "PTS":t1_pts, "REB":t1_reb, "AST":t1_ast, "STL":t1_stl, "BLK":t1_blk, "A/T":t1_ast_to}}
            matchup_num += 1
            # TODO make dictionary within dictionary: {'team1': {'fg':x, 'to':y, 'ast':z}, ...} OR (better idea) compare team matchup and then put stats of best team in dictionary within dictionary
           
        return self.all_matchup_stats
