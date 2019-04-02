import xlwt

def write_excel():
    xlwt_file = xlwt.Workbook()
    table = xlwt_file.add_sheet('data',cell_overwrite_ok=True)
    f = open('coco_dushi.txt')
    data_str = str(f.read())
    datas = data_str.split("<td class='text-left nowrap'>CoCo")
    i = 0
    table.write(i, 0, unicode('name', 'utf-8'))
    table.write(i, 1, unicode('city', 'utf-8'))
    table.write(i, 2, unicode('strict', 'utf-8'))
    table.write(i, 3, unicode('sales', 'utf-8'))
    table.write(i, 4, unicode('score', 'utf-8'))
    table.write(i, 5, unicode('time arrive', 'utf-8'))
    table.write(i, 6, unicode('total comments', 'utf-8'))
    table.write(i, 7, unicode('good comments', 'utf-8'))
    i = i + 1
    for data in datas:
        data_split = data.split('<\\/td>\\r\\n\\t\\t\\t<td class=\'text-left nowrap\'>')
        if len(data_split) >= 27:
            names = data_split[0].split('<td class=\'text-left nowrap\'>')
            if len(names) > 0:
                name = names[0]
                table.write(i, 0, unicode('CoCo' + name, 'utf-8'))
                city = data_split[1]
                table.write(i, 1, unicode(city, 'utf-8'))
                strict = data_split[3]
                table.write(i, 2, unicode(strict, 'utf-8'))
                sales_num = data_split[12]
                table.write(i, 3, unicode(sales_num, 'utf-8'))
                total_score = data_split[17]
                table.write(i, 4, unicode(total_score, 'utf-8'))
                time = data_split[22]
                table.write(i, 5, unicode(time, 'utf-8'))
                total_judge = data_split[25]
                table.write(i, 6, unicode(total_judge, 'utf-8'))
                good_judge = data_split[26]
                table.write(i, 7, unicode(good_judge, 'utf-8'))
                i = i + 1
    xlwt_file.save('data.xls')

if __name__ == '__main__':
    write_excel()
