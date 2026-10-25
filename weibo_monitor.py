import requests
import re
import time
import random
import json
import os
from datetime import datetime, timedelta

# ================= 配置区 =================
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# 1. 苏新皓
SU_XINHAO_CONFIG = {
    "name": "苏新皓",
    "url": "https://api.weibo.cn/2/statuses/container_timeline_topicpage?is_push_open=0&st_bottom_bar_new_style_enable=1&networktype=wifi&is_container=1&page_reform_enable=1&launchid=10000365--x&hasContent=false&flowId=10080819a5137ac9109462f670e39aaf64b1a0&is_pad=false&page_interrupt_enable=1&orifid=profile_me&sg_flow_header_enable=1&uicode=10000011&ul_hid=edd9b617-829a-4ee9-86aa-79fa53b77c20&ul_sid=edd9b617-829a-4ee9-86aa-79fa53b77c20&moduleID=700&taskType=refresh&just_followed=false&wb_version=8202&sg_field_default_null_enable=1&source_code=10000011_profile_me&is_push_alert=1&screenWidth=600&pageDataType=flow&c=android&s=b198710d&ft=0&tz=Asia%2FShanghai&ua=Samsung-SM-A5360__weibo__16.10.0__android__android15&wm=2468_1001&aid=01A0qmYxTlY9zX081BxBpuCxAwfR5NRSAp0OE_3iLnB1Vl9PE.&fid=10080819a5137ac9109462f670e39aaf64b1a0&v_f=2&v_p=93&from=10GA095010&gsid=_2A25H2YCvDeRxGeFH7lQY8CjNyDyIHXVizpNnrDV6PUJbkdAbLUnkkWpNevvXPwgFn8zOxk0qRetxedAIQhy7IE7q&lang=zh_CN&lfid=profile_me&skin=default&has_cache=1&dlang=zh-Hans-CN&oldwm=2468_1001&sflag=1&oriuicode=10000011&containerid=10080819a5137ac9109462f670e39aaf64b1a0&sgtotal_activity_enable=1&sg_widget_state=-1&is_load_container=1&luicode=10000011&android_id=fd2e50cf0ac06be9&shallow_consume=1&header_skin_enable=0&mix_media_enable=1&refresh=init&supergroup_album_v2=1&last_download_time=-1&request_referer=-1&is_album_water_fall=1&flowVersion=0.0.1&book_reservation=1&redpacket_fly=1&sg_tab_config=2&ul_ctime=1792930335373&invokeType=init&cum=026E245A",
    "headers": {
        "host": "api.weibo.cn",
        "authorization": "WB-SUT _2A95H2YCvDeRxGeFH7lQY8CjNyDyIHXVizpNnrDV6PUJbkdAbLWrWkWpNevvXPyW7pRAa24WxSHoCEelvp_jbfDCJ",
        "user-agent": USER_AGENT,
        "x-log-uid": "7956906130",
        "x-sessionid": "0eda3baa-8bc9-4ad2-a052-1efb6d7c519d",
        "accept-encoding": "gzip, deflate, br"
    },
    "payload": {
        "is_push_open": "0", "st_bottom_bar_new_style_enable": "1", "is_container": "1",
        "page_reform_enable": "1", "hasContent": "false", "flowId": "10080819a5137ac9109462f670e39aaf64b1a0",
        "page_interrupt_enable": "1", "sg_flow_header_enable": "1", "taskType": "refresh",
        "just_followed": "false", "sg_field_default_null_enable": "1", "is_push_alert": "1",
        "screenWidth": "600", "pageDataType": "flow", "tz": "Asia/Shanghai",
        "containerid": "10080819a5137ac9109462f670e39aaf64b1a0", "sgtotal_activity_enable": "1",
        "sg_widget_state": "-1", "is_load_container": "1", "shallow_consume": "1",
        "header_skin_enable": "0", "mix_media_enable": "1", "refresh": "init",
        "supergroup_album_v2": "1", "last_download_time": "-1", "is_album_water_fall": "1",
        "flowVersion": "0.0.1", "book_reservation": "1", "redpacket_fly": "1",
        "sg_tab_config": "2", "invokeType": "init"
    }
}

# 2. 朱志鑫
ZHU_ZHIXIN_CONFIG = {
    "name": "朱志鑫",
    "url": "https://api.weibo.cn/2/statuses/container_timeline_topicpage?trim_level=1&is_push_open=0&st_bottom_bar_new_style_enable=1&networktype=wifi&extparam=%E6%9C%B1%E5%BF%97%E9%91%AB&is_container=1&flowDynaVersion=%7B%22componentVersion%22%3A%221%22%2C%22moduleVersion%22%3A%221%22%2C%22groupVersion%22%3A%221%22%7D&is_header_sticky=0&image_type=heif_filter&page_reform_enable=1&launchid=10000365--x&manualType=pull&wait_no_need_refresh=true&screen_attrs=900_1600_1.5&hasContent=true&flowId=100808ab88231fa0b181b2200c636e4e2f164a_-_recommend&is_pad=false&page_interrupt_enable=1&orifid=102803_ctg1_1780_-_ctg1_1780%24%24100103type%3D1%26q%3D%E6%9C%B1%E5%BF%97%E9%91%AB%E8%B6%85%E8%AF%9D%26t%3D2&sg_flow_header_enable=1&uicode=10000011&ul_hid=edd9b617-829a-4ee9-86aa-79fa53b77c20&ul_sid=edd9b617-829a-4ee9-86aa-79fa53b77c20&moduleID=700&fromlog=100808ab88231fa0b181b2200c636e4e2f164a_-_recommend&wait_refresh_more_info=%7B%22pagingType%22%3A%22cursor%22%2C%22params%22%3A%7B%22page%22%3A2%2C%22since_id%22%3A%22%7B%5C%22max_id%5C%22%3A1%2C%5C%22ad_after%5C%22%3A6%7D%22%2C%22max_id%22%3A0%7D%2C%22error%22%3A%22%E7%BD%91%E7%BB%9C%E5%8A%A0%E8%BD%BD%E5%A4%B1%E8%B4%A5%EF%BC%8C%E8%AF%B7%E7%A8%8D%E5%90%8E%E5%B0%9D%E8%AF%95%22%2C%22loading%22%3A%22%E6%AD%A3%E5%9C%A8%E5%8A%A0%E8%BD%BD%E6%9B%B4%E5%A4%9A%22%2C%22moreType%22%3A%22default%22%7D&lastItemTime=0&taskType=refresh&featurecode=10000011&wb_version=8202&sg_field_default_null_enable=1&source_code=10000003_100103type%3D1%26q%3D%E6%9C%B1%E5%BF%97%E9%91%AB%E8%B6%85%E8%AF%9D%26t%3D2&is_push_alert=1&pageDataType=flow&lcardid=f3f41727-d068-4a7b-9811-f449051781c6&c=android&s=b198710d&ft=0&tz=Asia%2FShanghai&ua=Samsung-SM-A5360__weibo__16.10.0__android__android15&wm=2468_1001&aid=01A0qmYxTlY9zX081BxBpuCxAwfR5NRSAp0OE_3iLnB1Vl9PE.&ext=search_vsid%3A4804315284bbcab8df228b7eee1ca140%7Csearch_ssid%3A4804315284bbcab8df228b7eee1ca140&fid=100808ab88231fa0b181b2200c636e4e2f164a_-_recommend&v_f=2&v_p=93&from=10GA095010&gsid=_2A25H2YCvDeRxGeFH7lQY8CjNyDyIHXVizpNnrDV6PUJbkdAbLUnkkWpNevvXPwgFn8zOxk0qRetxedAIQhy7IE7q&lang=zh_CN&lfid=100103type%3D1%26q%3D%E6%9C%B1%E5%BF%97%E9%91%AB%E8%B6%85%E8%AF%9D%26t%3D2&page=1&skin=default&trim=1&count=15&dlang=zh-Hans-CN&oldwm=2468_1001&sflag=1&oriuicode=10001344_10000003&stream_visible=1&sgtotal_activity_enable=1&luicode=10000003&wait_refresh_refresh_info=%7B%22pagingType%22%3A%22page%22%2C%22refreshtype%22%3A%22clear%22%2C%22params%22%3A%7B%22count%22%3A15%2C%22lastItemTime%22%3A0%2C%22page%22%3A1%2C%22page_common_ext%22%3A%22topicPrompt%3A1%7Cpage%3Arecommend%3D1%7Chide_page%3A2%22%7D%7D&android_id=fd2e50cf0ac06be9&shallow_consume=1&header_skin_enable=0&mix_media_enable=1&refresh=pulldown&supergroup_album_v2=1&pagingType=page&page_common_ext=topicPrompt%3A1%7Cpage%3Arecommend%3D1%7Chide_page%3A2&is_album_water_fall=1&flowVersion=0.0.1&book_reservation=1&sg_tab_config=2&ul_ctime=1792931754952&invokeType=manual&cum=BFB82D5F",
    "headers": {
        "host": "api.weibo.cn",
        "authorization": "WB-SUT _2A95H2YCvDeRxGeFH7lQY8CjNyDyIHXVizpNnrDV6PUJbkdAbLWrWkWpNevvXPyW7pRAa24WxSHoCEelvp_jbfDCJ",
        "user-agent": USER_AGENT,
        "x-log-uid": "7956906130",
        "x-sessionid": "854f12f6-3af8-4e03-9a01-302a1ca3a798",
        "accept-encoding": "gzip, deflate, br"
    },
    "payload": {
        "is_push_open": "0", "st_bottom_bar_new_style_enable": "1", "is_container": "1",
        "flowDynaVersion": '{"componentVersion":"1","moduleVersion":"1","groupVersion":"1"}',
        "page_reform_enable": "1", "manualType": "pull", "wait_no_need_refresh": "true",
        "screen_attrs": "900_1600_1.5", "hasContent": "true", 
        "flowId": "100808ab88231fa0b181b2200c636e4e2f164a_-_recommend",
        "page_interrupt_enable": "1", "sg_flow_header_enable": "1",
        "wait_refresh_more_info": '{"pagingType":"cursor","params":{"page":2,"since_id":"{\\"max_id\\":1,\\"ad_after\\":6}","max_id":0},"error":"网络加载失败，请稍后尝试","loading":"正在加载更多","moreType":"default"}',
        "lastItemTime": "0", "taskType": "refresh", "sg_field_default_null_enable": "1",
        "bizType": "supergroup", "is_push_alert": "1", "pageDataType": "flow", "tz": "Asia/Shanghai",
        "v_p": "93", "page": "1", "count": "15", "feedDynamicEnable": "1", "stream_visible": "1",
        "sgtotal_activity_enable": "1",
        "wait_refresh_refresh_info": '{"pagingType":"page","refreshtype":"clear","params":{"count":15,"lastItemTime":0,"page":1,"page_common_ext":"topicPrompt:1|page:recommend=1|hide_page:2"}}',
        "shallow_consume": "1", "header_skin_enable": "0", "mix_media_enable": "1",
        "supergroup_album_v2": "1", "testUnreleasedCardEnable": "0", "pagingType": "page",
        "dynamicBundleVersion": "1598213", "page_common_ext": "topicPrompt:1|page:recommend:1|hide_page:2",
        "is_album_water_fall": "1", "flowVersion": "0.0.1", "book_reservation": "1",
        "sg_tab_config": "2", "invokeType": "manual"
    }
}

# 3. 陈奕恒
CHEN_YIHENG_CONFIG = {
    "name": "陈奕恒",
    "url": "https://api.weibo.cn/2/statuses/container_timeline_topicpage?trim_level=1&is_push_open=0&st_bottom_bar_new_style_enable=1&networktype=wifi&extparam=%E9%99%88%E5%A5%95%E6%81%92&is_container=1&flowDynaVersion=%7B%22componentVersion%22%3A%221%22%2C%22moduleVersion%22%3A%221%22%2C%22groupVersion%22%3A%221%22%7D&is_header_sticky=0&image_type=heif_filter&page_reform_enable=1&launchid=10000365--x&manualType=pull&wait_no_need_refresh=true&screen_attrs=900_1600_1.5&hasContent=true&flowId=100808416561dd8d6e5365a23477dce47fa369_-_recommend&is_pad=false&page_interrupt_enable=1&source_mid=100103type%3D1%26q%3D%E9%99%88%E9%80%B8%E6%81%92%E8%B6%85%E8%AF%9D%26t%3D1_5325749103889231&orifid=102803_ctg1_1780_-_ctg1_1780%24%24100103type%3D1%26q%3D%E9%99%88%E9%80%B8%E6%81%92%E8%B6%85%E8%AF%9D%26t%3D1&sg_flow_header_enable=1&uicode=10000011&ul_hid=d1390362-a1bc-4997-8939-b425f4638f30&ul_sid=d1390362-a1bc-4997-8939-b425f4638f30&moduleID=700&fromlog=100808416561dd8d6e5365a23477dce47fa369_-_recommend&wait_refresh_more_info=%7B%22pagingType%22%3A%22cursor%22%2C%22params%22%3A%7B%22page%22%3A2%2C%22since_id%22%3A%22%7B%5C%22max_id%5C%22%3A1%2C%5C%22ad_after%5C%22%3A6%7D%22%2C%22max_id%22%3A0%7D%2C%22error%22%3A%22%E7%BD%91%E7%BB%9C%E5%8A%A0%E8%BD%BD%E5%A4%B1%E8%B4%A5%EF%BC%8C%E8%AF%B7%E7%A8%8D%E5%90%8E%E5%B0%9D%E8%AF%95%22%2C%22loading%22%3A%22%E6%AD%A3%E5%9C%A8%E5%8A%A0%E8%BD%BD%E6%9B%B4%E5%A4%9A%22%2C%22moreType%22%3A%22default%22%7D&lastItemTime=0&taskType=refresh&featurecode=10000011&wb_version=8202&sg_field_default_null_enable=1&source_code=10000003_100103type%3D1%26q%3D%E9%99%88%E9%80%B8%E6%81%92%E8%B6%85%E8%AF%9D%26t%3D1&is_push_alert=1&pageDataType=flow&c=android&s=b198710d&ft=0&tz=Asia%2FShanghai&ua=Samsung-SM-A5360__weibo__16.10.0__android__android15&wm=2468_1001&aid=01A0qmYxTlY9zX081BxBpuCxAwfR5NRSAp0OE_3iLnB1Vl9PE.&ext=search_vsid%3Abfecb9e9c3e99f56753f17aecc30887d%7Csearch_ssid%3Abfecb9e9c3e99f56753f17aecc30887d&fid=100808416561dd8d6e5365a23477dce47fa369_-_recommend&v_f=2&v_p=93&from=10GA095010&gsid=_2A25H2YCvDeRxGeFH7lQY8CjNyDyIHXVizpNnrDV6PUJbkdAbLUnkkWpNevvXPwgFn8zOxk0qRetxedAIQhy7IE7q&lang=zh_CN&lfid=100103type%3D1%26q%3D%E9%99%88%E9%80%B8%E6%81%92%E8%B6%85%E8%AF%9D%26t%3D1&page=1&skin=default&trim=1&count=15&dlang=zh-Hans-CN&oldwm=2468_1001&sflag=1&oriuicode=10001344_10000003&stream_visible=1&sgtotal_activity_enable=1&luicode=10000003&wait_refresh_refresh_info=%7B%22pagingType%22%3A%22page%22%2C%22refreshtype%22%3A%22clear%22%2C%22params%22%3A%7B%22count%22%3A15%2C%22lastItemTime%22%3A0%2C%22page%22%3A1%2C%22page_common_ext%22%3A%22topicPrompt%3A1%7Cpage%3Arecommend%3D1%7Chide_page%3A1%22%7D%7D&android_id=fd2e50cf0ac06be9&shallow_consume=1&header_skin_enable=0&mix_media_enable=1&refresh=pulldown&supergroup_album_v2=1&pagingType=page&page_common_ext=topicPrompt%3A1%7Cpage%3Arecommend%3D1%7Chide_page%3A1&is_album_water_fall=1&flowVersion=0.0.1&book_reservation=1&sg_tab_config=2&ul_ctime=1792932693519&invokeType=manual&cum=6476716B",
    "headers": {
        "host": "api.weibo.cn",
        "authorization": "WB-SUT _2A95H2YCvDeRxGeFH7lQY8CjNyDyIHXVizpNnrDV6PUJbkdAbLWrWkWpNevvXPyW7pRAa24WxSHoCEelvp_jbfDCJ",
        "user-agent": USER_AGENT,
        "x-log-uid": "7956906130",
        "x-sessionid": "a8aff4be-c18d-4463-8b75-cfa21487530e",
        "accept-encoding": "gzip, deflate, br"
    },
    "payload": {
        "is_push_open": "0", "st_bottom_bar_new_style_enable": "1", "is_container": "1",
        "flowDynaVersion": '{"componentVersion":"1","moduleVersion":"1","groupVersion":"1"}',
        "page_reform_enable": "1", "manualType": "pull", "wait_no_need_refresh": "true",
        "screen_attrs": "900_1600_1.5", "hasContent": "true", 
        "flowId": "100808416561dd8d6e5365a23477dce47fa369_-_recommend",
        "page_interrupt_enable": "1", "sg_flow_header_enable": "1",
        "wait_refresh_more_info": '{"pagingType":"cursor","params":{"page":2,"since_id":"{\\"max_id\\":1,\\"ad_after\\":6}","max_id":0},"error":"网络加载失败，请稍后尝试","loading":"正在加载更多","moreType":"default"}',
        "lastItemTime": "0", "taskType": "refresh", "sg_field_default_null_enable": "1",
        "bizType": "supergroup", "is_push_alert": "1", "pageDataType": "flow", "tz": "Asia/Shanghai",
        "v_p": "93", "page": "1", "count": "15", "feedDynamicEnable": "1", "stream_visible": "1",
        "sgtotal_activity_enable": "1",
        "wait_refresh_refresh_info": '{"pagingType":"page","refreshtype":"clear","params":{"count":15,"lastItemTime":0,"page":1,"page_common_ext":"topicPrompt:1|page:recommend=1|hide_page:1"}}',
        "shallow_consume": "1", "header_skin_enable": "0", "mix_media_enable": "1",
        "supergroup_album_v2": "1", "testUnreleasedCardEnable": "0", "pagingType": "page",
        "dynamicBundleVersion": "1598213", "page_common_ext": "topicPrompt:1|page:recommend:1|hide_page:1",
        "is_album_water_fall": "1", "flowVersion": "0.0.1", "book_reservation": "1",
        "sg_tab_config": "2", "invokeType": "manual"
    }
}

# 4. 王橹杰
WANG_LUJIE_CONFIG = {
    "name": "王橹杰",
    "url": "https://api.weibo.cn/2/statuses/container_timeline_topicpage?is_push_open=0&st_bottom_bar_new_style_enable=1&networktype=wifi&extparam=%E7%8E%8B%E6%A9%B9%E6%9D%B0&is_container=1&page_reform_enable=1&launchid=10000365--x&hasContent=false&flowId=1008080587fa0e8198ad45108f3a0ef6e08d3a&is_pad=false&page_interrupt_enable=1&orifid=102803_ctg1_1780_-_ctg1_1780%24%24100103type%3D1%26q%3D%E7%8E%8B%E6%A9%B9%E6%9D%B0%E8%B6%85%E8%AF%9D%26t%3D2&sg_flow_header_enable=1&uicode=10000011&ul_hid=d1390362-a1bc-4997-8939-b425f4638f30&ul_sid=d1390362-a1bc-4997-8939-b425f4638f30&moduleID=700&taskType=refresh&just_followed=false&wb_version=8202&sg_field_default_null_enable=1&source_code=10000003_100103type%3D1%26q%3D%E7%8E%8B%E6%A9%B9%E6%9D%B0%E8%B6%85%E8%AF%9D%26t%3D2&is_push_alert=1&screenWidth=600&pageDataType=flow&lcardid=e03b0c1e-2018-4127-a938-adf71713d55c&c=android&s=b198710d&ft=0&tz=Asia%2FShanghai&ua=Samsung-SM-A5360__weibo__16.10.0__android__android15&wm=2468_1001&aid=01A0qmYxTlY9zX081BxBpuCxAwfR5NRSAp0OE_3iLnB1Vl9PE.&ext=search_vsid%3A30a20ea5e92222c76592d9cd7c5a6735%7Csearch_ssid%3A30a20ea5e92222c76592d9cd7c5a6735&fid=1008080587fa0e8198ad45108f3a0ef6e08d3a&v_f=2&v_p=93&from=10GA095010&gsid=_2A25H2YCvDeRxGeFH7lQY8CjNyDyIHXVizpNnrDV6PUJbkdAbLUnkkWpNevvXPwgFn8zOxk0qRetxedAIQhy7IE7q&lang=zh_CN&lfid=100103type%3D1%26q%3D%E7%8E%8B%E6%A9%B9%E6%9D%B0%E8%B6%85%E8%AF%9D%26t%3D2&skin=default&has_cache=0&dlang=zh-Hans-CN&oldwm=2468_1001&sflag=1&oriuicode=10001344_10000003&containerid=1008080587fa0e8198ad45108f3a0ef6e08d3a&sgtotal_activity_enable=1&sg_widget_state=-1&is_load_container=1&luicode=10000003&android_id=fd2e50cf0ac06be9&shallow_consume=1&header_skin_enable=0&mix_media_enable=1&refresh=init&supergroup_album_v2=1&last_download_time=-1&request_referer=-1&is_album_water_fall=1&flowVersion=0.0.1&book_reservation=1&redpacket_fly=1&sg_tab_config=2&ul_ctime=1792932744337&invokeType=init&cum=1951F6B1",
    "headers": {
        "host": "api.weibo.cn",
        "authorization": "WB-SUT _2A95H2YCvDeRxGeFH7lQY8CjNyDyIHXVizpNnrDV6PUJbkdAbLWrWkWpNevvXPyW7pRAa24WxSHoCEelvp_jbfDCJ",
        "user-agent": USER_AGENT,
        "x-log-uid": "7956906130",
        "x-sessionid": "9fb3bc69-0c4b-4afa-814f-011e8a92ac3d",
        "accept-encoding": "gzip, deflate, br"
    },
    "payload": {
        "is_push_open": "0", "st_bottom_bar_new_style_enable": "1", "is_container": "1",
        "page_reform_enable": "1", "hasContent": "false", "flowId": "1008080587fa0e8198ad45108f3a0ef6e08d3a",
        "page_interrupt_enable": "1", "sg_flow_header_enable": "1", "taskType": "refresh",
        "just_followed": "false", "sg_field_default_null_enable": "1", "is_push_alert": "1",
        "screenWidth": "600", "pageDataType": "flow", "tz": "Asia/Shanghai",
        "containerid": "1008080587fa0e8198ad45108f3a0ef6e08d3a", "sgtotal_activity_enable": "1",
        "sg_widget_state": "-1", "is_load_container": "1", "shallow_consume": "1",
        "header_skin_enable": "0", "mix_media_enable": "1", "refresh": "init",
        "supergroup_album_v2": "1", "last_download_time": "-1", "is_album_water_fall": "1",
        "flowVersion": "0.0.1", "book_reservation": "1", "redpacket_fly": "1",
        "sg_tab_config": "2", "invokeType": "init"
    }
}

TOPICS_CONFIG = [SU_XINHAO_CONFIG, ZHU_ZHIXIN_CONFIG, CHEN_YIHENG_CONFIG, WANG_LUJIE_CONFIG]
JSON_FILE = "cloud_data.json"

# ==========================================

def get_count_from_topic(topic):
    try:
        # 你的代理地址
        proxy_url = "https://my-weibo-proxy.2078397070.workers.dev/"
        
        request_data = {
            "url": topic["url"],
            "headers": topic["headers"],
            "payload": topic["payload"]
        }
        
        # 向代理发送 JSON 数据
        response = requests.post(
            proxy_url, 
            json=request_data, 
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"❌ [{topic['name']}] HTTP 状态码: {response.status_code}")
            print(f"返回内容: {response.text[:150]}")
            return None
            
        data = response.json()
        
        # ========== 解析逻辑 ==========
        labels = data.get('header', {}).get('data', {}).get('label_list', [])
        
        if not labels:
            print(f"⚠️ [{topic['name']}] 请求成功，但没找到 label_list 数据。可能被风控或参数失效。")
            print(f"返回内容预览: {str(data)[:150]}")
            return None
            
        for label in labels:
            text = label.get('text', '')
            if '超LIKE' in text:
                match = re.search(r'超LIKE\s*(\d+)人', text)
                if match:
                    return int(match.group(1))
                    
        all_texts = [l.get('text', '') for l in labels]
        print(f"⚠️ [{topic['name']}] 没匹配到超LIKE，现有的标签是: {all_texts}")
        return None
        
    except Exception as e:
        print(f"⚠️ 获取 [{topic['name']}] 时发生异常: {e}")
        return None
        
def main():
    # 强制使用北京时间 (UTC+8)，适配 GitHub Actions 的服务器时间
    beijing_now = datetime.utcnow() + timedelta(hours=8)
    current_time = beijing_now.strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"\n========== 🚀 开始抓取: {current_time} ==========")
    
    row_data = {"time": current_time}
    
    # 1. 抓取数据
    for i, topic in enumerate(TOPICS_CONFIG):
        name = topic["name"]
        count = get_count_from_topic(topic)
        
        row_data[name] = count
        
        if count is not None:
            print(f"✅ [{name}]: {count}人 ")
        else:
            print(f"❌ [{name}]: 抓取失败 ")
        
        # 停顿 3-6 秒，防封号
        if i < len(TOPICS_CONFIG) - 1:
            time.sleep(random.uniform(3, 6))

    # 2. 读取历史 JSON 数据（如果没有则新建）
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except:
                history = {"times": [], "series": {"苏新皓": [], "朱志鑫": [], "陈奕恒": [], "王橹杰": []}}
    else:
        history = {"times": [], "series": {"苏新皓": [], "朱志鑫": [], "陈奕恒": [], "王橹杰": []}}

    # 3. 将新数据追加到历史记录中
    history["times"].append(row_data["time"])
    for name in ["苏新皓", "朱志鑫", "陈奕恒", "王橹杰"]:
        history["series"][name].append(row_data.get(name, None))

    # 4. 可选：保留最近 300 次数据，防止 JSON 无限变大
    if len(history["times"]) > 300:
        history["times"] = history["times"][-300:]
        for name in history["series"].keys():
            history["series"][name] = history["series"][name][-300:]

    # 5. 保存回 JSON 文件
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
        
    print(f"⭐ 数据已成功追加到 {JSON_FILE}\n")

if __name__ == "__main__":
    main()
