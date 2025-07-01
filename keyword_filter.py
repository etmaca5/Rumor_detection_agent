BASE_KEYWORDS = [
    "rob the election", "rejected ballot", "steal the election", "cheat",
    "fraud", "rigged", "tamper", "faulty", "manipulate", "mislead", "rig",
    "outdated voter rolls", "uncleaned voter rolls", "inaccurate voter list", "voter list purge",
    "voter purge", "voter rolls", "voter roll", "invalid voter", "voter cleanup", "dirty rolls",
    "mail-in", "mail in", "ballot box", "ballot theft", "drop box", "absentee", "dropbox",
    "site unavailable", "polling crash", 
    "write-in issue", "write in issue", "FWAB abuse", "system hacked",
    "tampered drop box", "drop box theft", "drop box destroyed", "drop box security", "tampered ballot box",
    "voting software hacked", "manipulated voting system", "unreviewed voting software", "voting software",
    "software manipulation", "hacked voting machine", "voting machines don't work",
    "dead voter", "deceased vote", "fake voter",
    "dead people voting", "votes cast for deceased", "deceased voter", "dead voter ballots",
    "voter data breach", "registration data hacked", "voter database hacked", "leaked voter registration",
    "voter registration leak", "voter info breach",
    "vote breach", "vote privacy", "vote reveal", 
    "voter registration site down", "registration website outage", "voter site compromise", "registration system failure",
    "election IT breach", "state IT compromise", "local IT hacked", "compromised election tech", "IT system hacked",
    "fake voter info", "manipulated voter data", "tampered voter records", "altered registration data",
    "printed fake ballots", "stuffed ballot", "duplicate mail-in ballots", "ballot scheme", "counterfeit ballots",
    "FWAB", "Federal Write-In ballot", "Federal Write-In ballot", "FWAB scheme", "absentee ballot loophole",
    "ballot scanner error", "ballot not counted scanner", "scanner issue ballot", "scanner malfunction",
    "Sharpie ballot issue", "ballot rejected Sharpie", "voting pen issue", "Sharpie voting problem", "pen ballot rejection",
    "intimidating observers", "poll observer interference", "poll observer campaigning", "poll watcher intimidation",
    "poll station interference", "intimidating poll watcher",
    "observer intimidation", "intimidate voters", "cheating election", "election cheat", "fake vote",
    "knows who I voted for", "revealed my vote", "vote disclosure", "vote privacy breach", "vote confidentiality issue",
    "poll lookup site down", "voter lookup outage", "polling place site crash", "election lookup failure", "polling site unavailable"
]


class KeywordFilter:
    def __init__(self, additional_keywords=None, overwrite_keywords=False):
        self.keywords = BASE_KEYWORDS
        if overwrite_keywords: 
            assert additional_keywords
            self.keywords = additional_keywords
        elif additional_keywords:
            for kw in additional_keywords:
                self.keywords.append(kw)

    

    def run_filter(self, post: str) -> bool:
        """Check if post contains any keywords"""
        post_lower = post.lower()
        for kw in self.keywords:
            if kw.lower() in post_lower:
                return True
        return False