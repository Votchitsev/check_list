from django.contrib import admin

from checks.models import Location, Object, Question, Grade, ControlEvent, Result, ExecutiveDirector, EmployeePosition, EmployeePositionQuestion


class ObjectInline(admin.TabularInline):
    model = Object
    extra = 0


class ResultInline(admin.TabularInline):
    model = Result
    extra = 0

class EmployeePositionInline(admin.TabularInline):
    model = EmployeePositionQuestion
    extra = 0

@admin.register(Location)
class LocationsAdmin(admin.ModelAdmin):
    inlines = [ObjectInline]

@admin.register(EmployeePosition)
class ResultAdmin(admin.ModelAdmin):
    pass

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [EmployeePositionInline]

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    pass


@admin.register(ControlEvent)
class ControlEventAdmin(admin.ModelAdmin):
    inlines = [ResultInline]

@admin.register(ExecutiveDirector)
class ExecutiveDirectorAdmin(admin.ModelAdmin):
    pass

@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    pass
