from django.shortcuts import render, redirect
from django.urls import reverse


from checks.models import ControlEvent, CorrectionReport, CorrectionReportComment

def get_correction_report(request, control_event_id):
    control_event = ControlEvent.objects.filter(id=control_event_id)[0]
    correction_report = CorrectionReport.objects.filter(control_event=control_event_id)

    if len(correction_report) == 0:
        new_correction_report = CorrectionReport(
            control_event=control_event, 
            has_given=False, has_completed=False)
        new_correction_report.save()
        return redirect(reverse('get_correction_report', kwargs={'control_event_id': control_event_id}))

    has_given = str
    has_completed = str
    
    if correction_report[0].has_given == False: 
        has_given = 'Не представлен'
    else:
        has_given = 'Представлен'

    if correction_report[0].has_completed == False:
        has_completed = 'Не отработан'
    else:
        has_completed = 'Отработан'

    comments = CorrectionReportComment.objects.filter(correction_report_id=correction_report[0].id)
    
    context = {
        'control_event': control_event,
        'has_given': has_given,
        'has_completed': has_completed,
        'comment_list': comments,
    }

    return render(request, context=context, template_name='checks/correction_report.html')


def change_correction_report(request, control_event_id):
    correction_report = CorrectionReport.objects.filter(control_event=control_event_id)[0]
    action = request.GET['change']
    
    if action == 'has_given':

        if correction_report.has_given == False:
            correction_report.has_given = True
            correction_report.save()
            return redirect(reverse('get_correction_report', kwargs={'control_event_id': control_event_id}))
        else:
            correction_report.has_given = False
            correction_report.save()
            return redirect(reverse('get_correction_report', kwargs={'control_event_id': control_event_id}))

    if action == 'has_completed':
        
        if correction_report.has_completed == False:
            correction_report.has_completed = True
            correction_report.save()
            return redirect(reverse('get_correction_report', kwargs={'control_event_id': control_event_id}))
        else:
            correction_report.has_completed = False
            correction_report.save()
            return redirect(reverse('get_correction_report', kwargs={'control_event_id': control_event_id}))


def add_correction_report_comment(request, control_event_id):
    correction_report = CorrectionReport.objects.filter(control_event=control_event_id)[0]

    comment = CorrectionReportComment(correction_report=correction_report, comment=request.POST['text'])
    comment.save()

    return redirect(reverse('get_correction_report', kwargs={'control_event_id': control_event_id}))


def delete_correction_report_comment(request, control_event_id):
    deleting_comment = CorrectionReportComment.objects.filter(id=request.GET['id']).first() 
    deleting_comment.delete()

    return redirect(reverse('get_correction_report', kwargs={'control_event_id': control_event_id}))