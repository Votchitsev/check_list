import io
import xlsxwriter

from checks.models import Result, ControlEvent
from checks.servises.count_score_of_control_event import Counter


class CheckListReport:

    def __init__(self, control_event):
        self.control_event = control_event
        self.queryset = Result.objects.filter(control_event=self.control_event)

    def download_check_list_file(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        bold = workbook.add_format({'bold': True})
        worksheet = workbook.add_worksheet()

        row = 0

        worksheet.write(row, 0, f"Объект: {self.queryset[0].control_event.object}"
                                f"Дата проверки: {self.queryset[0].control_event.date}",
                        bold)
        row += 1

        for item in self.queryset:
            worksheet.write(row, 0, str(item.question))
            worksheet.write(row, 1, str(item.grade))
            row += 1

        worksheet.write(row, 0, f"Итоговая оценка: {Counter(self.control_event).count_score()} балла(-ов)")
        row += 1
        worksheet.write(row, 0, f"Оценка управляющему: {Counter(self.control_event).manager_count_score()} балла(-ов)")
        row += 1
        worksheet.write(row, 0,
                        f"Оценка управляющему по производству: "
                        f"{Counter(self.control_event).production_count_score()} балла(-ов)")

        workbook.close()
        output.seek(0)

        return output

    def create_filename(self):
        return f"{self.queryset[0].control_event.date}_" \
               f"{self.queryset[0].control_event.object.name}.xlsx"


class MainReport:
    def __init__(self, start_date, finish_date):
        self.start_date = start_date
        self.finish_date = finish_date

    def download_file(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        bold = workbook.add_format({'bold': True})
        worksheet = workbook.add_worksheet()
        column_headers = ['Дата', 'Объект', 'Оценка', 'Баллы', 'Оценка управляющему',
                          'Оценка управляющему по производству', 'Наличие просроченной продукции', 
                          'Наличие недоброкачественной продукции']
        row = 0

        for index, header in enumerate(column_headers):
            worksheet.write(row, index, header, bold)
        row += 1

        for i in ControlEvent.objects.filter(date__range=[self.start_date, self.finish_date]).order_by('date'):
            counter = Counter(i.id)
            worksheet.write(row, 0, str(i.date))
            worksheet.write(row, 1, str(i.object))
            worksheet.write(row, 2, counter.common_grade())
            worksheet.write(row, 3, counter.count_score())
            worksheet.write(row, 4, counter.manager_count_score())
            worksheet.write(row, 5, counter.production_count_score())
            worksheet.write(row, 6, str(counter.is_overdue_food()))
            worksheet.write(row, 7, str(counter.is_poor_quality()))
            row += 1

        workbook.close()
        output.seek(0)

        return output
