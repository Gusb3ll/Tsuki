from hentai import Hentai, Format

try:
  code = int(input('6 degit number : '))
except:
  print('Invalid input')

doujin = Hentai(code)

Hentai.exists(doujin.id)

print(f'Downloading : {doujin.id} - {doujin.title(Format.Pretty)}')

doujin.download(progressbar=True)