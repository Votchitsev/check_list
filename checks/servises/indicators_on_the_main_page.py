from checks.models import ControlEvent, Result
from pprint import pprint
from checks.servises.count_score_of_control_event import count_score


class StartPageInfo:

    def __init__(self, queryset):
        self.queryset = queryset

    def count_of_control_events(self):
        return self.queryset.count()

    def count_of_negative_scores(self):
        events = self.queryset

        negative_scores = 0

        for e in events:
            if count_score(e) < 80 or Result.objects.filter(control_event=e.id, question_id=33)[0].grade.id == 5:
                negative_scores += 1

        return negative_scores

    def avg_result(self):
        events = self.queryset

        results = 0
        number_of_control_events = 0

        for e in events:
            results += count_score(e)
            number_of_control_events += 1
        try:
            return int(results / number_of_control_events)
        except ZeroDivisionError:
            return '-'

    def most_positive_and_negative_results(self):

        results = {}

        for i in self.queryset:
            results[i] = count_score(i)

        try:
            winner = max(results, key=results.get)
            looser = min(results, key=results.get)
        except ValueError:
            return {
                'winner':
                    {'object': '-',
                     'result': '-'},
                'looser':
                    {'object': '-',
                     'result': '-'}
        }

        return {
            'winner':
                {'object': winner,
                 'result': results[winner]},
            'looser':
                {'object': looser,
                 'result': results[looser]}
        }
