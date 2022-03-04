import io
import xlsxwriter

from checks.models import Result
from checks.servises.count_score_of_control_event import count_score


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

        worksheet.write(row, 0, f"Итоговая оценка: {count_score(self.control_event)} балла(-ов)")

        workbook.close()
        output.seek(0)

        return output

    def create_filename(self):
        return f"{self.queryset[0].control_event.date}_" \
               f"{self.queryset[0].control_event.object.name}.xlsx"