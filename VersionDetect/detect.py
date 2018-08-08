#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 Tuhinshubhra

def start(id, url, ua, ga, source, ga_content):
    if id == "wp":
        # trust me more will be added soon
        import VersionDetect.wp as wpverdetect
        wpver = wpverdetect.start(id, url, ua, ga, source)
        return wpver
    elif id == 'joom':
        import VersionDetect.joom as joomverdetect
        joomver = joomverdetect.start(id, url, ua, ga, source)
        return joomver
    elif id == 'dru':
        import VersionDetect.dru as druverdetect
        druver = druverdetect.start(id, url, ua, ga, source)
        return druver
    elif id == 'xe':
        import VersionDetect.xe as xeverdetect
        xever = xeverdetect.start(ga_content)
        return xever
    elif id == 'wgui':
        import VersionDetect.wgui as wguiverdetect
        wguiver = wguiverdetect.start(ga_content)
        return wguiver
    elif id == 'umi':
        import VersionDetect.umi as umiverdetect
        umiver = umiverdetect.start(url, ua)
        return umiver
    elif id == 'tidw':
        import VersionDetect.tidw as tidwverdetect
        tidwver = tidwverdetect.start(source)
        return tidwver
    elif id == 'sulu':
        import VersionDetect.sulu as suluverdetect
        suluver = suluverdetect.start(url, ua)
        return suluver
    elif id == 'subcms':
        import VersionDetect.subcms as subcmsverdetect
        subcmsver = subcmsverdetect.start(ga_content)
        return subcmsver
    elif id == 'snews':
        import VersionDetect.snews as snewsverdetect
        snewsver = snewsverdetect.start(ga_content, source)
        return snewsver
    elif id == 'spity':
        import VersionDetect.spity as spityverdetect
        spityver = spityverdetect.start(ga_content)
        return spityver
    elif id == 'slcms':
        import VersionDetect.slcms as slcmsverdetect
        slcmsver = slcmsverdetect.start(source)
        return slcmsver
    elif id == 'rock':
        import VersionDetect.rock as rockverdetect
        rockver = rockverdetect.start(ga_content)
        return rockver
    elif id == 'roadz':
        import VersionDetect.roadz as roadzverdetect
        roadzver = roadzverdetect.start(ga_content)
        return roadzver
    elif id == 'rite':
        import VersionDetect.rite as riteverdetect
        ritever = riteverdetect.start(ga_content)
        return ritever
