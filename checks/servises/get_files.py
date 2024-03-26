import io
import xlsxwriter
from checks.servises.rating import getRating

from checks.models import EmployeePosition, Question, Result, ControlEvent, CorrectionReport, CorrectionReportComment
from checks.servises.count_score_of_control_event import Counter, NewCounter
from checks.servises.decorators import xlsx_file


class CheckListReport:

    def __init__(self, control_event):
        self.control_event = control_event
        self.queryset = Result.objects.filter(control_event=self.control_event).order_by('question__sort_id')

    def download_check_list_file(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        bold = workbook.add_format({'bold': True})
        worksheet = workbook.add_worksheet()

        row = 0

        worksheet.write(row, 0, f"Объект: {self.queryset[0].control_event.object} "
                                f"Дата проверки: {self.queryset[0].control_event.date}",
                        bold)
        row += 1

        for item in self.queryset:
            worksheet.write(row, 0, str(item.question))
            worksheet.write(row, 1, str(item.grade))
            row += 1

        worksheet.write(row, 0, f"Итоговая оценка: {Counter(self.control_event).count_score()} балла(-ов)")

        row += 1

        employee_results = NewCounter(self.control_event).employee_count_score()

        for key, value in employee_results.items():
            worksheet.write(
                row, 0, f"Оценка {key}: {value} балла(-ов)"
            )

            row += 1

        workbook.close()
        output.seek(0)

        return output

    def create_filename(self):
        return f"{self.queryset[0].control_event.date}_" \
               f"{self.queryset[0].control_event.object.name}.xlsx"


class MainReport:
    def __init__(self, start_date, finish_date, executive_director=None):
        self.start_date = start_date
        self.finish_date = finish_date
        self.executive_director = executive_director

    def download_file(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        bold = workbook.add_format({'bold': True})
        worksheet = workbook.add_worksheet()
        employee_positions = EmployeePosition.objects.all()

        column_headers = ['Дата', 'Объект', 'Муниципалитет', 'Оценка', 'Баллы'] + [position.position for position in employee_positions] +  ['Наличие просроченной продукции', 'Наличие недоброкачественной продукции']
        row = 0

        for index, header in enumerate(column_headers):
            worksheet.write(row, index, header, bold)
        row += 1

        control_events = None

        if self.executive_director != None:
            control_events = ControlEvent.objects.filter(
                date__range=[self.start_date, 
                self.finish_date], object__location__executive_director=self.executive_director
                ).order_by('date')
        else:
            control_events = ControlEvent.objects.filter(
                date__range=[self.start_date, 
                self.finish_date]
                ).order_by('date')
        
        for i in control_events:
            counter = NewCounter(i.id)
            employee_results = counter.employee_count_score()

            column = 0

            worksheet.write(row, column, str(i.date.strftime("%d.%m.%Y")))
            column += 1

            worksheet.write(row, column, str(i.object.name))
            column += 1

            worksheet.write(row, column, str(i.object.location))
            column += 1

            worksheet.write(row, column, counter.common_grade())
            column += 1

            worksheet.write(row, column, counter.count_score())
            column += 1

            for employee_result in employee_results.values():
                worksheet.write(row, column, employee_result["score"])
                column += 1

            worksheet.write(row, column, str(counter.is_overdue_food()))
            column += 1

            worksheet.write(row, column, str(counter.is_poor_quality()))
            row += 1

        workbook.close()
        output.seek(0)

        return output


class BreachStatistics:

    def __init__(self, start_date, finish_date):
        self.start_date = start_date
        self.finish_date = finish_date

    def download_file(self):

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})

        column_headers = ['Нарушение', 'Количество фактов', '% от общего числа нарушений', '% проверок от общего числа, в которых встречается нарушение']

        question_count = {}

        for result in Result.objects.filter(grade__name='Нет', control_event__date__range=[self.start_date, self.finish_date]):
            
            if result.question in question_count:
                question_count[result.question] += 1

            else:
                question_count[result.question] = 1

        question_count_sorted = {key: value for key, value in sorted(question_count.items(), key=lambda item: item[1], reverse=True)}
        question_sum = sum([grade for grade in question_count.values()])

        row = 0

        for index, header in enumerate(column_headers):
            worksheet.write(row, index, header, bold)

        row += 1

        for i in question_count_sorted.items():
            worksheet.write(row, 0, str(i[0]))
            worksheet.write(row, 1, str(i[1]))
            worksheet.write(row, 2, round((i[1] / question_sum * 100), 2))
            worksheet.write(row, 3, round((i[1] / ControlEvent.objects.filter(date__range=[self.start_date, self.finish_date]).count()) * 100))
            row += 1
        
        workbook.close()
        output.seek(0)

        return output

    
def download_report_not_submited():

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})

    column_headers = ['Дата проверки', 'Объект', 'Муниципалитет', 'Предоставлен ли отчёт', 'Комментарии']
        
    row = 0

    for index, value in enumerate(column_headers):
        worksheet.write(row, index, value, bold)
        
    row += 1

    for item in CorrectionReport.objects.filter(has_completed=False):
        worksheet.write(row, 0, str(item.control_event.date.strftime("%d.%m.%Y")))
        worksheet.write(row, 1, str(item.control_event.object.name))
        worksheet.write(row, 2, str(item.control_event.object.location))
                
        has_given = str()
            
        if item.has_given:
            has_given = 'Представлен'
        else:
            has_given = 'Не представлен'

        worksheet.write(row, 3, has_given)
            
        if not item.has_completed:

            comments = str()

            for comment in CorrectionReportComment.objects.filter(correction_report=item):
                comments += f"{comment.comment}\n"

            worksheet.write(row, 4, comments)
                               
        row += 1

    workbook.close()
    output.seek(0)

    return output


@xlsx_file
def download_rating(workbook, worksheet, start_date, finish_date):

    column_headers = ['Место', 'Муниципалитет', 'Количество проверок', 'Средний балл']

    row = 0

    for index, value in enumerate(column_headers):
        worksheet.write(row, index, value)
    
    row += 1

    for item in getRating(start_date, finish_date):
        worksheet.write(row, 0, item['place'])
        worksheet.write(row, 1, item['location'].name)
        worksheet.write(row, 2, item['events_count'])
        worksheet.write(row, 3, item['avg_score'])

        row += 1
