emojis = [
    u'\u262a',
    u'\u2764',
    u'\ud83d\ude00',
	u'\ud83d\ude01',
    u'\ud83d\ude02',
    u'\ud83e\udd23',
    u'\ud83d\ude03',
    u'\ud83d\ude04',
    u'\ud83d\ude05',
    u'\ud83d\ude06',
    u'\ud83d\ude09',
    u'\ud83d\ude0a',
    u'\ud83d\ude0b',
    u'\ud83d\ude0e',
    u'\ud83d\ude0d',
    u'\ud83d\ude18',
    u'\ud83d\ude17',
    u'\ud83e\udd17',
    u'\ud83e\udd14',
    u'\ud83d\ude10',
    u'\ud83d\ude44',
    u'\ud83d\ude0f',
    u'\ud83d\ude2e',
    u'\ud83e\udd10',
    u'\ud83d\ude34',
    u'\ud83d\ude0c',
    u'\ud83d\ude1c',
    u'\ud83d\ude14',
    u'\ud83d\ude15',
    u'\ud83d\ude32'
]
d = {}
for i,emj in enumerate(emojis):
    key = '?'+str(i)+'?'
    d[emj] = key
print(d)
