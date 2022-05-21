class Comment:
    def diffToCurrent(self, index, column):
        return round(self.statics.loc['current', column] - self.statics.loc[index, column], 2)
    def diffToCurrentInPercent(self, index, column):
        return round(((self.statics.loc['current', column] - self.statics.loc[index, column]) / self.statics.loc[index, column]) * 100, 2)
    def increaseTrend(self, column):
        increase1 = self.statics.loc['current', column] > self.statics.loc['prev1', column]
        increase2 = self.statics.loc['prev1', column] > self.statics.loc['prev2', column]
        increase3 = self.statics.loc['prev2', column] > self.statics.loc['prev3', column]
        return increase1 and increase2 and increase3
    def decreaseTrend(self, column):
        decrease1 = self.statics.loc['current', column] < self.statics.loc['prev1', column]
        decrease2 = self.statics.loc['prev1', column] < self.statics.loc['prev2', column]
        decrease3 = self.statics.loc['prev2', column] < self.statics.loc['prev3', column]
        return decrease1 and decrease2 and decrease3
    def periodMax(self, column):
        return self.statics.loc['current', column] == self.statics.loc['max', column]
    def periodMin(self, column):
        return self.statics.loc['current', column] == self.statics.loc['min', column]
    def makeComments(self):
        for event_name in self.statics:
            if self.periodMax(event_name):
                self.positive.append(self.event_map[event_name]+'為30日內最高')
            elif self.periodMin(event_name):
                self.negative.append(self.event_map[event_name]+'為30日內最低')
            else:
                if event_name == 'convert_rate':
                    diff = self.diffToCurrent('mean', event_name)
                else:
                    diff = self.diffToCurrentInPercent('mean', event_name)
                if diff >= 0:
                    # self.positive.append(self.event_map[event_name]+'高於30日平均值'+str(diff)+'%')
                    self.positive.append('本日{0}對比30日內平均值({1})，上升+{2}%'.format(self.event_map[event_name], round(self.statics.loc['mean', event_name], 3), diff))
                else:
                    # self.negative.append(self.event_map[event_name]+'低於30日平均值'+str(diff*-1)+'%')
                    self.negative.append('本日{0}對比30日內平均值({1})，下降-{2}%'.format(self.event_map[event_name], round(self.statics.loc['mean', event_name], 3), diff*-1))
            if self.decreaseTrend(event_name):
                self.negative.append(self.event_map[event_name]+'已連續三天下降')
            if self.increaseTrend(event_name):
                self.positive.append(self.event_map[event_name]+'已連續三天上升')
        with open('positive_comment.txt', 'w') as f:
            for comment in self.positive:
                f.write(comment+',')
        with open('negative_comment.txt', 'w') as f:
            for comment in self.negative:
                f.write(comment+',')
    def __init__(self, statics):
        self.statics = statics
        self.positive = []
        self.negative = []
        self.event_map = {'purchase': '結帳完成次數', 'session_start': '工作階段啟動次數', 'convert_rate': '轉換率', 'revenue': '銷售額'}