""" Author: Li Wei """
""" Date: 2022-05-06 """
""" Description: game-GoBang """
# section1 Program initialization
import pygame
import datetime
import pandas as pd
import numpy as np
import random

# 按钮
class Button(object):
    def __init__(self, surface, color_B, color_T, text, x, y, length, width, font):
        self.surface = surface
        self.color_B = color_B
        self.text = text
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.font = font
        self.color_T = color_T

    #  创建按钮
    def set_Button(self):
        pygame.draw.rect(self.surface, self.color_B, (self.x, self.y, self.length, self.width), border_radius=30)
        button_text = self.font.render(self.text, True, self.color_T)
        window.blit(button_text, (self.x + self.length / 2 - button_text.get_rect().width / 2,
                                  self.y + self.width / 2 - button_text.get_rect().height / 2))
        pygame.display.flip()

    #  按下按钮
    def Button_press(self, mouseX, mouseY):
        if (mouseX >= self.x and mouseX <= self.x + self.length
                and mouseY >= self.y and mouseY <= self.y + self.width):
            return True
        else:
            return False

# 文本输入框
class InputBox:
    def __init__(self, rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)) -> None:
        self.boxBody: pygame.Rect = rect
        self.color_inactive = pygame.Color(211, 211, 211)  # 未被选中时颜色
        self.color_active = pygame.Color(65, 105, 225)  # 被选中时颜色
        self.color = self.color_inactive  # 初始为未激活颜色
        self.active = False
        self.text = ''
        self.text_length = 0
        self.done = False
        self.font = font1

    def dealMouse(self, event: pygame.event.Event):
        # 若按下鼠标且位置在文本框,文本框激活
        if self.boxBody.collidepoint(event.pos):
            self.active = True
        else:
            self.active = False
        # 文本框激活后变色
        if self.active:
            self.color = self.color_active
        else:
            self.color = self.color_inactive

    def dealKeyboard(self, event: pygame.event.Event):
        # 键盘输入响应
        if self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.text_length -= 1
            else:
                if self.text_length < 8:
                    self.text += event.unicode
                    self.text_length += 1

    def draw(self, screen: pygame.surface.Surface):
        txtSurface = self.font.render(self.text, True, (0, 0, 0))  # 文字转换为图片
        screen.blit(txtSurface, (self.boxBody.x+5, self.boxBody.y+5))
        pygame.draw.rect(screen, self.color, self.boxBody, 2)

# 文本提示框
def textBox(text, color, fontSize, pos):
    font = pygame.font.SysFont("FangSong", fontSize, bold=True)
    Text = font.render(text, True, color)
    window.blit(Text, pos)
    pygame.display.flip()

# 选择笔刷
def Font(size):
    f = pygame.font.SysFont("FangSong", size, bold=True)
    return f

# 获取游戏记录存档
def recordProcess(sheet, column):
    if sheet == 1:
        fileRecord = pd.read_excel("gameRecordFile.xlsx", usecols=[column], names=None)
        record_list = fileRecord.values.tolist()
    if sheet == 2:
        fileRecord = pd.read_excel("rankFile.xlsx", usecols=[column], names=None)
        record_list = fileRecord.values.tolist()
    return record_list

"---------------------------------------------------------------------------------------------------------------------"
# section2 Game initialization
pygame.init()  # 游戏初始化
pygame.mixer.init()  # 混音器模块初始化
window = pygame.display.set_mode((1100, 700))  # 创建游戏窗口
pygame.display.set_caption("GoBang")  # 设置窗口标题
music = pygame.mixer.Sound("丹凤.mp3")

#  初始化后续代码中的全局变量
#  存储记录的数组
global black_list
global white_list
global result_list
global time_list
global name_list
global score_list

# 按钮
global button_back1
global button_back2
global button_back3
global button_back4
global button_back5
global button_back6
global button_back7
global button_back8
global button_back9
global button_start
global button_rank
global button_re
global button_rule
global button_HuiQi
global button_HeQi
global button_pair
global button_auto
global button_confirm
global button_black
global button_white
global button_autob_confirm
global button_autow_confirm
global button_page1
global button_page2
global button_page3
global button_page4
global button_page5

# 信息输入框
global inputbox_black
global inputbox_white
global inputbox_auto_black
global inputbox_auto_white

# 初始化界面设计需要的笔刷
font1 = Font(35)
font2 = Font(30)
font3 = Font(32)
font4 = Font(45)

# 游戏记录、玩家积分的数据处理
black_list = recordProcess(1, 1)
white_list = recordProcess(1, 2)
result_list = recordProcess(1, 3)
time_list = recordProcess(1, 4)
name_list = recordProcess(2, 1)
score_list = recordProcess(2, 2)

# 棋子
black = pygame.image.load("黑.png")
black = pygame.transform.scale(black, (40, 40))  # 黑子图片
white = pygame.image.load("白.png")
white = pygame.transform.scale(white, (40, 40))  # 白子图片

# 游戏过程需要的标志
order = 0  # 所在页面编号
mode = 0  # 游戏模式  双人0 人机黑1  人机白2
auto = 1  # 人机电脑棋子
human = 0  # 人机玩家棋子
play = 1  # 游戏是否进行中  进行1  结束0
board = [[0] * 15 for i in range(15)]  # 本剧游戏棋盘记录
chessCount = 0  # 本局游戏落子个数
history = []  # 本局游戏落子记录
hejv = 0  # 是否平局
win = ""  # 胜方
lost = ""  # 负方
userName = []  # 玩家昵称
namedict = dict()  # 玩家昵称字典
page = 0  # 战绩页面页数
rankpage = 1  # 排行榜页面页数
voi = 0  # 音乐
mess = ""  # 本局游戏结果
"-----------------------------------------------------------------------------------------------------------------------"
#  section3 Interface initialization
#  切换界面：0：开始界面，1：游戏界面，2：选择模式界面，3：双人登陆界面 4：人机选棋界面
#  5：人机-黑界面 6：人机-白界面 7：历史战绩查询，8：玩家排行榜，9：游戏规则
def windowChange(order):
    # 开始
    if order == 0:
        global button_start
        global button_rank
        global button_re
        global button_rule
        startBackground = pygame.image.load("开始界面.png")
        window.blit(startBackground, (0, 0))
        voice = pygame.image.load("音效.png")
        voice = pygame.transform.scale(voice, (40, 40))
        window.blit(voice, (1020, 20))
        # 开始游戏按钮
        button_start = Button(window, (255, 211, 155), (0, 0, 0), "开始对决", 650, 100, 250, 120, font1)
        button_start.set_Button()
        # 排名榜按钮
        button_rank = Button(window, (255, 174, 185), (0, 0, 0), "玩家排行榜", 665, 270, 220, 95, font2)
        button_rank.set_Button()
        # 记录查询
        button_re = Button(window, (175, 238, 238), (0, 0, 0), "对战记录", 665, 410, 220, 95, font2)
        button_re.set_Button()
        # 游戏规则按钮
        button_rule = Button(window, (202, 225, 255), (0, 0, 0), "游戏规则", 665, 550, 220, 95, font2)
        button_rule.set_Button()
        pygame.display.flip()  # 更新窗口

    # 游戏
    if order == 1:
        global button_HuiQi
        global button_HeQi
        global button_back9

        gameBackground = pygame.image.load("游戏背景.jpg")
        window.blit(gameBackground, (0, 0))
        # 画棋盘
        pygame.draw.rect(window, (238, 154, 73), (50, 50, 630, 630))  # (x1, y1, length, width)
        for j in range(80, 680, 40):
            pygame.draw.line(window, (0, 0, 0), (80, j), (640, j), 3)
            pygame.draw.line(window, (0, 0, 0), (j, 80), (j, 640), 3)
        pygame.draw.circle(window, (0, 0, 0), (201, 201), 5)
        pygame.draw.circle(window, (0, 0, 0), (521, 201), 5)
        pygame.draw.circle(window, (0, 0, 0), (201, 521), 5)
        pygame.draw.circle(window, (0, 0, 0), (521, 521), 5)
        pygame.draw.circle(window, (0, 0, 0), (361, 361), 5)

        #  悔棋按钮
        button_HuiQi = Button(window, (185, 211, 238), (0, 0, 0), "悔 棋", 800, 400, 200, 80, font3)
        button_HuiQi.set_Button()
        #  和棋按钮
        button_HeQi = Button(window, (143, 188, 143), (0, 0, 0), "和 棋", 800, 500, 200, 80, font3)
        button_HeQi.set_Button()
        # 返回按钮
        button_back9 = Button(window, (255, 222, 173), (0, 0, 0), "返 回", 800, 600, 200, 80, font3)
        pygame.display.flip()  # 更新窗口

    # 选择模式
    if order == 2:
        global button_back4
        global button_auto
        global button_pair
        gameBackground = pygame.image.load("登录背景.jpg")
        gameBackground = pygame.transform.scale(gameBackground, (1100, 700))
        window.blit(gameBackground, (0, 0))

        button_pair = Button(window, (255, 222, 173), (0, 0, 0), "双人模式", 420, 200, 300, 120, font4)
        button_pair.set_Button()
        button_auto = Button(window, (255, 222, 173), (0, 0, 0), "人机模式", 420, 380, 300, 120, font4)
        button_auto.set_Button()
        button_back4 = Button(window, (255, 222, 173), (0, 0, 0), "返 回", 830, 570, 180, 75, font1)
        button_back4.set_Button()
        pygame.display.flip()  # 更新窗口

    # 双人登陆界面
    if order == 3:
        global button_back5
        global button_confirm
        global inputbox_black
        global inputbox_white

        gameBackground = pygame.image.load("双人登录.png")
        gameBackground = pygame.transform.scale(gameBackground, (1100, 700))
        window.blit(gameBackground, (0, 0))
        text_black = textBox("执黑方昵称：", (0, 0, 0), 30, (130, 200))
        text_white = textBox("执白方昵称：", (0, 0, 0), 30, (130, 400))
        button_confirm = Button(window, (255, 222, 173), (0, 0, 0), "确 定", 150, 580, 180, 75, font3)
        button_confirm.set_Button()
        button_back5 = Button(window, (255, 222, 173), (0, 0, 0), "返 回", 400, 580, 180, 75, font3)
        button_back5.set_Button()
        inputbox_black = InputBox(pygame.Rect(350, 185, 220, 60))  # 输入框
        inputbox_white = InputBox(pygame.Rect(350, 385, 220, 60))  # 输入框
        inputbox_black.draw(window)  # 输入框显示
        inputbox_white.draw(window)  # 输入框显示
        pygame.draw.rect(window, (255, 255, 255), (352, 187, 216, 56))  # 输入框底色
        pygame.draw.rect(window, (255, 255, 255), (352, 387, 216, 56))
        pygame.display.flip()  # 更新窗口

    # 人机选棋界面
    if order == 4:
        global button_back6
        global button_black
        global button_white
        gameBackground = pygame.image.load("人机登录.png")
        gameBackground = pygame.transform.scale(gameBackground, (1100, 700))
        window.blit(gameBackground, (0, 0))
        button_black = Button(window, (255, 222, 173), (0, 0, 0), "执 黑", 240, 200, 250, 120, font4)
        button_black.set_Button()
        button_white = Button(window, (255, 222, 173), (0, 0, 0), "执 白", 590, 200, 250, 120, font4)
        button_white.set_Button()
        button_back6 = Button(window, (255, 222, 173), (0, 0, 0), "返 回", 830, 570, 180, 75, font1)
        button_back6.set_Button()
        pygame.display.flip()  # 更新窗口

    # 人机-黑
    if order == 5:
        global button_back7
        global button_autob_confirm
        global inputbox_auto_black
        gameBackground = pygame.image.load("人机黑.png")
        gameBackground = pygame.transform.scale(gameBackground, (1100, 700))
        window.blit(gameBackground, (0, 0))
        button_back7 = Button(window, (255, 222, 173), (0, 0, 0), "返 回", 830, 600, 180, 75, font1)
        button_back7.set_Button()
        inputbox_auto_black = InputBox(pygame.Rect(280, 255, 220, 60))  # 输入框
        inputbox_auto_black.draw(window)  # 输入框显示
        pygame.draw.rect(window, (255, 255, 255), (280, 255, 220, 60))  # 输入框底色
        button_autob_confirm = Button(window, (255, 222, 173), (0, 0, 0), "确 定", 250, 500, 180, 75, font1)
        button_autob_confirm.set_Button()
        pygame.display.flip()  # 更新窗口

    # 人机-白
    if order == 6:
        global button_back8
        global button_autow_confirm
        global inputbox_auto_white
        gameBackground = pygame.image.load("人机白.png")
        gameBackground = pygame.transform.scale(gameBackground, (1100, 700))
        window.blit(gameBackground, (0, 0))
        button_back8 = Button(window, (255, 222, 173), (0, 0, 0), "返 回", 830, 600, 180, 75, font1)
        button_back8.set_Button()
        inputbox_auto_white = InputBox(pygame.Rect(280, 255, 220, 60))  # 输入框
        inputbox_auto_white.draw(window)  # 输入框显示
        pygame.draw.rect(window, (255, 255, 255), (280, 255, 220, 60))  # 输入框底色
        button_autow_confirm = Button(window, (255, 222, 173), (0, 0, 0), "确 定", 250, 500, 180, 75, font1)
        button_autow_confirm.set_Button()
        pygame.display.flip()  # 更新窗口

    # 战绩
    if order == 7:
        recordPage(1)

    # 排行榜
    if order == 8:
        rankProcess(1)

    # 规则
    if order == 9:
        global button_back3
        ruleBackground = pygame.image.load("游戏规则.png")
        ruleBackground = pygame.transform.scale(ruleBackground, (1100, 700))
        window.blit(ruleBackground, (0, 0))
        button_back3 = Button(window, (255, 222, 173), (0, 0, 0), "返 回", 830, 610, 180, 75, font1)
        button_back3.set_Button()
        pygame.display.flip()  # 更新窗口

"-------------------------------------------------------------------------------------------------------------------------"
# section4 Common functions
# 落子
def chessDown(mouseX, mouseY):
    global chessCount
    global board
    global history
    # 获得点位
    col = chessPos(mouseX)
    row = chessPos(mouseY)
    windowX = col * 40 + 60
    windowY = row * 40 + 60
    # 是否合法落子位置
    if board[row][col] == 0:
        # 更新棋子颜色,棋盘
        if chessCount % 2 == 0:
            chess = black
            board[row][col] = 1
        else:
            chess = white
            board[row][col] = 2
        # 落子
        window.blit(chess, (windowX, windowY))
        pygame.display.flip()
        chessCount += 1
        # 更新落子记录
        history.append([row, col])

# 判断落子位置
def chessPos(p):
    if p <= 100:
        pos = 0
    elif p >= 620:
        pos = 14
    elif p > 100 and p < 620:
        pos = int((p - 100) / 40 + 1)
    return pos

# 计算可移动位置
def empty(boardC, auto, row, col):
    minbR, maxbR, minbC, maxbC = 0, 0, 0, 0
    # 横向可移动范围
    if col >= 4:
        minR = 4
    else:
        minR = col

    if col <= 10:
        maxR = 4
    else:
        maxR = 14 - col
    # 纵向可移动范围
    if row >= 4:
        minC = 4
    else:
        minC = row

    if row <= 10:
        maxC = 4
    else:
        maxC = 14 - row

    if minR > 0:
        for i in range(1, minR + 1):
            if boardC[row][col - i] == auto or boardC[row][col - i] == 0:
                minbR += 1
            else:
                break
    if maxR > 0:
        for i in range(1, maxR + 1):
            # print("加分")
            if boardC[row][col + i] == auto or boardC[row][col + i] == 0:
                maxbR += 1
            else:
                break
    if minC > 0:
        for i in range(1, minC + 1):
            # print("加分")
            if boardC[row - i][col] == auto or boardC[row - i][col] == 0:
                minbC += 1
            else:
                break
    if maxC > 0:
        for i in range(1, maxC + 1):
            # print("加分")
            if boardC[row + i][col] == auto or boardC[row + i][col] == 0:
                maxbC += 1
            else:
                break
    return minbR, maxbR, minbC, maxbC

# 电脑落子评分 活2/活3/活4判断
def Live(boardC, row, col, minR, maxR, minC, maxC, auto, dir, c):
    if dir == 1:  # 水平移动
        count = 0
        for j in range(col - minR + 1, col + maxR + 1 - c):
            if boardC[row][j] == auto:
                count += 1
                if count >= c:
                    if board[row][j - c] == 0 or board[row][j + 1] == 0:
                        return True
            else:
                count = 0
    if dir == 2:  # 竖直移动
        count = 0
        for i in range(row - minC + 1, row + maxC + 1 - c):
            if boardC[i][col] == auto:
                count += 1
                if count >= c:
                    if board[i - c][col] == 0 or board[i + 1][col] == 0:
                        return True
            else:
                count = 0
    if dir == 3:  # 左上对角线移动
        count = 0
        minLU = min(minR, minC)  # 左上
        minRD = min(maxR, maxC)  # 右下
        for i in range(1 - minLU, minRD + 1 - c):
            if boardC[row + i][col + i] == auto:
                count += 1
                if count >= c:
                    if i - c in range(0, 15) and col - c in range(0, 15) and i + 1 in range(0, 15) and col + 1 in range(
                            0, 15):
                        if board[i - c][col - c] == 0 or board[i + 1][col + 1] == 0:
                            return True
            else:
                count = 0
    if dir == 4:  # 右上对角线移动
        count = 0
        minRU = min(maxR, minC)  # 右上
        minLD = min(minR, maxC)  # 左下
        for i in range(1 - minRU, minLD + 1 - c):
            if boardC[row + i][col - i] == auto:
                count += 1
                if count >= c:
                    if i-c in range(0, 15) and col - c in range(0, 15) and i + 1 in range(0, 15) and col - 1 in range(0, 15):
                        if board[i - c][col + c] == 0 or board[i + 1][col - 1] == 0:
                            return True
            else:
                count = 0
    return False

# 电脑落子评分 跳3判断
def Jump3(boardC, row, col, minR, maxR, minC, maxC, auto, dir):
    if dir == 1:  # 水平移动
        count = 0
        flag = 0
        for j in range(col - minR + 1, col + maxR - 3):
            if boardC[row][j] == auto:
                count += 1
                flag = 0
                if count >= 3:
                    if board[row][j - (3 + flag)] == 0 and board[row][j + 1] == 0 and (flag == 1 or flag == 0):
                        return True
            else:
                count = 0
                flag += 1
    if dir == 2:  # 竖直移动
        count = 0
        flag = 0
        for i in range(row - minC + 1, row + maxC - 3):
            if boardC[i][col] == auto:
                count += 1
                flag = 0
                if count >= 3:
                    if board[i - (3 + flag)][col] == 0 and board[i + 1][col] == 0 and (flag == 1 or flag == 0):
                        return True
            else:
                count = 0
                flag += 1
    if dir == 3:  # 左上对角线移动
        count = 0
        flag = 0
        minLU = min(minR, minC)  # 左上
        minRD = min(maxR, maxC)  # 右下
        for i in range(1 - minLU, minRD - 3):
            if boardC[row + i][col + i] == auto:
                count += 1
                flag = 0
                if count >= 3:
                    if board[i - (3 + flag)][col - (3 + flag)] == 0 and board[i + 1][col + 1] == 0 and (flag == 1 or flag == 0):
                        return True
            else:
                count = 0
                flag += 1
    if dir == 4:  # 右上对角线移动
        count = 0
        flag = 0
        minRU = min(maxR, minC)  # 右上
        minLD = min(minR, maxC)  # 左下
        for i in range(1 - minRU, minLD - 3):
            if boardC[row + i][col - i] == auto:
                count += 1
                flag = 0
                if count >= 3:
                    if board[i - (3 + flag)][col + (3 + flag)] == 0 and board[i + 1][col - 1] == 0 and (flag == 1 or flag == 0):
                        return True
            else:
                count = 0
                flag += 1
    return False

# 计算位置得分
def posScore(auto):
    score = [[0] * 15 for i in range(15)]
    boardC = board

    for row in range(0, 15):
        for col in range(0, 15):
            rowScore = 0
            colScore = 0
            diaScore = 0

            if board[row][col] == 0:
                score[row][col] = 1
                boardC[row][col] = auto
                minR, maxR, minC, maxC = empty(boardC, auto, row, col)
                # 横向分数
                if (minR + maxR + 1) >= 6:
                    if Live(boardC, row, col, 1, 4, minC, maxC, auto, 1, 4):
                        rowScore += 1000
                    if Jump3(boardC, row, col, minR, maxR, 1, 3, auto, 1):
                        rowScore += 3
                if (minR + maxR + 1) >= 4:
                    if Live(boardC, row, col, minR, maxR, 1, 3, auto, 1, 3):
                        rowScore += 6
                if (minR + maxR + 1) >= 2:
                    if Live(boardC, row, col, minR, maxR, 1, 2, auto, 1, 2):
                        rowScore += 3
                # 纵向得分
                if (minC + maxC + 1) >= 6:
                    if Live(boardC, row, col, 1, 4, minC, maxC, auto, 2, 4):
                        colScore += 1000
                    if Jump3(boardC, row, col, 1, 3, minC, maxC, auto, 2):
                        colScore += 3
                if (minC + maxC + 1) >= 4:
                    if Live(boardC, row, col, 1, 3, minC, maxC, auto, 2, 3):
                        colScore += 6
                if (minC + maxC + 1) >= 2:
                    if Live(boardC, row, col, 1, 2, minC, maxC, auto, 2, 2):
                        colScore += 3
                # 对角线得分
                if (minR + maxR + 1) >= 6 and (minC + maxC + 1) >= 6:
                    if Live(boardC, row, col, minR, maxR, minC, maxC, auto, 3, 4):
                        diaScore += 1000
                    if Live(boardC, row, col, minR, maxR, minC, maxC, auto, 4, 4):
                        diaScore += 1000
                    if Jump3(boardC, row, col, minR, maxR, minC, maxC, auto, 3):
                        diaScore += 3
                    if Jump3(boardC, row, col, minR, maxR, minC, maxC, auto, 4):
                        diaScore += 3
                if (minR + maxR + 1) >= 4 and (minC + maxC + 1) >= 4:
                    if Live(boardC, row, col, minR, maxR, minC, maxC, auto, 3, 3):
                        diaScore += 6
                    if Live(boardC, row, col, minR, maxR, minC, maxC, auto, 4, 3):
                        diaScore += 6
                if (minR + maxR + 1) >= 2 and (minC + maxC + 1) >= 2:
                    if Live(boardC, row, col, minR, maxR, minC, maxC, auto, 3, 2):
                        diaScore += 3
                    if Live(boardC, row, col, minR, maxR, minC, maxC, auto, 4, 2):
                        diaScore += 3
                boardC[row][col] = 0
                score[row][col] += score[row][col] + rowScore + colScore + diaScore + minR + maxR + minC + maxC
            else:
                score[row][col] = -1000
    return score

# 电脑落子
def autoChessDown():
    global auto
    global human
    # 确定执子方
    if auto == 1:
        human = 2
    else:
        human = 1
    score = posScore(auto)  # AI全棋盘落子分数
    score_human = posScore(human)  # 玩家全棋盘落子分数

    score1 = np.array(score)
    score_max = score1.max()  # AI落子位置分数最大值
    score_human1 = np.array(score_human)
    score_human_max = score_human1.max()  # 玩家落子位置分数最大值

    score2 = np.argmax(score1)  # 把矩阵拉成一维，m是在一维数组中最大值的下标
    score_human2 = np.argmax(score_human1)
    row_auto, col_auto = divmod(score2, score1.shape[1])  # r和c分别为商和余数，即最大值在矩阵中的行和列
    row_human, col_human = divmod(score_human2, score_human1.shape[1])
    if score_max >= score_human_max:  # 攻/防选择，返回落子位置
        return col_auto * 40 + 80, row_auto * 40 + 80
    else:
        return col_human * 40 + 80, row_human * 40 + 80

# 判断输赢
def isWin(board, mouseX, mouseY):
    heng, shu, xie = 0, 0, 0
    # 判断棋子颜色
    if chessCount % 2 == 1:
        flag = 1  # 黑子
    else:
        flag = 2  # 白子
    # 获得点位
    col = chessPos(mouseX)
    row = chessPos(mouseY)
    # 水平方向
    i = row
    while heng < 5 and i > -1 and board[i][col] == flag:
        heng += 1
        i -= 1
    i = row + 1
    while heng < 5 and i < 15 and board[i][col] == flag:
        heng += 1
        i += 1
    # 竖直方向
    if heng < 5:
        j = col
        while shu < 5 and j > -1 and board[row][j] == flag:
            shu += 1
            j -= 1
        j = col + 1
        while shu < 5 and j < 15 and board[row][j] == flag:
            shu += 1
            j += 1
    # 对角线方向
    if heng < 5 and shu < 5:
        i, j = row, col
        while xie < 5 and j > -1 and i > -1 and board[i][j] == flag:
            xie += 1
            j -= 1
            i -= 1
        i, j = row + 1, col + 1
        while xie < 5 and j < 15 and i < 15 and board[i][j] == flag:
            xie += 1
            j += 1
            i += 1
    if heng == 5 or shu == 5 or xie == 5:
        return True
    return False

# 悔棋
def HuiQi(pos):
    # 移除棋子
    # 画矩形
    global board
    global chessCount
    global history
    row = pos[0]
    col = pos[1]
    windowX = col * 40 + 60
    windowY = row * 40 + 60
    pygame.draw.rect(window, (238, 154, 73), (windowX, windowY, 40, 40))
    # 画线
    if col != 0:  # 左
        pygame.draw.line(window, (0, 0, 0), (60 + col * 40, 80 + row * 40), (80 + col * 40, 80 + row * 40), 3)
    if col != 14:  # 右
        pygame.draw.line(window, (0, 0, 0), (80 + col * 40, 80 + row * 40), (100 + col * 40, 80 + row * 40), 3)
    if row != 0:  # 上
        pygame.draw.line(window, (0, 0, 0), (80 + col * 40, 60 + row * 40), (80 + col * 40, 80 + row * 40), 3)
    if row != 14:  # 下
        pygame.draw.line(window, (0, 0, 0), (80 + col * 40, 80 + row * 40), (80 + col * 40, 100 + row * 40), 3)
    # 修改棋盘信息
    board[row][col] = 0
    # 修改落子数
    chessCount -= 1
    pygame.display.flip()  # 更新窗口

# 结束游戏，处理本次游戏记录
def endGame(he):
    global userName
    global win
    global lost
    global hejv
    global mess

    if he:
        mess = "和局"
        win = userName[0]
        lost = userName[1]
        hejv = 1
    else:
        if chessCount % 2 == 1:
            mess = "黑方胜"
            win = userName[0]
            lost = userName[1]
        else:
            mess = "白方胜"
            win = userName[1]
            lost = userName[0]

    resultText = font4.render(mess, True, (255, 0, 0))
    window.blit(resultText, (790, 300))
    pygame.display.flip()
    # 记录存档
    date = datetime.datetime.now()
    gameRecord = {'black': [], 'white': [], 'result': [], 'date': []}  # 游戏记录存档获取
    rankRecord = {'name': [], 'score': []}
    length = len(black_list)
    # 若记录已满70条， 保留最新的70条
    if length == 70:
        for i in range(1, 70):
            black_list[i - 1][0] = black_list[i][0]
            white_list[i - 1][0] = white_list[i][0]
            result_list[i - 1][0] = result_list[i][0]
            time_list[i - 1][0] = time_list[i][0]
        black_list[69] = userName[0]
        white_list[69] = userName[1]
        result_list[69] = mess
        time_list[69] = date.strftime("%m-%d %H:%M")
    else:
        black_list.append([userName[0]])
        white_list.append([userName[1]])
        result_list.append([mess])
        time_list.append([date.strftime("%m-%d %H:%M")])
    for i in range(0, length + 1):
        gameRecord['black'].append(black_list[i][0])
        gameRecord['white'].append(white_list[i][0])
        gameRecord['result'].append(result_list[i][0])
        gameRecord['date'].append(time_list[i][0])

    # 更新游戏记录
    data = pd.DataFrame(gameRecord)
    data.to_excel("gameRecordFile.xlsx")
    # 更新玩家排名
    ranklist = scorePlus(he)
    for item in ranklist:
        rankRecord['name'].append(item[0])
        rankRecord['score'].append(item[1])
    data2 = pd.DataFrame(rankRecord)
    data2.to_excel("rankFile.xlsx")

# 玩家加分 胜3 负0 平1
def scorePlus(he):
    global win
    global lost
    global namedict
    if he:
        if win != "computer":
            if win not in namedict.keys():
                namedict[win] = 1
            else:
                namedict[win] += 1
        if lost != "computer":
            if lost not in namedict.keys():
                namedict[lost] = 1
            else:
                namedict[lost] += 1
    else:
        if win != "computer":
            if win not in namedict.keys():
                namedict[win] = 3
            else:
                namedict[win] += 3
            if lost not in namedict.keys():
                namedict[lost] = 0
            else:
                namedict[lost] += 0
    #  玩家积分排序
    ranklist = sorted(namedict.items(), key=lambda x: x[1], reverse=True)
    return ranklist

# 显示游戏记录
def recordPage(page):
    global button_back1
    global button_page1
    global button_page2
    global button_page3
    global button_page4
    global button_page5
    global black_list
    global white_list
    global result_list
    global time_list
    reBackground = pygame.image.load("历史战绩.png")
    reBackground = pygame.transform.scale(reBackground, (1100, 700))
    window.blit(reBackground, (0, 0))
    button_back1 = Button(window, (255, 222, 173), (0, 0, 0), "返 回", 70, 50, 180, 75, font3)
    button_back1.set_Button()
    button_page1 = Button(window, (255, 222, 173), (0, 0, 0), "1", 760, 70, 50, 50, font3)
    button_page2 = Button(window, (255, 222, 173), (0, 0, 0), "2", 820, 70, 50, 50, font3)
    button_page3 = Button(window, (255, 222, 173), (0, 0, 0), "3", 880, 70, 50, 50, font3)
    button_page4 = Button(window, (255, 222, 173), (0, 0, 0), "4", 940, 70, 50, 50, font3)
    button_page5 = Button(window, (255, 222, 173), (0, 0, 0), "5", 1000, 70, 50, 50, font3)
    if page == 1:
        button_page1 = Button(window, (255, 106, 106), (0, 0, 0), "1", 760, 70, 50, 50, font3)
    if page == 2:
        button_page2 = Button(window, (255, 106, 106), (0, 0, 0), "2", 820, 70, 50, 50, font3)
    if page == 3:
        button_page3 = Button(window, (255, 106, 106), (0, 0, 0), "3", 880, 70, 50, 50, font3)
    if page == 4:
        button_page4 = Button(window, (255, 106, 106), (0, 0, 0), "4", 940, 70, 50, 50, font3)
    if page == 5:
        button_page5 = Button(window, (255, 106, 106), (0, 0, 0), "5", 1000, 70, 50, 50, font3)
    button_page1.set_Button()
    button_page2.set_Button()
    button_page3.set_Button()
    button_page4.set_Button()
    button_page5.set_Button()
    textBox("黑方", (139, 58, 58), 32, (120, 140))
    textBox("白方", (139, 58, 58), 32, (340, 140))
    textBox("对弈结果", (139, 58, 58), 32, (560, 140))
    textBox("对弈时间", (139, 58, 58), 32, (780, 140))

    recordCount = len(black_list)

    # 计算页数
    if recordCount % 13 == 0:
        pageNeed = int(recordCount / 13)
        dataLast = 13
    else:
        pageNeed = int(recordCount / 13 + 1)
        dataLast = recordCount - (13 * (pageNeed - 1))
    # 最后一页数据个数
    icount = 13 * (page - 1)
    if page == pageNeed:
        fcount = icount + dataLast
    else:
        fcount = 13 * page

    ii = 0
    for i in range(icount, fcount):
        record = black_list[i][0]
        recordPic = font2.render(str(record), True, (0, 0, 0))
        window.blit(recordPic, (120, 180 + 40 * ii))
        record = white_list[i][0]
        recordPic = font2.render(str(record), True, (0, 0, 0))
        window.blit(recordPic, (340, 180 + 40 * ii))
        record = result_list[i][0]
        recordPic = font2.render(str(record), True, (0, 0, 0))
        window.blit(recordPic, (560, 180 + 40 * ii))
        record = time_list[i][0]
        recordPic = font2.render(str(record), True, (0, 0, 0))
        window.blit(recordPic, (780, 180 + 40 * ii))
        ii += 1

    pygame.display.flip()  # 更新窗口

# 显示玩家排名
def rankProcess(rankpage):
    global button_back2
    global button_page1
    global button_page2
    global button_page3
    global button_page4
    global button_page5
    global namedict

    reBackground = pygame.image.load("玩家排行榜.png")
    reBackground = pygame.transform.scale(reBackground, (1100, 700))
    window.blit(reBackground, (0, 0))
    button_back2 = Button(window, (255, 222, 173), (0, 0, 0), "返 回", 70, 50, 180, 75, font3)
    button_back2.set_Button()
    button_page1 = Button(window, (255, 222, 173), (0, 0, 0), "1", 780, 70, 50, 50, font3)
    button_page2 = Button(window, (255, 222, 173), (0, 0, 0), "2", 840, 70, 50, 50, font3)
    button_page3 = Button(window, (255, 222, 173), (0, 0, 0), "3", 900, 70, 50, 50, font3)
    button_page4 = Button(window, (255, 222, 173), (0, 0, 0), "4", 960, 70, 50, 50, font3)
    button_page5 = Button(window, (255, 222, 173), (0, 0, 0), "5", 1020, 70, 50, 50, font3)
    if rankpage == 1:
        button_page1 = Button(window, (255, 106, 106), (0, 0, 0), "1", 780, 70, 50, 50, font3)
    if rankpage == 2:
        button_page2 = Button(window, (255, 106, 106), (0, 0, 0), "2", 840, 70, 50, 50, font3)
    if rankpage == 3:
        button_page3 = Button(window, (255, 106, 106), (0, 0, 0), "3", 900, 70, 50, 50, font3)
    if rankpage == 4:
        button_page4 = Button(window, (255, 106, 106), (0, 0, 0), "4", 960, 70, 50, 50, font3)
    if rankpage == 5:
        button_page5 = Button(window, (255, 106, 106), (0, 0, 0), "5", 1020, 70, 50, 50, font3)
    button_page1.set_Button()
    button_page2.set_Button()
    button_page3.set_Button()
    button_page4.set_Button()
    button_page5.set_Button()

    ranklist = sorted(namedict.items(), key=lambda x: x[1], reverse=True)
    recordCount = len(ranklist)

    # 计算页数
    if recordCount % 14 == 0:
        pageNeed = int(recordCount / 14)
        dataLast = 14
    else:
        pageNeed = int(recordCount / 14 + 1)
        dataLast = recordCount - (14 * (pageNeed - 1))

    icount = 14 * (rankpage - 1)
    if rankpage == pageNeed:
        fcount = icount + dataLast
    else:
        fcount = 14 * rankpage

    ii = 0
    for i in range(icount, fcount):
        if i == 0 or i == 1 or i == 2:
            colour = (238, 44, 44)
        else:
            colour = (0, 0, 0)
        record = ranklist[i][0]
        recordPic = font2.render(str(record), True, colour)
        window.blit(recordPic, (340, 140 + 40 * ii))
        record = ranklist[i][1]
        recordPic = font2.render(str(record), True, colour)
        window.blit(recordPic, (680, 140 + 40 * ii))
        ii += 1

    pygame.display.flip()  # 更新窗口

# 处理玩家积分
def scoreProcess():
    global namedict
    i = 0
    for name in name_list:
        namedict[name[0]] = score_list[i][0]
        i += 1

"----------------------------------------------------------------------------------------------------------------------"
# section5 Interface specific functions
# 0：开始界面，1：游戏界面，2：选择模式界面，3：双人登陆界面 4：人机选棋界面
# 5：人机-黑界面 6：人机-白界面 7：历史战绩查询，8：玩家排行榜，9：游戏规则

# 0开始界面功能
def startFunc():
    global order
    global voi
    global play
    global win
    global lost
    global chessCount
    global board
    global history
    global mode
    global hejv
    global mess
    global userName

    win = ""
    lost = ""
    chessCount = 0  # 落子个数
    board = [[0] * 15 for i in range(15)]  # 棋盘记录
    history = []  # 落子记录
    mode = 0  # 游戏模式  双人0 人机黑1  人机白2
    hejv = 0
    mess = ""
    userName = []

    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos

        if button_start.Button_press(x, y):
            order = 2
            play = 1
            windowChange(order)
        if button_re.Button_press(x, y):
            order = 7
            windowChange(order)
        if button_rank.Button_press(x, y):
            order = 8
            windowChange(order)
        if button_rule.Button_press(x, y):
            order = 9
            windowChange(order)
        if x <= 1060 and x >= 1020 and y <= 60 and y >= 20:
            if voi:
                music.stop()
                voi = 0
            else:
                music.play()
                voi = 1

# 1游戏界面功能
def gameFunc():
    global chessCount
    global board
    global history
    global order
    global play
    global mode
    global auto
    global userName
    global button_back9
    global order
    global win
    global lost
    global hejv

    font = pygame.font.SysFont("Arial", 60, bold=True)
    textBlack = font.render(userName[0], True, (65, 105, 225))
    window.blit(textBlack, (890 - textBlack.get_rect().width / 2, 30))
    textVS = textBox("VS", (0, 0, 0), 60, (850, 110))
    textWhite = font.render(userName[1], True, (65, 105, 225))
    window.blit(textWhite, (890 - textWhite.get_rect().width / 2, 170))


    # 人机模式，电脑执黑，游戏开始时电脑先下一子
    if chessCount == 0 and mode == 2 and auto == 1:
        i = random.randint(70, 650)
        j = random.randint(70, 650)
        chessDown(i, j)
    pygame.display.flip()

    # 下棋
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        if play == 1 and button_HuiQi.Button_press(x, y):
            if chessCount > 0:
                HuiQi(history.pop())

        if play == 1 and button_HeQi.Button_press(x, y):
            hejv = 1
            endGame(1)

        if mode == 1:
            if play == 1 and x >= 70 and x <= 650 and y >= 70 and y <= 650:  # 容许一定点击误差
                chessDown(x, y)
                if chessCount == 225:
                    play = 0
                    endGame(1)
                if isWin(board, x, y):
                    play = 0
                    endGame(0)

        if mode == 2 and play == 1:
            if (chessCount % 2) != (auto - 1):
                if play == 1 and x >= 70 and x <= 650 and y >= 70 and y <= 650:  # 容许一定点击误差
                    chessDown(x, y)
                    if chessCount == 225:
                        play = 0
                        endGame(1)
                    if isWin(board, x, y):
                        play = 0
                        endGame(0)
                    a, b = autoChessDown()
                    chessDown(a, b)
                    if chessCount == 225:
                        play = 0
                        endGame(1)
                    if isWin(board, a, b):
                        play = 0
                        endGame(0)

        if play == 0 or hejv == 1:
            button_back9.set_Button()
            pygame.display.flip()  # 更新窗口
            if button_back9.Button_press(x, y):
                order = 0
                windowChange(order)

# 2选择模式界面
def modeFunc():
    global order
    global mode
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos

        if button_back4.Button_press(x, y):
            order = 0
            windowChange(order)
        elif button_auto.Button_press(x, y):
            mode = 2
            order = 4
            windowChange(order)
        elif button_pair.Button_press(x, y):
            mode = 1
            order = 3
            windowChange(order)

# 3双人登陆模式
def pairFunc():
    global order
    global inputbox_black
    global inputbox_white

    if event.type == pygame.MOUSEBUTTONDOWN:
        pygame.draw.rect(window, (255, 255, 255), (352, 187, 216, 56))  # 输入框底色
        pygame.draw.rect(window, (255, 255, 255), (352, 387, 216, 56))
        inputbox_black.dealMouse(event)
        inputbox_white.dealMouse(event)
        inputbox_black.draw(window)  # 输入框显示
        inputbox_white.draw(window)
        pygame.display.flip()

        x, y = event.pos
        if button_back5.Button_press(x, y):
            order = 2
            windowChange(order)
        elif button_confirm.Button_press(x, y):
            # 保存昵称
            if len(inputbox_black.text) > 0 and len(inputbox_white.text) > 0:
                userName.append(inputbox_black.text)
                userName.append(inputbox_white.text)
                order = 1
                windowChange(order)

    if event.type == pygame.KEYDOWN:
        pygame.draw.rect(window, (255, 255, 255), (352, 187, 216, 56))  # 输入框底色
        pygame.draw.rect(window, (255, 255, 255), (352, 387, 216, 56))
        inputbox_black.dealKeyboard(event)
        inputbox_white.dealKeyboard(event)
        inputbox_black.draw(window)  # 输入框显示
        inputbox_white.draw(window)
        pygame.display.flip()

# 4人机选棋界面
def autoFunc():
    global order
    global auto
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos

        if button_back6.Button_press(x, y):
            order = 2
            windowChange(order)
        if button_black.Button_press(x, y):
            auto = 2
            order = 5
            windowChange(order)
        if button_white.Button_press(x, y):
            auto = 1
            order = 6
            windowChange(order)

# 5人机黑界面
def autoBlackFunc():
    global order
    global inputbox_auto_black

    if event.type == pygame.MOUSEBUTTONDOWN:
        pygame.draw.rect(window, (255, 255, 255), (280, 255, 220, 60))  # 输入框底色
        inputbox_auto_black.dealMouse(event)
        inputbox_auto_black.draw(window)  # 输入框显示
        pygame.display.flip()

        x, y = event.pos

        if button_back7.Button_press(x, y):
            order = 4
            windowChange(order)

        elif button_autob_confirm.Button_press(x, y):
            # 保存昵称
            if len(inputbox_auto_black.text) > 0:
                userName.append(inputbox_auto_black.text)
                userName.append("computer")
                order = 1
                windowChange(order)

    if event.type == pygame.KEYDOWN:
        pygame.draw.rect(window, (255, 255, 255), (280, 255, 220, 60))  # 输入框底色
        inputbox_auto_black.dealKeyboard(event)
        inputbox_auto_black.draw(window)  # 输入框显示
        pygame.display.flip()

# 6人机白界面
def autoWhiteFunc():
    global order
    if event.type == pygame.MOUSEBUTTONDOWN:
        pygame.draw.rect(window, (255, 255, 255), (280, 255, 220, 60))  # 输入框底色
        inputbox_auto_white.dealMouse(event)
        inputbox_auto_white.draw(window)  # 输入框显示
        pygame.display.flip()

        x, y = event.pos

        if button_back8.Button_press(x, y):
            order = 4
            windowChange(order)

        elif button_autow_confirm.Button_press(x, y):
            # 保存昵称
            if len(inputbox_auto_white.text) > 0:
                userName.append("computer")
                userName.append(inputbox_auto_white.text)
                order = 1
                windowChange(order)

    if event.type == pygame.KEYDOWN:
        pygame.draw.rect(window, (255, 255, 255), (280, 255, 220, 60))  # 输入框底色
        inputbox_auto_white.dealKeyboard(event)
        inputbox_auto_white.draw(window)  # 输入框显示
        pygame.display.flip()

# 7战绩界面功能
def reFunc():
    global order
    global page
    global black_list
    page = 1
    recordCount = len(black_list)
    # 计算页数
    if recordCount % 13 == 0:
        pageNeed = int(recordCount / 13)
    else:
        pageNeed = int(recordCount / 13 + 1)

    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        if button_back1.Button_press(x, y):
            order = 0
            page = 0
            windowChange(0)
        if button_page1.Button_press(x, y):
            recordPage(1)
        if button_page2.Button_press(x, y):
            if pageNeed >= 2:
                recordPage(2)
        if button_page3.Button_press(x, y):
            if pageNeed >= 3:
                recordPage(3)
        if button_page4.Button_press(x, y):
            if pageNeed >= 4:
                recordPage(4)
        if button_page5.Button_press(x, y):
            if pageNeed >= 5:
                recordPage(5)

# 8排行界面功能
def rankFunc():
    global order
    global rankpage
    global namedict
    rankpage = 1
    ranklist = sorted(namedict.items(), key=lambda x: x[1], reverse=True)
    recordCount = len(ranklist)
    # 计算页数
    if recordCount % 14 == 0:
        pageNeed = int(recordCount / 14)
    else:
        pageNeed = int(recordCount / 14 + 1)

    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        if button_back2.Button_press(x, y):
            order = 0
            rankpage = 0
            windowChange(0)
        if button_page1.Button_press(x, y):
            rankProcess(1)
        if button_page2.Button_press(x, y):
            if pageNeed >= 2:
                rankProcess(2)
        if button_page3.Button_press(x, y):
            if pageNeed >= 3:
                rankProcess(3)
        if button_page4.Button_press(x, y):
            if pageNeed >= 4:
                rankProcess(4)
        if button_page5.Button_press(x, y):
            if pageNeed >= 5:
                rankProcess(5)

# 9规则界面功能
def ruleFunc():
    global order
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos

        if button_back3.Button_press(x, y):
            order = 0
            windowChange(order)

scoreProcess()
windowChange(0)
pygame.display.flip()  # 更新窗口
"-----------------------------------------------------------------------------------------------------------------------"
# 切换界面：0：开始界面，1：游戏界面，2：选择模式界面，3：双人登陆界面 4：人机选棋界面
# 5：人机-黑界面 6：人机-白界面 7：历史战绩查询，8：玩家排行榜，9：游戏规则
# section6 the Game loop
while True:
    for event in pygame.event.get():
        # 关闭游戏窗口
        if event.type == pygame.QUIT:
            exit()

        # 开始界面
        if order == 0:
            startFunc()

        # 游戏界面
        if order == 1:
            gameFunc()

        # 选择模式界面
        if order == 2:
            modeFunc()

        # 双人登录界面
        if order == 3:
            pairFunc()

        # 人机选棋界面
        if order == 4:
            autoFunc()

        # 人机黑界面
        if order == 5:
            autoBlackFunc()

        # 人机白界面
        if order == 6:
            autoWhiteFunc()

        # 战绩界面
        if order == 7:
            reFunc()

        # 排行榜
        if order == 8:
            rankFunc()

        # 规则
        if order == 9:
            ruleFunc()






