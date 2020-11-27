# 为了实现多条件的组合筛选，可以使用如下方法进行组合，不知道是否是最优的，但是经测试可以达到联合筛选的效果
# 其中ins_name project_name image_type ins_status为筛选的参数，如果不传默认为‘’（默认值可以根据需要改变）
final_result = []
if (i.get('name') == ins_name or ins_name == '') and (i.get('project_name') == event_name or event_name == '') \
    and (i.get('hypervisor_type') == image_type or image_type == '') and (i.get('power_state') == ins_status or ins_status == ''):
    final_result.append(i)
