def start(id, url, ua, ga, source):
    if id == "wp":
        # trust me more will be added soon
        import VersionDetect.wp as wpverdetect
        wpver = wpverdetect.start(id, url, ua, ga, source):
        return wpver
    elif id == 'mg':
        import VersionDetect.mg as mgverdetect
        mgver = mgverdetect.start(url, ua)
        return mgver
