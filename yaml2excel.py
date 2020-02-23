import tablib
import yaml
import os
import xlwt
import click
import re


def create_id_excel(dir_path):
    # 创建ID.xls
    headers = ('卡號', '訂單', '扎號', '颜色', '尺碼', '数量')
    data = tablib.Dataset(headers=headers, title="扎卡綁定掃描")
    file_path = os.path.join(dir_path, "ID.xls")
    open(file_path, "wb").write(data.xlsx)


def create_style_excel(conf_path, dir_path):
    workbook = xlwt.Workbook()

    filename = os.path.split(conf_path)[1]
    val_data = filename.split(".")[0]
    key_data = val_data + "_chinese"

    # 创建需要的sheet对象
    sheet1 = workbook.add_sheet('款式', cell_overwrite_ok=True)
    sheet2 = workbook.add_sheet('尺寸檢測步驟', cell_overwrite_ok=True)
    sheet3 = workbook.add_sheet('對稱性檢測步驟', cell_overwrite_ok=True)
    sheet4 = workbook.add_sheet('步驟對應名稱', cell_overwrite_ok=True)
    sheet5 = workbook.add_sheet('示例圖', cell_overwrite_ok=True)
    sheet6 = workbook.add_sheet('多音字', cell_overwrite_ok=True)
    # 向sheet1中写入数据
    sheet1.write(0, 0, key_data)
    sheet1.write(0, 1, val_data)

    with open(conf_path, encoding='utf-8') as f:
        content = yaml.safe_load(f.read())

    result = []
    symmetric_result = []
    step = []
    img = []
    for k, v in content.items():
        diff = v.get("diff")
        measure = set([i.split("_")[0] for i in v.get("measure").keys()]
                      ) if diff else list(v.get("measure").keys())
        symmetric = [i.split("_")[0] for i in diff.keys()] if diff else []

        # 将addup字段中的数据添加到measure中
        addup = v.get("addup")
        for k in addup.keys():
            measure.add(k)

        # 组织sheet2的数据
        res_data = [k, *measure]
        result.append(res_data)

        # 组织sheet3的数据
        symmetric_check = [k, *symmetric]
        symmetric_result.append(symmetric_check)

        # 组织sheet4的数据
        step_data = [k, 1]
        step.append(step_data)

        # 组织sheet5
        img_data = [k, ""]
        img.append(img_data)

    # 向sheet2中写入数据
    for r in range(len(result)):
        [sheet2.write(r, i, v) for i, v in enumerate(result[r])]

    # 向sheet3中写入数据
    for r in range(len(symmetric_result)):
        [sheet3.write(r, i, v) for i, v in enumerate(symmetric_result[r])]

    # 向sheet4中写入数据
    for r in range(len(step)):
        [sheet4.write(r, i, v) for i, v in enumerate(step[r])]

    # 向sheet5中写入数据
    for r in range(len(img)):
        [sheet5.write(r, i, v) for i, v in enumerate(img[r])]

    workbook.save(os.path.join(dir_path, "款式.xls"))


def create_size_excel(conf_path, dir_path):

    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet('款式', cell_overwrite_ok=True)
    sheet2 = workbook.add_sheet('尺寸', cell_overwrite_ok=True)
    sheet3 = workbook.add_sheet('對稱性檢查項', cell_overwrite_ok=True)

    filename = os.path.split(conf_path)[1]
    style_data = filename.split(".")[0] + "_chinese"
    # 第一个sheet的表头
    sheet1.write(0, 0, "SoNo")
    sheet1.write(0, 1, "Style")
    sheet1.write(1, 0, "000000")
    # 第一个sheet的数据
    sheet1.write(1, 1, style_data)

    # 第二个sheet的表头
    sheet2.write_merge(0, 1, 0, 0, "SoNo")
    sheet2.write_merge(0, 1, 1, 1, "ChnCode")
    sheet2.write_merge(0, 1, 2, 2, "Fold")
    sheet2.write_merge(0, 1, 3, 3, "Unit")
    sheet2.write_merge(0, 1, 4, 4, "Check")

    sheet2.write_merge(0, 0, 5, 8, "S")
    sheet2.write(1, 5, "标准值")
    sheet2.write(1, 6, "Tol(-)")
    sheet2.write(1, 7, "Tol(+)")
    sheet2.write(1, 8, "Offset")

    # 第三个sheet的表头
    sheet3.write(0, 0, "SoNo")
    sheet3.write(0, 1, "SymCode")
    sheet3.write(0, 2, "SymTol")

    with open(conf_path, encoding='utf-8') as f:
        content = yaml.safe_load(f.read())

    chn_code_list = []
    # 组织sheet3的数据
    for k, v in content.items():
        diff = v.get("diff")
        symmetric = [i.split("_")[0] for i in diff.keys()] if diff else []
        measure = list(set([i.split("_")[0] for i in v.get(
            "measure").keys()])) if diff else list(v.get("measure").keys())

        # 增加auxiliary 項中后缀为_std_val的字段添加到尺寸表尺寸中
        auxiliary = v.get("auxiliary")
        r = re.compile("^[0-9]_std_val$")
        for k, v in auxiliary.items():
            result = r.search(k)
            if result:
                # measure.append(result.group())
                measure.append(v)

        # 将addup字段中的数据添加到measure中
        addup = v.get("addup")
        for k in addup.keys():
            measure.add(k)

        if symmetric:
            for i, v in enumerate(range(1, len(symmetric)+1)):
                sheet3.write(v, 0, "000000")
                sheet3.write(v, 1, symmetric[i])
                sheet3.write(v, 2, "1/8")

        chn_code_list += measure

    # sheet2的数据整合
    for i, v in enumerate(range(2, len(chn_code_list)+2)):
        sheet2.write(v, 0, "000000")
        sheet2.write(v, 1, chn_code_list[i])
        sheet2.write(v, 2, 1)
        sheet2.write(v, 3, "cm")
        sheet2.write(v, 4, "Y")

    workbook.save(os.path.join(dir_path, "尺寸表.xls"))


@click.command()
@click.option("--p", help="需要转换的配置文件的路径")
def main(p):
    if os.path.exists(p):
        filename = os.path.split(p)[1]
        data = filename.split(".")[0] + "_chinese"
        dirname = data + "+000000"
        dir_path = os.path.join(os.path.split(p)[0], dirname)
        os.makedirs(dir_path, exist_ok=True)
        create_id_excel(dir_path)
        create_style_excel(p, dir_path)
        create_size_excel(p, dir_path)
    else:
        raise FileNotFoundError("file is not exists!")


if __name__ == "__main__":
    main()


