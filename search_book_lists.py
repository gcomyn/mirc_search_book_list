import argparse
import os
import sys
import re

searchdir = r'C:\Users\gwydi\Downloads\#Torrents\ebooks\searches'


def read_files():
    fcount = 0
    booklist = []
    searchlist = []
    fbldupstot = 0
    global searchdir 

    print('='*160)
    print('   Using default search director: {}'.format(searchdir))
    choice = input('     Continue using this directory?\n>>> ')
    if choice.upper() != 'Y' and choice.upper() != 'YES':
        searchdir = input('  Enter the search directory\n>>> ')
    for (path, dirs, files) in os.walk(searchdir):
        if path == searchdir:
            if files:
                files = sorted(files)
                searchlist = [ffile for ffile in files if 'sbl_-_' not in ffile]
                searchlist = [ffile for ffile in searchlist if 'getting files from ps2.txt' not in ffile]
                print('='*160)
                print('   Reading {:>5} files:'.format(len(searchlist)))
                print('='*160)
                for ffile in searchlist:
                    fcount +=1
                    filebooklist = []
                    print('{:>3} - {:75}'.format(fcount, ffile), end='')
                    with open(os.path.join(path, ffile),'r', encoding="utf8", errors='ignore') as lfile:
                        blist = lfile.readlines()
                    filebooklist = [bline for bline in blist if bline[0]=='!']
                    # Get the number of books listed in the file, 
                    # then remove the duplicates, and report the number
                    fbldups = len(filebooklist)
                    filebooklist = list(set(filebooklist))
                    fbldups = fbldups - len(filebooklist)
                    print('{:>9,d} books'.format(len(filebooklist)), end='')
                    if fbldups > 0:
                        print(' - {:>9,d} dups removed'.format(fbldups))
                        fbldupstot += fbldups
                    else:
                        print()

                    # Combine the list of books with the main list
                    booklist = [*booklist, *filebooklist]
    print('-'*160)
    print('\nFound {:>15,d} books | Removed {:>15,d} duplicates'.format(len(booklist), fbldupstot))
    return booklist


def searchlists():
    '''This will search the book lists from MIRC 
    for the search term, and sort them by the 
    book name, not the location '''
    booklist = read_files()
    terms = '.'
    while terms.upper() != "STOP" or len(terms)>0:
        terms = input('What do you want to search for?\n >>> ')
        if terms.upper() == "STOP" or len(terms)==0:
            break
        elif terms.upper() == "REREAD":
            booklist = read_files()
        elif terms.upper() == "HELP":
            print('-'*160)
            print('Not written yet!')
            print('-'*160)
        else:
            foundlist = []
            lcount = 0
            bcount = 0
            totbooks = len(booklist)
            for bline in booklist:
                bcount += 1
                bfound = False
                for term in terms.split(', '):
                    if term.upper() in bline.upper():
                        bfound = True
                    else:
                        bfound = False
                        break
                if bfound:
                    header = bline.split(' ')[0]
                    book = bline.replace(header,'').strip().split("::")[0].strip()
                    foundlist.append((header, book))
                    lcount += 1
                    print('\rBooks Found: {:>9,d}  {:>5.2f}%  '.format(lcount, float(bcount/totbooks)*100), end='')
                if lcount == 0 and bcount % 5000 == 0:
                    print('\rBooks Searched: {:>9,d} {:>5.2f}%    '.format(bcount, float(bcount/totbooks)*100), end='')
        
            print()
            print('-'*160)
            if len(foundlist) == 0:
                print('\nNo books found!')
            else:
                cflist = len(foundlist)
                foundlist = list(set(foundlist))
                foundlist = sorted(foundlist, key = lambda x: (x[1].upper(), x[0].upper()))
                cflist = cflist-len(foundlist)
                if cflist > 0:
                    print('\nRemoved {:>5} duplicates'.format(cflist))
                print('-'*160)
    #            for (i, bbook) in enumerate(foundlist):
    #                print("{:>5}: {:15} {}".format(i, bbook[0], bbook[1]))
    #            print(len(foundlist))
                ofn = 'sbl_-_[{}].txt'.format(terms)
                print('\nWriting {:>5} books to file: {}'.format(len(foundlist), ofn))
                with open(os.path.join(searchdir, ofn), "w", encoding="utf8", errors='ignore') as ffile:
                    for line in foundlist:
                        ffile.write('{:15}{}\n'.format(line[0], line[1]))
            print('='*160)
    
    return


def Main():
    searchlists()

if __name__ == '__main__':
    Main()
