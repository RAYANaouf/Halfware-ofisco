import openpyxl
wb = openpyxl.load_workbook(r'C:\Users\pc\Downloads\Custom Field.xlsx', data_only=True)
ws = wb['Custom Field']
for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True)):
    print('Row', i, row[1], repr(row[1]), row[7], row[2])
