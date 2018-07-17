def start(id, url, ua, ga, source):
    if id == "wp":
        # for now this is the only cms... but not for long!
        import deepscans.wp.init as wpscan
        wpscan.start(id, url, ua, ga, source)
    if id == 'joom':
        # told ya... not for long
        import deepscans.joom.init as joomscan
        joomscan.start(id, url, ua, ga, source)
