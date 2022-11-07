# -*- coding: utf-8 -*-
"""
Created on Sat May 22 21:37:46 2021

@author: brian
"""

from tensorflow.python.keras import backend as K
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.preprocessing import image
from tensorflow.keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.applications.efficientnet import EfficientNetB4

import tensorflow as tf
import sys
import numpy as np
import os
import shutil
import random
import time
import csv
import pandas as pd

clss = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D',
        'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
         'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
        'V', 'W', 'X', 'Y', 'Z', 'a-', 'b-', 'c-', 'd-', 'e-', 'f-',
        'g-', 'h-', 'i-', 'j-', 'k-', 'l-','m-', 'n-', 'o-', 'p-', 'q-', 'r-', 's-', 't-', 'u-',
         'v-', 'w-', 'x-', 'y-', 'z-',
        '一', '丁', '七', '三', '上', '下', '不', '世', '丘', '丙', '丞', '丟', '並', '中', '丰', '串', '丸', '丹', '主', '丼', '久', '之', '乘', '乙', '九', '也', '乳', '乾', '亀', '了', '事', '二', '互', '五', '井', '亞', '交', '亨', '享', '京', '亭', '亮', '人', '什', '仁', '今', '介', '从', '仔', '仕', '他', '付', '仙', '仟', '代', '令', '以', '仲', '件', '任', '份', '仿', '企', '伊', '伍', '休', '众', '伙', '伯', '估', '伴', '伸', '佈', '位', '低', '住', '佐', '佑', '何', '佛', '作', '你', '佩', '佰', '佳', '使', '來', '例', '供', '依', '便', '係', '促', '俊', '俗', '保', '俠', '信', '修', '俱', '倆', '倉', '個', '倍', '們', '倒', '候', '借', '倪', '倫', '值', '假', '偉', '偕', '做', '停', '健', '側', '傅', '傑', '傘', '備', '傢', '傳', '傷', '像', '僑', '價', '儀', '億', '儒', '優', '儲', '儷', '元', '兄', '充', '兆', '先', '光', '克', '免', '兒', '兔', '入', '內', '全', '兩', '八', '公', '六', '共', '兵', '其', '具', '典', '兼', '冊', '再', '冒', '冠', '冬', '冰', '冷', '凌', '凍', '凝', '凡', '凰', '凱', '出', '刀', '刁', '分', '切', '刈', '刊', '列', '初', '別', '刨', '利', '刮', '到', '制', '刷', '券', '刺', '刻', '剉', '削', '剌', '前', '剪', '割', '創', '劃', '劇', '劉', '劍', '劑', '力', '功', '加', '助', '努', '劵', '勁', '勇', '勒', '動', '務', '勝', '勞', '勢', '勤', '勳', '勵', '勿', '包', '化', '北', '匙', '匠', '匯', '區', '十', '千', '升', '午', '卉', '半', '卍', '卓', '協', '南', '博', '卜', '卡', '卦', '印', '危', '即', '卷', '卸', '厚', '厝', '原', '厲', '去', '叁', '參', '又', '及', '友', '双', '叔', '取', '受', '口', '古', '另', '只', '叫', '召', '叮', '可', '台', '史', '右', '号', '司', '吃', '各', '合', '吉', '吊', '同', '名', '后', '吐', '向', '君', '吧', '含', '吳', '吸', '吾', '呈', '告', '周', '呱', '味', '呷', '呼', '命', '和', '咕', '咖', '咩', '咪', '咳', '品', '哈', '員', '哥', '哩', '唇', '唐', '售', '唯', '唱', '商', '問', '啓', '啟', '啡', '啤', '啦', '善', '喉', '喘', '喜', '喝', '喫', '喬', '單', '喵', '嗎', '嗑', '嗲', '嗽', '嘉', '嘟', '嘴', '噌', '器', '噴', '嚐', '嚕', '嚴', '囉', '囍', '四', '回', '因', '固', '圈', '國', '圍', '園', '圓', '圖', '團', '土', '在', '地', '圾', '址', '均', '坊', '坐', '坑', '坡', '坤', '坦', '坪', '垂', '垃', '型', '垣', '城', '埔', '埕', '域', '培', '基', '堂', '堃', '堅', '堆', '堡', '堤', '報', '場', '塊', '塑', '塔', '塗', '塩', '填', '塵', '境', '墅', '墊', '墘', '增', '墨', '墾', '壁', '壓', '壞', '壢', '士', '売', '壹', '壺', '壽', '夏', '外', '多', '夜', '夠', '夢', '夥', '大', '天', '太', '夫', '央', '夯', '失', '夷', '夾', '奇', '奈', '奕', '套', '奧', '奪', '女', '奶', '好', '如', '妃', '妍', '妙', '妝', '妮', '妳', '妹', '姆', '姊', '始', '姐', '姑', '姓', '委', '姜', '姨', '姿', '威', '娃', '娘', '娛', '娜', '娥', '婆', '婕', '婚', '婦', '婷', '媒', '媚', '媽', '嫁', '嫂', '嫩', '嬌', '嬰', '子', '孔', '孕', '字', '存', '孝', '季', '学', '孩', '孫', '學', '宅', '宇', '守', '安', '宋', '完', '宏', '宗', '官', '宙', '定', '宜', '宝', '客', '宣', '室', '宥', '宮', '宴', '宵', '家', '宸', '容', '宿', '寄', '密', '富', '寒', '寓', '察', '寢', '實', '寧', '寫', '寬', '寮', '寰', '寵', '寶', '寺', '寿', '封', '射', '將', '專', '尊', '尋', '對', '導', '小', '少', '尖', '尚', '就', '尺', '尼', '尾', '尿', '局', '居', '屈', '屋', '屏', '展', '層', '屬', '山', '岐', '岡', '岩', '岳', '岸', '峰', '島', '峽', '崇', '崎', '崗', '崧', '嵐', '嶺', '嶼', '川', '州', '巢', '工', '左', '巧', '巨', '己', '已', '巴', '巷', '巾', '市', '布', '帆', '希', '帖', '帝', '帥', '師', '席', '帳', '帶', '常', '帽', '幕', '幣', '幫', '干', '平', '年', '幸', '幻', '幼', '庄', '床', '序', '底', '店', '庚', '府', '度', '座', '庫', '庭', '康', '廂', '廈', '廉', '廊', '廖', '廚', '廟', '廠', '廢', '廣', '廬', '廳', '延', '廷', '建', '弄', '式', '弓', '引', '弘', '弟', '張', '強', '彈', '彌', '形', '彥', '彩', '彫', '彭', '彰', '影', '彼', '往', '待', '很', '律', '後', '徐', '徒', '得', '從', '御', '復', '循', '微', '徵', '德', '心', '必', '忌', '志', '忙', '忠', '快', '念', '思', '怡', '急', '性', '怪', '恆', '恒', '恩', '恭', '息', '悅', '悠', '悦', '您', '情', '惟', '惠', '惡', '想', '意', '愛', '感', '慈', '態', '慕', '慢', '慧', '慶', '憲', '應', '懶', '懷', '戀', '成', '我', '戒', '或', '戰', '戲', '戴', '戶', '房', '所', '扁', '扇', '手', '才', '打', '托', '扭', '批', '找', '承', '技', '抄', '把', '抓', '投', '抗', '折', '披', '抹', '抽', '担', '拆', '拉', '拋', '拌', '拍', '拓', '拔', '拖', '招', '拜', '拳', '拷', '拼', '拾', '拿', '持', '指', '按', '挑', '振', '挽', '捏', '捐', '捲', '捷', '掃', '授', '掌', '排', '採', '探', '接', '控', '推', '描', '提', '插', '揚', '換', '握', '揭', '援', '損', '搖', '搜', '搬', '搭', '摩', '撈', '撒', '撞', '撥', '播', '擂', '擇', '擊', '操', '擎', '擴', '攜', '攝', '攤', '支', '收', '改', '放', '政', '故', '效', '敏', '救', '教', '散', '敦', '敬', '敲', '整', '數', '文', '斐', '斑', '斗', '料', '斯', '新', '斷', '方', '於', '施', '旁', '旅', '旋', '族', '旗', '日', '旦', '早', '旭', '旺', '昇', '昌', '明', '易', '昔', '昕', '星', '映', '春', '昭', '是', '昱', '時', '晉', '晚', '晟', '晨', '普', '景', '晴', '晶', '智', '暉', '暖', '暘', '暢', '曉', '曜', '曦', '曲', '更', '書', '曼', '曾', '最', '會', '月', '有', '朋', '服', '朗', '望', '朝', '期', '木', '未', '末', '本', '朱', '朵', '杉', '李', '杏', '材', '村', '杜', '杞', '束', '杯', '杰', '東', '松', '板', '析', '枕', '林', '果', '枝', '架', '柏', '柒', '染', '柔', '柚', '查', '柯', '柳', '柴', '栗', '校', '核', '根', '格', '栽', '桂', '桃', '框', '案', '桌', '桐', '桑', '桔', '桶', '梁', '梅', '條', '梨', '梭', '梯', '械', '梵', '棄', '棉', '棋', '棒', '棟', '棠', '棧', '森', '椅', '植', '椒', '椰', '楊', '楓', '業', '極', '楽', '概', '榔', '榕', '榛', '榜', '榨', '榭', '榮', '構', '槍', '樂', '樓', '標', '模', '樣', '樸', '樹', '樺', '樽', '橋', '橘', '橙', '機', '橡', '橫', '檀', '檜', '檢', '檬', '檯', '檳', '檸', '櫃', '櫥', '櫻', '權', '次', '欣', '款', '歆', '歌', '歐', '歡', '止', '正', '此', '步', '武', '歲', '歸', '殊', '段', '殺', '殼', '殿', '毅', '母', '每', '毒', '比', '毛', '毯', '氏', '民', '氣', '氧', '水', '永', '汁', '求', '汎', '汕', '汗', '江', '池', '污', '汪', '汶', '決', '汽', '沃', '沅', '沉', '沏', '沐', '沒', '沖', '沙', '沛', '沫', '河', '油', '治', '泉', '泌', '泓', '法', '泡', '波', '泥', '注', '泰', '泳', '泵', '洋', '洗', '洛', '洞', '津', '洪', '洱', '洲', '活', '洽', '派', '流', '浦', '浩', '浪', '浮', '浴', '海', '消', '涎', '涮', '液', '涵', '涼', '淇', '淋', '淑', '淘', '淡', '淨', '深', '淳', '淺', '添', '清', '減', '渡', '測', '港', '渴', '游', '湖', '湘', '湯', '湾', '源', '準', '溢', '溪', '溫', '滋', '滑', '滴', '滷', '滾', '滿', '漁', '漂', '漆', '漏', '演', '漢', '漫', '漾', '漿', '潔', '潛', '潢', '潤', '潭', '潮', '澄', '澎', '澡', '澤', '澳', '濃', '濕', '濟', '濰', '濱', '瀚', '灘', '灣', '火', '灰', '灶', '灸', '炎', '炒', '炙', '炫', '炭', '炸', '為', '烈', '烏', '烘', '烤', '烹', '焊', '焗', '焙', '無', '焢', '焦', '然', '焿', '煉', '煌', '煎', '煙', '煤', '照', '煮', '煲', '熊', '熟', '熬', '熱', '燈', '燉', '燒', '燕', '燙', '營', '燥', '燦', '燭', '燴', '燻', '爆', '爌', '爐', '爪', '爭', '爵', '父', '爸', '爹', '爺', '爽', '爾', '牆', '片', '版', '牌', '牙', '牛', '牧', '物', '特', '犬', '狀', '狂', '狗', '狠', '猛', '猴', '獅', '獎', '獨', '獲', '獸', '獻', '玄', '率', '玉', '王', '玖', '玩', '玫', '玲', '玻', '珈', '珊', '珍', '珠', '班', '現', '球', '理', '琦', '琪', '琲', '琳', '琴', '瑋', '瑚', '瑜', '瑞', '瑟', '瑤', '瑩', '瑪', '瑰', '瑾', '璃', '璇', '璉', '璜', '璞', '環', '璽', '瓏', '瓜', '瓦', '瓶', '瓷', '甕', '甘', '甜', '生', '產', '用', '田', '由', '甲', '申', '男', '甸', '町', '界', '留', '畢', '番', '畫', '異', '當', '疆', '疙', '疫', '疼', '疾', '病', '症', '痘', '痛', '痠', '痧', '瘋', '瘦', '瘩', '療', '癌', '癒', '癮', '登', '發', '白', '百', '的', '皆', '皇', '皮', '盅', '盆', '盈', '益', '盒', '盛', '盟', '盡', '監', '盤', '盧', '目', '直', '相', '省', '眉', '看', '真', '眠', '眷', '眼', '眾', '睡', '督', '睫', '睿', '瞳', '知', '短', '矯', '石', '砂', '研', '破', '硬', '硯', '碁', '碑', '碗', '碟', '碧', '碩', '碳', '確', '碼', '磁', '磅', '磚', '磨', '礎', '礙', '礦', '示', '社', '祈', '祐', '祖', '祝', '神', '祥', '票', '祺', '祿', '禁', '禎', '福', '禧', '禪', '禮', '禹', '禾', '秀', '私', '秉', '秋', '科', '秒', '秘', '租', '秤', '移', '稅', '程', '種', '稻', '穀', '穌', '積', '穎', '穗', '究', '空', '穿', '窈', '窕', '窗', '窩', '窯', '立', '站', '章', '童', '端', '競', '竹', '笑', '第', '筆', '等', '筋', '筌', '筍', '筒', '策', '筵', '箋', '算', '管', '箱', '節', '範', '篇', '築', '篩', '簡', '簧', '簽', '簾', '籃', '籍', '籠', '米', '籽', '粄', '粉', '粑', '粒', '粗', '粥', '粧', '粵', '粽', '精', '粿', '糕', '糖', '糧', '糬', '糰', '系', '紀', '約', '紅', '紋', '納', '紐', '紓', '純', '紗', '紙', '級', '素', '紡', '索', '紫', '細', '紳', '紹', '終', '組', '結', '絕', '絡', '給', '統', '絲', '經', '綜', '綠', '維', '綱', '網', '綵', '綸', '綺', '綿', '緊', '緑', '線', '緣', '編', '緬', '緯', '練', '緹', '緻', '縣', '縫', '縮', '總', '織', '繕', '繡', '繪', '繳', '繼', '續', '纖', '罐', '罩', '置', '罰', '署', '羅', '羊', '美', '群', '義', '羹', '羽', '羿', '翁', '翅', '翊', '翎', '習', '翔', '翠', '翡', '翰', '翻', '翼', '耀', '老', '考', '者', '而', '耐', '耕', '耳', '耶', '聖', '聚', '聞', '聯', '聰', '聲', '職', '聽', '肉', '肌', '肚', '肝', '股', '肢', '肥', '肩', '肯', '育', '胃', '背', '胎', '胖', '胡', '胤', '胸', '能', '脂', '脆', '脚', '脫', '腊', '腎', '腐', '腔', '腦', '腰', '腳', '腸', '腹', '腿', '膚', '膜', '膝', '膠', '膩', '膳', '膽', '臉', '臘', '臟', '臣', '臥', '臨', '自', '臭', '至', '致', '臺', '臻', '與', '興', '舉', '舊', '舌', '舍', '舒', '舖', '舘', '舞', '航', '般', '舶', '船', '舺', '艇', '艋', '艦', '良', '色', '艾', '芋', '芒', '芙', '芝', '芬', '芭', '芮', '芯', '花', '芳', '芽', '苑', '苓', '苔', '苗', '若', '苦', '英', '茂', '茄', '茅', '茉', '茗', '茱', '茶', '草', '荳', '荷', '莉', '莊', '莎', '莒', '莓', '莫', '菁', '菇', '菈', '菊', '菌', '菓', '菜', '菠', '菩', '華', '菱', '菲', '菸', '萃', '萄', '萊', '萬', '萱', '落', '葉', '著', '葛', '葡', '董', '葱', '葳', '葵', '蒂', '蒔', '蒙', '蒜', '蒞', '蒸', '蓁', '蓄', '蓉', '蓋', '蓬', '蓮', '蔓', '蔔', '蔗', '蔘', '蔡', '蔣', '蔥', '蔬', '蕃', '蕉', '蕭', '蕾', '薄', '薇', '薏', '薑', '薦', '薩', '薪', '薬', '薯', '藍', '藏', '藝', '藤', '藥', '蘆', '蘇', '蘋', '蘭', '蘿', '虎', '處', '號', '虱', '虹', '蚵', '蛋', '蛤', '蜀', '蜂', '蜜', '蝦', '蝶', '融', '螢', '螺', '蟹', '蠔', '蠟', '蠶', '血', '行', '術', '街', '衛', '衡', '衣', '表', '衫', '袋', '被', '裏', '裕', '補', '裝', '裡', '製', '複', '褲', '襪', '襯', '西', '要', '見', '規', '覓', '視', '親', '覺', '覽', '觀', '角', '解', '觸', '言', '訂', '計', '訊', '訓', '託', '記', '訪', '設', '許', '診', '註', '証', '評', '詠', '詢', '試', '詩', '詮', '話', '詹', '誌', '認', '誕', '語', '誠', '說', '誰', '課', '誼', '調', '請', '論', '諦', '諮', '諾', '謙', '講', '謝', '證', '識', '警', '議', '護', '譽', '讀', '變', '讓', '讚', '谷', '豆', '豐', '豚', '象', '豪', '豬', '貓', '貝', '貞', '負', '財', '貢', '貨', '販', '責', '貳', '貴', '買', '貸', '費', '貼', '貿', '賀', '賃', '資', '賓', '賞', '賢', '賣', '質', '賴', '購', '賽', '贈', '贊', '赤', '赫', '走', '起', '超', '越', '趙', '趣', '足', '趴', '跆', '跌', '跑', '距', '跨', '路', '跳', '踏', '蹈', '蹟', '躍', '身', '車', '軋', '軍', '軒', '軟', '載', '輔', '輕', '輛', '輝', '輪', '輸', '轉', '辛', '辣', '辦', '辰', '農', '迎', '近', '迪', '迷', '追', '退', '送', '透', '逗', '這', '通', '速', '造', '逢', '連', '週', '進', '逸', '遇', '遊', '運', '過', '道', '達', '違', '遙', '遠', '遣', '適', '選', '邀', '邁', '還', '邊', '邑', '那', '邦', '邱', '邸', '郎', '部', '郭', '郵', '都', '鄉', '鄧', '鄭', '鄰', '酉', '酌', '配', '酒', '酥', '酪', '酵', '酷', '酸', '醇', '醉', '醋', '醫', '醬', '釀', '采', '釋', '里', '重', '野', '量', '金', '針', '釣', '鈑', '鈴', '鈺', '鉄', '鉅', '鉑', '銀', '銅', '銓', '銘', '銳', '銷', '鋁', '鋒', '鋪', '鋼', '錄', '錢', '錦', '錫', '錶', '鍊', '鍋', '鍍', '鍵', '鍾', '鎖', '鎮', '鎰', '鏈', '鏡', '鐘', '鐵', '鑄', '鑑', '鑫', '鑲', '鑽', '長', '門', '閃', '閉', '開', '閒', '間', '閣', '閱', '闆', '關', '阪', '防', '阿', '陀', '附', '限', '陞', '院', '除', '陪', '陰', '陳', '陵', '陶', '陸', '陽', '隆', '隊', '階', '隔', '際', '障', '隨', '險', '隱', '隻', '雀', '雄', '雅', '集', '雕', '雙', '雜', '雞', '離', '難', '雨', '雪', '雲', '零', '雷', '電', '需', '震', '霖', '霜', '霞', '霧', '露', '霸', '靈', '靑', '青', '靖', '靚', '靜', '非', '靠', '面', '鞋', '韋', '韓', '音', '韻', '響', '頁', '頂', '項', '順', '頌', '預', '頒', '頓', '領', '頤', '頭', '頸', '頻', '顆', '題', '額', '顎', '顏', '願', '類', '顧', '風', '飄', '飛', '食', '飩', '飯', '飲', '飼', '飽', '飾', '餃', '餅', '養', '餐', '餓', '餘', '餛', '餡', '館', '饅', '饋', '饌', '饕', '饗', '首', '香', '馥', '馨', '馬', '駁', '駐', '駕', '駛', '駿', '騎', '騏', '騰', '驗', '驚', '骨', '體', '高', '髮', '鬆', '鬍', '鬚', '鬥', '鬼', '魂', '魏', '魔', '魚', '魠', '魯', '魷', '鮑', '鮮', '鯛', '鯨', '鰻', '鱈', '鱔', '鱻', '鳥', '鳳', '鴛', '鴦', '鴨', '鴻', '鵝', '鵬', '鶴', '鷄', '鹹', '鹽', '鹿', '麒', '麗', '麟', '麥', '麩', '麵', '麻', '黃', '黎', '黑', '黛', '點', '鼎', '鼓', '鼠', '鼻', '齊', '齋', '齒', '齡', '龍', '龐', '龜']

fix = ['a-','b-','c-','d-','e-','f-','g-','h-','i-','j-','k-','l-','m-','n-','o-','p-','q-','r-','s-','t-','u-','v-','w-','x-','y-','z-']

def test(cls_list, net):

    al = 0
    ans = ""
    after = "00001"
    all_ans = []
    for i in os.listdir("outF/"):
        
        al += 1
        
        img = image.load_img( "outF/" + i, target_size=(75, 75))
        
        if img is None:
            continue
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis = 0)
        pred = net.predict(x)[0]
        top_inds = pred.argsort()[::-1][:3]

        
        if cls_list[top_inds[0]] in fix:    
            cls_list[top_inds[0]] = cls_list[top_inds[0]][:1]

        quiz = i[:5]

        if (quiz == after):
            ans += cls_list[top_inds[0]]
        else:
            
            all_ans.append(ans)
            ans = cls_list[top_inds[0]] 
           
                
        after = quiz
        
    all_ans.append(ans)
    pd.DataFrame.to_csv(pd.DataFrame(all_ans), "outF_IE_46-2.csv", header=False, index=False)


    
# 影像大小
IMAGE_SIZE = (75, 75)

# 影像類別數
NUM_CLASSES = 2277

# 凍結網路層數
FREEZE_LAYERS = 2

start = 2
#類別載入
cls_list = clss
#print(cls_list)
#模組載入

net = tf.keras.applications.InceptionResNetV2(include_top=False, weights='imagenet', input_tensor=None,
               input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3))
x = net.output
x = Flatten()(x)

# 增加 DropOut layer
x = Dropout(0.5)(x)

# 增加 Dense layer，以 softmax 產生個類別的機率值
output_layer = Dense(NUM_CLASSES , activation='softmax', name='softmax')(x)

# 設定凍結與要進行訓練的網路層
net_final = Model(inputs=net.input, outputs=output_layer)
for layer in net_final.layers[:FREEZE_LAYERS]:
    layer.trainable = False
for layer in net_final.layers[FREEZE_LAYERS:]:
    layer.trainable = True
    
# 請自行改變路徑
net_final.load_weights('D:/場景文字辨識/高階賽/Model/model-InceptionResnetV2-e46-2.h5')
test(cls_list, net_final)



