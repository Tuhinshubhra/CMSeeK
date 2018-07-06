def start(id, url, ua, ga, source):
    if id == "wp":
        # trust me more will be added soon
        import VersionDetect.wp as wpverdetect
        wpver = wpverdetect.start(id, url, ua, ga, source):
        return wpver
