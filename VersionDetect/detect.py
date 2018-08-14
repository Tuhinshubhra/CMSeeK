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
    elif id == 'quick':
        import VersionDetect.quick as quickverdetect
        quickver = quickverdetect.start(ga_content)
        return quickver
    elif id == 'pwind':
        import VersionDetect.pwind as pwindverdetect
        pwindver = pwindverdetect.start(ga_content)
        return pwindver
    elif id == 'ophal':
        import VersionDetect.ophal as ophalverdetect
        ophalver = ophalverdetect.start(ga_content, url, ua)
        return ophalver
    elif id == 'sfy':
        import VersionDetect.sfy as sfyverdetect
        sfyver = sfyverdetect.start(ga_content)
        return sfyver
    elif id == 'otwsm':
        import VersionDetect.otwsm as otwsmverdetect
        otwsmver = otwsmverdetect.start(source)
        return otwsmver
    elif id == 'ocms':
        import VersionDetect.ocms as ocmsverdetect
        ocmsver = ocmsverdetect.start(url, ua)
        return ocmsver
    elif id == 'share':
        import VersionDetect.share as shareverdetect
        sharever = shareverdetect.start(url, ua)
        return sharever
    elif id == 'mura':
        import VersionDetect.mura as muraverdetect
        muraver = muraverdetect.start(ga_content)
        return muraver
    elif id == 'kbcms':
        import VersionDetect.kbcms as kbcmsverdetect
        kbcmsver = kbcmsverdetect.start(url, ua)
        return kbcmsver
    elif id == 'koken':
        import VersionDetect.koken as kokenverdetect
        kokenver = kokenverdetect.start(ga_content)
        return kokenver
    elif id == 'impage':
        import VersionDetect.impage as impageverdetect
        impagever = impageverdetect.start(ga_content)
        return impagever
    elif id == 'flex':
        import VersionDetect.flex as flexverdetect
        flexver = flexverdetect.start(source, url, ua)
        return flexver
