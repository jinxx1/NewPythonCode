import datetime
import exifread
import re



if __name__ == '__main__':
    file = 'aaa2018-01-01aaa'
    # file = 'aaaFDGDFGaaa'
    dateTime = None
    regxTime = re.compile("\d{4}-\d{2}-\d{2}")
    getTime = regxTime.search(file)
    if getTime:
        dateTime = datetime.datetime.strptime(str(getTime.group()), '%Y-%m-%d')
    print(dateTime)