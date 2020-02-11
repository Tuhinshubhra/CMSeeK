#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

def start(id, url, ua, ga, source, ga_content, headers):
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
    elif id == 'dncms':
        import VersionDetect.dncms as dncmsverdetect
        dncmsver = dncmsverdetect.start(url, ua)
        return dncmsver
    elif id == 'cntsis':
        import VersionDetect.cntsis as cntsisverdetect
        cntsisver = cntsisverdetect.start(ga_content)
        return cntsisver
    elif id == 'cnido':
        import VersionDetect.cnido as cnidoverdetect
        cnidover = cnidoverdetect.start(ga_content)
        return cnidover
    elif id == 'con5':
        import VersionDetect.con5 as con5verdetect
        con5ver = con5verdetect.start(ga_content)
        return con5ver
    elif id == 'csim':
        import VersionDetect.csim as csimverdetect
        csimver = csimverdetect.start(ga_content)
        return csimver
    elif id == 'brcms':
        import VersionDetect.brcms as brcmsverdetect
        brcmsver = brcmsverdetect.start(ga_content)
        return brcmsver
    elif id == 'bboard':
        import VersionDetect.bboard as bboardverdetect
        bboardver = bboardverdetect.start(source)
        return bboardver
    elif id == 'dscrs':
        import VersionDetect.dscrs as dscrsverdetect
        dscrsver = dscrsverdetect.start(ga_content)
        return dscrsver
    elif id == 'discuz':
        import VersionDetect.discuz as discuzverdetect
        discuzver = discuzverdetect.start(ga_content)
        return discuzver
    elif id == 'minibb':
        import VersionDetect.minibb as minibbverdetect
        minibbver = minibbverdetect.start(source)
        return minibbver
    elif id == 'mybb':
        import VersionDetect.mybb as mybbverdetect
        mybbver = mybbverdetect.start(source)
        return mybbver
    elif id == 'nodebb':
        import VersionDetect.nodebb as nodebbverdetect
        nodebbver = nodebbverdetect.start(source)
        return nodebbver
    elif id == 'punbb':
        import VersionDetect.punbb as punbbverdetect
        punbbver = punbbverdetect.start(source)
        return punbbver
    elif id == 'smf':
        import VersionDetect.smf as smfverdetect
        smfver = smfverdetect.start(source)
        return smfver
    elif id == 'vanilla':
        import VersionDetect.vanilla as vanillaverdetect
        vanillaver = vanillaverdetect.start(url, ua)
        return vanillaver
    elif id == 'uknva':
        import VersionDetect.uknva as uknvaverdetect
        uknvaver = uknvaverdetect.start(ga_content)
        return uknvaver
    elif id == 'xmb':
        import VersionDetect.xmb as xmbverdetect
        xmbver = xmbverdetect.start(source)
        return xmbver
    elif id == 'yabb':
        import VersionDetect.yabb as yabbverdetect
        yabbver = yabbverdetect.start(source)
        return yabbver
    elif id == 'aef':
        import VersionDetect.aef as aefverdetect
        aefver = aefverdetect.start(source)
        return aefver
    elif id == 'bhf':
        import VersionDetect.bhf as bhfverdetect
        bhfver = bhfverdetect.start(ga_content)
        return bhfver
    elif id == 'fudf':
        import VersionDetect.fudf as fudfverdetect
        fudfver = fudfverdetect.start(source)
        return fudfver
    elif id == 'yaf':
        import VersionDetect.yaf as yafverdetect
        yafver = yafverdetect.start(source)
        return yafver
    elif id == 'ubbt':
        import VersionDetect.ubbt as ubbtverdetect
        ubbtver = ubbtverdetect.start(source, ga_content)
        return ubbtver
    elif id == 'myupb':
        import VersionDetect.myupb as myupbverdetect
        myupbver = myupbverdetect.start(source)
        return myupbver
    elif id == 'mvnf':
        import VersionDetect.mvnf as mvnfverdetect
        mvnfver = mvnfverdetect.start(source)
        return mvnfver
    elif id == 'mcb':
        import VersionDetect.mcb as mcbverdetect
        mcbver = mcbverdetect.start(source)
        return mcbver
    elif id == 'aspf':
        import VersionDetect.aspf as aspfverdetect
        aspfver = aspfverdetect.start(source)
        return aspfver
    elif id == 'jf':
        import VersionDetect.jf as jfverdetect
        jfver = jfverdetect.start(source)
        return jfver
    elif id == 'mg':
        import VersionDetect.mg as mgverdetect
        mgver = mgverdetect.start(url, ua)
        return mgver
    elif id == 'coms':
        import VersionDetect.coms as comsverdetect
        comsver = comsverdetect.start(url, ua)
        return comsver
    elif id == 'abda':
        import VersionDetect.abda as abdaverdetect
        abdaver = abdaverdetect.start(source)
        return abdaver
    elif id == 'dweb':
        import VersionDetect.dweb as dwebverdetect
        dwebver = dwebverdetect.start(ga_content)
        return dwebver
    elif id == 'qcart':
        import VersionDetect.qcart as qcartverdetect
        qcartver = qcartverdetect.start(ga_content)
        return qcartver
    elif id == 'rbsc':
        import VersionDetect.rbsc as rbscverdetect
        rbscver = rbscverdetect.start(ga_content)
        return rbscver
    elif id == 'oracle_atg':
        import VersionDetect.atg as atgverdetect
        atgver = atgverdetect.start(headers)
        return atgver
    elif id == 'umbraco':
        import VersionDetect.umbraco as umbracoverdetect
        umbracover = umbracoverdetect.start(headers, url, ua)
        return umbracover
    elif id == 'shopfa':
        import VersionDetect.shopfa as shopfaverdetect
        shopfaver = shopfaverdetect.start(ga_content, headers)
        return shopfaver
    elif id == 'amiro':
        import VersionDetect.amiro as amiroverdetect
        amirover = amiroverdetect.start(source)
        return amirover
    elif id == 'godaddywb':
        import VersionDetect.godaddywb as godaddywbverdetect
        godaddywb_version = godaddywbverdetect.start(ga_content)
        return godaddywb_version
