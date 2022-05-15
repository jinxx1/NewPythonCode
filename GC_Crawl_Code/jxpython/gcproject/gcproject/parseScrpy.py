# -*- coding: utf-8 -*-


def get_location(strword,how=0):
    import cpca

    item = {}

    if not isinstance(strword,str):
        return ''
    # if len(strword) > 20:
    #     print(strword)
    if strword and '三台' in strword:
        item['Project_province'] = '四川省'
        item['Project_country'] = '绵阳市'
        item['Project_district'] = '三台县'



    elif strword and '济源' in strword:
        item['Project_province'] = '河南省'
        item['Project_country'] = '济源市'
        item['Project_district'] = ''

    elif strword and '鄂尔多斯' in strword:
        item['Project_province'] = '内蒙古自治区'
        item['Project_country'] = '鄂尔多斯市'
        item['Project_district'] = ''
    elif strword and '兴安' in strword:
        item['Project_province'] = '内蒙古自治区'
        item['Project_country'] = '兴安盟'
        item['Project_district'] = ''
    elif strword and '通辽' in strword:
        item['Project_province'] = '内蒙古自治区'
        item['Project_country'] = '通辽市'
        item['Project_district'] = ''
    elif strword and '赤峰' in strword:
        item['Project_province'] = '内蒙古自治区'
        item['Project_country'] = '赤峰市'
        item['Project_district'] = ''
    elif strword and '呼伦贝尔' in strword:
        item['Project_province'] = '内蒙古自治区'
        item['Project_country'] = '呼伦贝尔市'
        item['Project_district'] = ''
    elif strword and '扎噜特' in strword or '扎鲁特' in strword:
        item['Project_province'] = '内蒙古自治区'
        item['Project_country'] = '扎噜特部'
        item['Project_district'] = ''
    elif strword and '石河子' in strword:
        item['Project_province'] = '新疆维吾尔自治区'
        item['Project_country'] = '石河子县级市'
        item['Project_district'] = ''
    elif strword and '甘孜' in strword:
        item['Project_province'] = '四川省'
        item['Project_country'] = '甘孜藏族自治州'
        item['Project_district'] = ''
    elif strword and '南充' in strword:
        item['Project_province'] = '四川省'
        item['Project_country'] = '南充县级市'
        item['Project_district'] = ''
    elif strword and '凉山' in strword:
        item['Project_province'] = '四川省'
        item['Project_country'] = '凉山彝族自治州'
        item['Project_district'] = ''
    elif strword and '阿坝' in strword:
        item['Project_province'] = '四川省'
        item['Project_country'] = '阿坝藏族羌族自治州'
        item['Project_district'] = ''
    elif strword and '上海市浦东新区金桥镇' in strword:
        item['Project_province'] = '上海市'
        item['Project_country'] = '浦东新区'
        item['Project_district'] = '金桥镇'
    elif strword and '平潭' in strword:
        item['Project_province'] = '福建省'
        item['Project_country'] = '平潭县级市'
        item['Project_district'] = ''
    elif strword and '荔波' in strword:
        item['Project_province'] = '贵州省'
        item['Project_country'] = '布依族苗族自治州'
        item['Project_district'] = '荔波县'
    elif strword and '甘南' in strword:
        item['Project_province'] = '甘肃省'
        item['Project_country'] = '甘南藏族自治州'
        item['Project_district'] = ''
    elif strword and '崆峒' in strword:
        item['Project_province'] = '甘肃省'
        item['Project_country'] = '平凉市'
        item['Project_district'] = '崆峒山'
    elif strword and '武都' in strword:
        item['Project_province'] = '甘肃省'
        item['Project_country'] = '陇南市'
        item['Project_district'] = '武都区'
    elif strword and '博州' in strword:
        item['Project_province'] = '新疆维吾尔自治区'
        item['Project_country'] = '博尔塔拉蒙古自治州'
        item['Project_district'] = ''
    elif strword and '海西' in strword:
        item['Project_province'] = '青海省'
        item['Project_country'] = '海西蒙古族藏族自治州'
        item['Project_district'] = ''
    elif strword and '贵安' in strword:
        item['Project_province'] = '贵州省'
        item['Project_country'] = '贵安新区'
        item['Project_district'] = ''
    elif strword and '宝应' in strword:
        item['Project_province'] = '江苏省'
        item['Project_country'] = '扬州市'
        item['Project_district'] = '宝应区'
    elif strword and '南宁' in strword:
        item['Project_province'] = '广西壮族自治区'
        item['Project_country'] = '南宁市'
        item['Project_district'] = ''
    elif strword and '梅县' in strword:
        item['Project_province'] = '广东省'
        item['Project_country'] = '梅州市'
        item['Project_district'] = '梅县区'
    elif strword and '增城' in strword:
        item['Project_province'] = '广东省'
        item['Project_country'] = '广州市'
        item['Project_district'] = '增城区'
    elif strword and '深圳' in strword:
        item['Project_province'] = '广东省'
        item['Project_country'] = '深圳市'
        item['Project_district'] = ''
    elif strword and '红河' in strword:
        item['Project_province'] = '云南省'
        item['Project_country'] = '红河哈尼族彝族自治州'
        item['Project_district'] = ''
    elif strword and '中山' in strword:
        item['Project_province'] = '广东省'
        item['Project_country'] = '中山市'
        item['Project_district'] = ''
    elif strword and '象山' in strword:
        item['Project_province'] = '浙江省'
        item['Project_country'] = '宁波市'
        item['Project_district'] = '象山县'
    elif strword and '鄞州' in strword:
        item['Project_province'] = '浙江省'
        item['Project_country'] = '宁波市'
        item['Project_district'] = '鄞州县'
    elif strword and '山西晋中' in strword:
        item['Project_province'] = '山西省'
        item['Project_country'] = '晋中市'
        item['Project_district'] = ''
    elif strword and '西藏阿里' in strword:
        item['Project_province'] = '西藏自治区'
        item['Project_country'] = '阿里地区'
        item['Project_district'] = ''
    elif strword and '新疆省' in strword:
        item['Project_province'] = '新疆维吾尔自治区'
        item['Project_country'] = ''
        item['Project_district'] = ''

    elif strword and '内蒙' in strword:
        item['Project_province'] = '内蒙古自治区'
        item['Project_country'] = ''
        item['Project_district'] = ''

    elif strword and '云南昆明' in strword:
        item['Project_province'] = '云南省'
        item['Project_country'] = '昆明市'
        item['Project_district'] = ''

    elif strword and '新疆伊犁' in strword:
        item['Project_province'] = '新疆维吾尔自治区'
        item['Project_country'] = '伊犁市'
        item['Project_district'] = ''

    elif strword and '福建厦门' in strword:
        item['Project_province'] = '福建省'
        item['Project_country'] = '厦门市'
        item['Project_district'] = ''

    elif strword and '奉节' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '重庆市'
        item['Project_district'] = '奉节县'

    elif strword and '闵行' in strword:
        item['Project_province'] = '上海市'
        item['Project_country'] = '上海市'
        item['Project_district'] = '闵行区'

    elif strword and '徐汇' in strword:
        item['Project_province'] = '上海市'
        item['Project_country'] = '上海市'
        item['Project_district'] = '徐汇区'

    elif strword and '杨浦' in strword:
        item['Project_province'] = '上海市'
        item['Project_country'] = '上海市'
        item['Project_district'] = '杨浦区'

    elif strword and '浦东' in strword:
        item['Project_province'] = '上海市'
        item['Project_country'] = '上海市'
        item['Project_district'] = '浦东区'

    elif strword and '宝山' in strword:
        item['Project_province'] = '上海市'
        item['Project_country'] = '上海市'
        item['Project_district'] = '宝山区'

    elif strword and '六库' in strword:
        item['Project_province'] = '云南省'
        item['Project_country'] = '怒江傈僳族自治州'
        item['Project_district'] = '六库镇'

    elif strword and '怒江' in strword:
        item['Project_province'] = '云南省'
        item['Project_country'] = '怒江傈僳族自治州'
        item['Project_district'] = ''

    elif strword and '铜仁' in strword:
        item['Project_province'] = '贵州省'
        item['Project_country'] = '铜仁市'
        item['Project_district'] = ''

    elif strword and '天门' in strword:
        item['Project_province'] = '湖北省'
        item['Project_country'] = '天门市'
        item['Project_district'] = ''

    elif strword and '那曲' in strword:
        item['Project_province'] = '西藏自治区'
        item['Project_country'] = '那曲市'
        item['Project_district'] = ''

    elif strword and '雄安' in strword:
        item['Project_province'] = '河北省'
        item['Project_country'] = '雄安新区'
        item['Project_district'] = ''

    elif strword and '荷泽' in strword:
        item['Project_province'] = '山东省'
        item['Project_country'] = '荷泽市'
        item['Project_district'] = ''

    elif strword and '海南州' in strword:
        item['Project_province'] = '青海省'
        item['Project_country'] = '海南藏族自治州'
        item['Project_district'] = ''

    elif strword and '海北州' in strword:
        item['Project_province'] = '青海省'
        item['Project_country'] = '海北藏族自治州'
        item['Project_district'] = ''

    elif strword and '大兴安岭' in strword:
        item['Project_province'] = '黑龙江省'
        item['Project_country'] = '大兴安岭地区'
        item['Project_district'] = ''

    elif strword and '伊犁' in strword:
        item['Project_province'] = '新疆维吾尔自治区'
        item['Project_country'] = '伊犁哈萨克自治州'
        item['Project_district'] = ''

    elif strword and '巴州' in strword:
        item['Project_province'] = '新疆维吾尔自治区'
        item['Project_country'] = '巴音郭楞蒙古自治州'
        item['Project_district'] = ''

    elif strword and '天府' in strword:
        item['Project_province'] = '四川省'
        item['Project_country'] = '天府新区'
        item['Project_district'] = ''

    elif strword and '锡林郭勒' in strword:
        item['Project_province'] = '内蒙古自治区'
        item['Project_country'] = '锡林郭勒盟'
        item['Project_district'] = ''

    elif strword and '阿拉善' in strword:
        item['Project_province'] = '内蒙古自治区'
        item['Project_country'] = '阿拉善盟'
        item['Project_district'] = ''

    elif strword and '桔山' in strword:
        item['Project_province'] = '贵州省'
        item['Project_country'] = '兴义市'
        item['Project_district'] = '桔山新区'

    elif strword and '万宁' in strword:
        item['Project_province'] = '海南省'
        item['Project_country'] = '万宁市'
        item['Project_district'] = ''

    elif strword and '乐东' in strword:
        item['Project_province'] = '海南省'
        item['Project_country'] = '乐东黎族自治县'
        item['Project_district'] = ''

    elif strword and '文昌' in strword:
        item['Project_province'] = '海南省'
        item['Project_country'] = '文昌市'
        item['Project_district'] = ''

    elif strword and '临高' in strword:
        item['Project_province'] = '海南省'
        item['Project_country'] = '临高直辖县'
        item['Project_district'] = '临高县'

    elif strword and '陵水' in strword:
        item['Project_province'] = '海南省'
        item['Project_country'] = '陵水黎族自治县'
        item['Project_district'] = ''

    elif strword and '黔南' in strword:
        item['Project_province'] = '贵州省'
        item['Project_country'] = '黔南布依族苗族自治州'
        item['Project_district'] = ''

    elif strword and '黔东南' in strword or '黔东' in strword:
        item['Project_province'] = '贵州省'
        item['Project_country'] = '黔东南苗族侗族自治州'
        item['Project_district'] = ''

    elif strword and '迪庆' in strword:
        item['Project_province'] = '云南省'
        item['Project_country'] = '迪庆藏族自治州'
        item['Project_district'] = ''

    elif strword and '奎山' in strword:
        item['Project_province'] = '江苏省'
        item['Project_country'] = '徐州市'
        item['Project_district'] = '泉山区奎山街道'

    elif strword and '稀土高新区' in strword:
        item['Project_province'] = '内蒙古自治区'
        item['Project_country'] = '包头市'
        item['Project_district'] = '稀土高新技术产业开发区'

    elif strword and '琼海' in strword:
        item['Project_province'] = '海南省'
        item['Project_country'] = '琼海市'
        item['Project_district'] = ''

    elif strword and '定安' in strword:
        item['Project_province'] = '海南省'
        item['Project_country'] = '定安直辖县'
        item['Project_district'] = ''

    elif strword and '保亭' in strword:
        item['Project_province'] = '海南省'
        item['Project_country'] = '保亭黎族苗族自治县'
        item['Project_district'] = ''

    elif strword and '五指山' in strword:
        item['Project_province'] = '海南省'
        item['Project_country'] = '五指山市'
        item['Project_district'] = ''

    elif strword and '恰卜恰' in strword:
        item['Project_province'] = '青海省'
        item['Project_country'] = '海南藏族自治州'
        item['Project_district'] = '恰卜恰镇'

    elif strword and '东方' in strword:
        item['Project_province'] = '海南省'
        item['Project_country'] = '东方'
        item['Project_district'] = ''

    elif strword and '天鹅县' in strword:
        item['Project_province'] = '广西壮族自治区'
        item['Project_country'] = '河池市'
        item['Project_district'] = '天鹅县'

    elif strword and '巴马' in strword:
        item['Project_province'] = '广西壮族自治区'
        item['Project_country'] = '河池市'
        item['Project_district'] = '巴马瑶族自治县'

    elif strword and '大化' in strword:
        item['Project_province'] = '广西壮族自治区'
        item['Project_country'] = '河池市'
        item['Project_district'] = '大化瑶族自治县'

    elif strword and '果洛' in strword:
        item['Project_province'] = '青海省'
        item['Project_country'] = '果洛藏族自治州'
        item['Project_district'] = ''

    elif strword and '海北' in strword:
        item['Project_province'] = '青海省'
        item['Project_country'] = '海北藏族自治州'
        item['Project_district'] = ''

    elif strword and '克州' in strword:
        item['Project_province'] = '新疆维吾尔自治区'
        item['Project_country'] = '克孜勒苏柯尔克孜自治州'
        item['Project_district'] = ''

    elif strword and '西双版纳' in strword:
        item['Project_province'] = '云南省'
        item['Project_country'] = '西双版纳傣族自治州'
        item['Project_district'] = ''

    elif strword and '琼中' in strword:
        item['Project_province'] = '海南省'
        item['Project_country'] = '琼中黎族苗族自治县'
        item['Project_district'] = ''

    elif strword and '昌江' in strword:
        item['Project_province'] = '海南省'
        item['Project_country'] = '昌江黎族自治县'
        item['Project_district'] = ''

    elif strword and '潜江' in strword:
        item['Project_province'] = '湖北省'
        item['Project_country'] = '潜江直管县'
        item['Project_district'] = ''

    elif strword and '仙桃' in strword:
        item['Project_province'] = '湖北省'
        item['Project_country'] = '仙桃市'
        item['Project_district'] = ''

    elif strword and '德宏' in strword:
        item['Project_province'] = '云南省'
        item['Project_country'] = '德宏傣族景颇族自治州'
        item['Project_district'] = ''

    elif strword and '东辽' in strword:
        item['Project_province'] = '吉林省'
        item['Project_country'] = '辽源市'
        item['Project_district'] = '东辽县'

    elif strword and '临安' in strword:
        item['Project_province'] = '浙江省'
        item['Project_country'] = '杭州市'
        item['Project_district'] = '临安区'

    elif strword and '通州' in strword:
        item['Project_province'] = '北京市'
        item['Project_country'] = '北京市'
        item['Project_district'] = '通州区'

    elif strword and '湘西' in strword:
        item['Project_province'] = '湖南省'
        item['Project_country'] = '湘西土家族苗族自治州'
        item['Project_district'] = ''

    elif strword and '澄迈' in strword:
        item['Project_province'] = '海南省'
        item['Project_country'] = '澄迈直辖县'
        item['Project_district'] = ''

    elif strword and '崇明' in strword:
        item['Project_province'] = '上海市'
        item['Project_country'] = '上海市'
        item['Project_district'] = '崇明区'

    elif strword and '密云' in strword:
        item['Project_province'] = '北京市'
        item['Project_country'] = '北京市'
        item['Project_district'] = '密云区'

    elif strword and '塘沽' in strword:
        item['Project_province'] = '天津市'
        item['Project_country'] = '天津市'
        item['Project_district'] = '塘沽区'

    elif strword and '静海' in strword:
        item['Project_province'] = '天津市'
        item['Project_country'] = '天津市'
        item['Project_district'] = '静海区'

    elif strword and '延边' in strword:
        item['Project_province'] = '吉林省'
        item['Project_country'] = '延边朝鲜族自治州'
        item['Project_district'] = ''

    elif strword and '潍城' in strword:
        item['Project_province'] = '山东省'
        item['Project_country'] = '潍坊市'
        item['Project_district'] = '潍城县'

    elif strword and '璧山' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '重庆市'
        item['Project_district'] = '璧山县'
    elif strword and '江津' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '重庆市'
        item['Project_district'] = '江津区'

    elif strword and '延庆' in strword:
        item['Project_province'] = '北京市'
        item['Project_country'] = '北京市'
        item['Project_district'] = '延庆区'


    elif strword and '白沙' in strword:
        item['Project_province'] = '海南省'
        item['Project_country'] = '白沙黎族自治县'
        item['Project_district'] = ''

    elif strword and '渝北' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '重庆市'
        item['Project_district'] = '渝北区'

    elif strword and '江北' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '重庆市'
        item['Project_district'] = '江北区'

    elif strword and '神农架' in strword:
        item['Project_province'] = '湖北省'
        item['Project_country'] = '神农架林区'
        item['Project_district'] = '神农架林区'


    elif strword and '人民北路' in strword:
        item['Project_province'] = '广东省'
        item['Project_country'] = '广州市'
        item['Project_district'] = ''

    elif strword and '荣昌' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '重庆市'
        item['Project_district'] = '荣昌县'

    elif strword and '合川' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '重庆市'
        item['Project_district'] = '合川区'

    elif strword and '大足' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '重庆市'
        item['Project_district'] = '大足区'

    elif strword and '辽河源' in strword:
        item['Project_province'] = '吉林省'
        item['Project_country'] = '东辽县'
        item['Project_district'] = '辽河源'

    elif strword and '南京路' in strword:
        item['Project_province'] = '上海市'
        item['Project_country'] = '上海市'
        item['Project_district'] = '和平区'

    elif strword and '和平区' in strword:
        item['Project_province'] = '上海市'
        item['Project_country'] = '上海市'
        item['Project_district'] = '和平区'

    elif strword and '铜梁' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '重庆市'
        item['Project_district'] = '铜梁区'

    elif strword and '彭水' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '彭水苗族土家族自治县'
        item['Project_district'] = '彭水苗族土家族自治县'

    elif strword and '梁平' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '重庆市'
        item['Project_district'] = '梁平区'

    elif strword and '潼南' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '重庆市'
        item['Project_district'] = '潼南县'

    elif strword and '蓟州' in strword:
        item['Project_province'] = '天津市'
        item['Project_country'] = '天津市'
        item['Project_district'] = '蓟州区'

    elif strword and '大理' in strword:
        item['Project_province'] = '云南省'
        item['Project_country'] = '大理白族自治州'
        item['Project_district'] = '大理白族自治州'

    elif strword and '文山' in strword:
        item['Project_province'] = '云南省'
        item['Project_country'] = '文山壮族苗族自治州'
        item['Project_district'] = '文山壮族苗族自治州'

    elif strword and '酉阳' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '酉阳土家族苗族自治县'
        item['Project_district'] = '酉阳土家族苗族自治县'

    elif strword and '武隆' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '重庆市'
        item['Project_district'] = '武隆区'

    elif strword and '丰都' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '重庆市'
        item['Project_district'] = '丰都县'

    elif strword and '万州' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '重庆市'
        item['Project_district'] = '万州区'

    elif strword and '沙坪坝' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '重庆市'
        item['Project_district'] = '沙坪坝区'

    elif strword and '綦江' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '重庆市'
        item['Project_district'] = '綦江区'

    elif strword and '开县' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '重庆市'
        item['Project_district'] = '开州区'

    elif strword and '北碚' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '重庆市'
        item['Project_district'] = '北碚区'

    elif strword and '石柱' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '石柱土家族自治县'
        item['Project_district'] = '石柱土家族自治县'

    elif strword and '哈平' in strword:
        item['Project_province'] = '黑龙江省'
        item['Project_country'] = '哈尔滨市'
        item['Project_district'] = '动力区'

    elif strword and '秀山' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '秀山土家族苗族自治县'
        item['Project_district'] = '秀山土家族苗族自治县'

    elif strword and '万盛区' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '重庆市'
        item['Project_district'] = '万盛经济技术开发区'

    elif strword and '南川' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '重庆市'
        item['Project_district'] = '南川区'

    elif strword and '屯昌' in strword:
        item['Project_province'] = '海南省'
        item['Project_country'] = '屯昌直辖县'
        item['Project_district'] = '屯昌直辖县'

    elif strword and '汉沽' in strword:
        item['Project_province'] = '天津市'
        item['Project_country'] = '天津市'
        item['Project_district'] = '汉沽区'


    elif strword and '宝坻' in strword:
        item['Project_province'] = '天津市'
        item['Project_country'] = '天津市'
        item['Project_district'] = '宝坻县'


    elif strword and '高新区' in strword:
        item['Project_province'] = '四川省'
        item['Project_country'] = '成都市'
        item['Project_district'] = '高新技术产业开发区'


    elif strword and '阳光花苑' in strword:
        item['Project_province'] = '新疆维吾尔自治区'
        item['Project_country'] = '乌鲁木齐市'
        item['Project_district'] = '天山区'


    elif strword and '两江新区' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '重庆市'
        item['Project_district'] = '两江新区'


    elif strword and '宁河' in strword:
        item['Project_province'] = '天津市'
        item['Project_country'] = '天津市'
        item['Project_district'] = '宁河区'


    elif strword and '大港' in strword:
        item['Project_province'] = '天津市'
        item['Project_country'] = '天津市'
        item['Project_district'] = '大港区'


    elif strword and '崇文' in strword:
        item['Project_province'] = '北京市'
        item['Project_country'] = '北京市'
        item['Project_district'] = '崇文区'


    elif strword and '山南' in strword:
        item['Project_province'] = '西藏自治区'
        item['Project_country'] = '山南市'
        item['Project_district'] = '山南地区'



    elif strword and '林芝' in strword:
        item['Project_province'] = '西藏自治区'
        item['Project_country'] = '林芝市'
        item['Project_district'] = ''


    elif strword and '石景山' in strword:
        item['Project_province'] = '北京市'
        item['Project_country'] = '北京市'
        item['Project_district'] = '石景山区'


    elif strword and '康泰街' in strword:
        item['Project_province'] = '河北省'
        item['Project_country'] = '衡水市'
        item['Project_district'] = '开发区'


    elif strword and '大渡口' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '重庆市'
        item['Project_district'] = '大渡口区'


    elif strword and '宁河' in strword:
        item['Project_province'] = '天津市'
        item['Project_country'] = '天津市'
        item['Project_district'] = '宁河区'


    elif strword and '永川' in strword:
        item['Project_province'] = '重庆市'
        item['Project_country'] = '重庆市'
        item['Project_district'] = '永川区'


    elif strword and '松江' in strword:
        item['Project_province'] = '上海市'
        item['Project_country'] = '上海市'
        item['Project_district'] = '松江区'


    elif strword and '南汇区' in strword:
        item['Project_province'] = '上海市'
        item['Project_country'] = '上海市'
        item['Project_district'] = '南汇区'


    elif strword and '黄畈村' in strword:
        item['Project_province'] = '湖北省'
        item['Project_country'] = '咸宁市'
        item['Project_district'] = '永川区'


    elif strword and '将军庙' in strword or '鼓楼区' in strword:
        item['Project_province'] = '江苏省'
        item['Project_country'] = '南京市'
        item['Project_district'] = '鼓楼区'

    elif strword and '平安镇' in strword:
        item['Project_province'] = '青海省'
        item['Project_country'] = '海东市'
        item['Project_district'] = '平安区'


    elif strword and '华天道' in strword:
        item['Project_province'] = '天津市'
        item['Project_country'] = '天津市'
        item['Project_district'] = '华苑产业区'


    elif strword and 'xxx' in strword:
        item['Project_province'] = ''
        item['Project_country'] = ''
        item['Project_district'] = ''

    else:
        strwordlist = [strword]
        a = cpca.transform(strwordlist)
        item['Project_province']=a.loc[0]['省'][0:20]
        item['Project_country']=a.loc[0]['市'][0:20]
        item['Project_district']=a.loc[0]['区'][0:20]

    if strword and not item['Project_province'] and how != 1:
        item['Project_province'] = strword[0:20]
        item['Project_country'] = strword[0:20]
        item['Project_district'] = strword[0:20]

    return item


def get_timestr(date,outformat = "%Y-%m-%d",combdata = False):
    import time
    time_array = ''
    format_string = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H",
        "%Y-%m-%d",
        "（%Y-%m-%d %H:%M:%S）",
        "（%Y-%m-%d %H:%M）",
        "（%Y-%m-%d %H）",
        "（%Y-%m-%d）",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y/%m/%d %H",
        "%Y/%m/%d",
        "%Y.%m.%d %H:%M:%S",
        "%Y.%m.%d %H:%M",
        "%Y.%m.%d %H",
        "%Y.%m.%d",
        "%Y年%m月%d日 %H:%M:%S",
        "%Y年%m月%d日 %H:%M",
        "%Y年%m月%d日 %H",
        "%Y年%m月%d日",
        "%Y_%m_%d %H:%M:%S",
        "%Y_%m_%d %H:%M",
        "%Y_%m_%d %H",
        "%Y_%m_%d",
        "%Y%m%d%H:%M:%S",
        "%Y%m%d %H:%M:%S",
        "%Y%m%d %H:%M",
        "%Y%m%d %H",
        "%Y%m%d",
        "%Y%m%d%H%M%S",
        "%Y%m%d %H%M%S",
        "%Y%m%d %H%M",
        "%Y%m%d %H",
        "%Y%m%d",
        "%Y\%m\%d %H:%M:%S",
        "%Y\%m\%d %H:%M",
        "%Y\%m\%d %H",
        "%Y\%m\%d",
        "%Y年%m月%d日%H:%M:%S",
        "%Y年%m月%d日%H:%M",
        "%Y年%m月%d日%H",
        "%Y年%m月%d日",
    ]
    for i in format_string:

        try:
            time_array = time.strptime(date, i)
        except:
            continue

    if not time_array:
        return None
    timeL1 = int(time.mktime(time_array))
    timeL = time.localtime(timeL1)
    if combdata:
        return time.strftime(outformat, timeL),timeL1
    else:
        return time.strftime(outformat,timeL)


if __name__ == '__main__':
    aa = '2020-09-24'
    bb = get_timestr(aa,"%Y-%m-%d %H:%M:%S")
    print(bb)
