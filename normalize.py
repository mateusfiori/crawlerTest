dataset = pd.read_csv('datasetFunk.csv')

arquivo = open('datasetNorm.txt', 'w', encoding='utf-8')
arquivo.write('letra,label\n\n')

# chars_to_remove = ['D7', 'F7', 'Dm']

s = dataset.letra[0]

# a = re.sub("\d+", " ", a)
# rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
# a = re.sub(rx, '', s)
a = re.sub("\s\s+", " ", s)

cont = 0
while cont < dataset.shape[0]:
    cont += 1

print()