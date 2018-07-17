def start(id, url, ua, ga, source):
    if id == "wp":
        # trust me more will be added soon
        import VersionDetect.wp as wpverdetect
        wpver = wpverdetect.start(id, url, ua, ga, source)
        return wpver
    elif id == 'joom':
        import VersionDetect.joom as joomverdetect
        joomver = joomverdetect.start(id, url, ua, ga, source)
        return joomver
