import gradio as gr
import datetime
import cnlunar
def luner_info(date = datetime.datetime.now()):
    """Get Chinese lunar calendar information for a given date.
    
    Args:
        date: The date to analyze, accepts datetime object or string in 'YYYY-MM-DD' format or 'YYYY年MM月DD日' format.Defaults to current date if not provided.
        
    Returns:
        Dictionary containing lunar calendar information including lunar date, zodiac, solar terms, and auspicious/inauspicious activities
    """
    if date == "":
        date = datetime.datetime.now()
    elif "-" in date:
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
    elif isinstance(date == datetime.datetime.now()):
        pass
    elif "年" in date:
        date = datetime.datetime.strptime(date, "%Y年%m月%d日")

    # 获取当前日期
    a = cnlunar.Lunar(date, godType='8char')  # 常规算法
    # a = cnlunar.Lunar(datetime.datetime(2022, 2, 3, 10, 30), godType='8char', year8Char='beginningOfSpring')  # 八字立春切换算法
    dic = {
        '日期': a.date,
        '农历': '%s %s[%s]年 %s%s' % (a.lunarYearCn, a.year8Char, a.chineseYearZodiac, a.lunarMonthCn, a.lunarDayCn),
        '星期': a.weekDayCn,
        # 未增加除夕
        '八字': ' '.join([a.year8Char, a.month8Char, a.day8Char, a.twohour8Char]),
        '今日节气': a.todaySolarTerms,
        '下一节气': (a.nextSolarTerm, a.nextSolarTermDate, a.nextSolarTermYear),
        '季节': a.lunarSeason,
        '生肖冲煞': a.chineseZodiacClash,
        '星座': a.starZodiac,
        '吉神方位': a.get_luckyGodsDirection(),
        '宜': a.goodThing,
        '忌': a.badThing,
    }
    data = ""
    for i in dic:
        midstr = '\t' * (2 - len(i) // 2) + ':' + '\t'
        data = data +str(i) + midstr + str(dic[i]) + "\n"
    return data
demo = gr.Interface(
    fn=luner_info,
    inputs=["text"],
    outputs="text",
    title="luner info",
    description="Get Chinese lunar calendar information for a given date."
)

demo.launch(mcp_server=True)
