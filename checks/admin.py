from django.contrib import admin

from checks.models import Location, Object, Question, Grade, ControlEvent, Result, ExecutiveDirector


class ObjectInline(admin.TabularInline):
    model = Object
    extra = 0


class ResultInline(admin.TabularInline):
    model = Result
    extra = 0


@admin.register(Location)
class LocationsAdmin(admin.ModelAdmin):
    inlines = [ObjectInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    pass


@admin.register(ControlEvent)
class ControlEventAdmin(admin.ModelAdmin):
    inlines = [ResultInline]

@admin.register(ExecutiveDirector)
class ExecutiveDirectorAdmin(admin.ModelAdmin):
    pass