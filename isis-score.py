#!/usr/bin/env python

import pyperclip

def isRatingPage(page):
    return page and (page[:15] == '<!DOCTYPE html>') and ('<title>Bewertungen: Zugriff</title>' in page)

def getRatingz(page):
    namez, mailz, catz, scorezz = [], [], [], []
    pos = page.find('<tbody>')              # goto table begin
    pos = page.find('<tr class="heading r1">', pos + 1)       # goto header row
    row = page[pos : page.find('</tr>', pos + 1)]
    # now working in header row
    rowpos = 0
    while True:
        # CATZ
        rowpos = row.find('<th class="item catlevel1', rowpos + 1)  # goto row begin
        if rowpos == -1:
            break
        rowpos = row.find('<a', rowpos + 1)  # goto
        rowpos = row.find('<img', rowpos + 1)  # goto
        rowpos = row.find('>', rowpos + 1)  # goto
        catz.append(row[rowpos + 1 : row.find('</a>', rowpos)])
    while True:
        # NAME
        pos = page.find('<th class="user cell', pos + 1)  # goto row begin
        if pos == -1:                       # no rows left
            break
        row = page[pos : page.find('</tr>', pos + 1)]
        # now working in student row
        rowpos = row.find('</a>')           # skip link
        rowpos = row.find('>', rowpos + 4)  # goto username begin
        namez.append(row[rowpos + 1 : row.find('</a>', rowpos)])
        # MAIL
        rowpos = row.find('<th class="header userfield useremail', rowpos + 1)  # goto mail cell
        rowpos = row.find('>', rowpos + 1)  # goto mail begin
        mailz.append(row[rowpos + 1 : row.find('</th>', rowpos)])
        # SCOREZ
        scorez = []
        while True:
            rowpos = row.find('<td class="grade', rowpos + 1)   # goto grade cell
            if rowpos == -1:
                break
            rowpos = row.find('<span', rowpos + 1)              # goto grade cell
            rowpos = row.find('>', rowpos + 1)          # goto grade entry
            score = row[rowpos + 1 : row.find('</span>', rowpos + 1)]
            scorez.append(score)
        scorezz.append(scorez)
    return namez, mailz, catz, scorezz

def countScorez(catz, scorez, ccond, scond):
    '''returns a tuple of:
        - count of scorez which meet scond and whose category meets ccond
        - count of scorez whose category meets ccond.
       ungraded slots are not counted.'''
    s, c = 0, 0
    for i in range(len(catz)):
        if scorez[i] == '-':
            continue
        if ccond(catz[i]):
            c += 1
            if scond(scorez[i]):
                s += 1
    return s, c

def showRatingz(namez, mailz, catz, scorezz):
    print '\t\t\t\t(blatt 02)\thomework\tmilestonez'
    # homework 1 categroy condition:
    chw1 = lambda c : 'Aufgabenblatt 02' in c
    # other homework categroy condition:
    chw2 = lambda c : 'Aufgabenblatt' in c and not 'Aufgabenblatt 02' in c
    # milestone categroy condition:
    cms = lambda c : 'Meilenstein' in c
    # pass condition:
    cpass = lambda s : not 'nicht' in s
    for i in range(len(namez)):
        hw1_pass, hw1_total = countScorez(catz, scorezz[i], chw1, cpass)
        hw2_pass, hw2_total = countScorez(catz, scorezz[i], chw2, cpass)
        ms_pass, ms_total   = countScorez(catz, scorezz[i],  cms, cpass)
        print "%s\t%d/%d\t\t%d/%d\t\t%d/%d" % (
                '{:<30}'.format(namez[i]),  # name
                hw1_pass, hw1_total,        # homework 1
                hw2_pass, hw2_total,        # homework 2-
                ms_pass, ms_total
            )

print 'Processing cliboard content...',
pastage = pyperclip.paste()
print 'aquired.'
if not isRatingPage(pastage):
    print 'This is not an ISIS rating page!'
    exit(1)
print ''
namez, mailz, catz, scorezz = getRatingz(pastage)
showRatingz(namez, mailz, catz, scorezz)
